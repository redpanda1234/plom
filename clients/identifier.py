__author__ = "Andrew Rechnitzer"
__copyright__ = "Copyright (C) 2018-2019 Andrew Rechnitzer"
__credits__ = ["Andrew Rechnitzer", "Colin MacDonald", "Elvis Cai", "Matt Coles"]
__license__ = "GPLv3"

from collections import defaultdict
import csv
import json
import os
import tempfile
from PyQt5.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
    QStringListModel,
    QTimer,
    QVariant,
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QCompleter, QDialog, QInputDialog, QMessageBox
from examviewwindow import ExamViewWindow
import messenger
from useful_classes import ErrorMessage, SimpleMessage
from uiFiles.ui_identify import Ui_IdentifyWindow

# set up variables to store paths for marker and id clients
tempDirectory = tempfile.TemporaryDirectory()
directoryPath = tempDirectory.name


class Paper:
    """A simple container for storing a test's idgroup code (tgv) and
    the associated filename for the image. Once identified also
    store the studentName and ID-numer.
    """

    def __init__(self, tgv, fname, stat="unidentified", id="", name=""):
        # tgv = t0000p00v0
        # ... = 0123456789
        # The test-IDgroup code
        self.prefix = tgv
        # The test number
        self.test = tgv[1:5]
        # Set status as unid'd
        self.status = stat
        # no name or id-number yet.
        self.sname = name
        self.sid = id
        # the filename of the image.
        self.originalFile = fname

    def setStatus(self, st):
        self.status = st

    def setReverted(self):
        # reset the test as unidentified and no ID or name.
        self.status = "unidentified"
        self.sid = ""
        self.sname = ""

    def setID(self, sid, sname):
        # tgv = t0000p00v0
        # ... = 0123456789
        # Set the test as ID'd and store name / number.
        self.status = "identified"
        self.sid = sid
        self.sname = sname


class ExamModel(QAbstractTableModel):
    """A tablemodel for handling the test-ID-ing data."""

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        # Data stored in this ordered list.
        self.paperList = []
        # Headers.
        self.header = ["Code", "Status", "ID", "Name"]

    def setData(self, index, value, role=Qt.EditRole):
        # Columns are [code, status, ID and Name]
        # Put data in appropriate box when setting.
        if role != Qt.EditRole:
            return False
        if index.column() == 0:
            self.paperList[index.row()].prefix = value
            self.dataChanged.emit(index, index)
            return True
        elif index.column() == 1:
            self.paperList[index.row()].status = value
            self.dataChanged.emit(index, index)
            return True
        elif index.column() == 2:
            self.paperList[index.row()].sid = value
            self.dataChanged.emit(index, index)
            return True
        elif index.column() == 3:
            self.paperList[index.row()].sname = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def identifyStudent(self, index, sid, sname):
        # When ID'd - set status, ID and Name.
        self.setData(index[1], "identified")
        self.setData(index[2], sid)
        self.setData(index[3], sname)

    def revertStudent(self, index):
        # When reverted - set status, ID and Name appropriately.
        self.setData(index[1], "unidentified")
        self.setData(index[2], "")
        self.setData(index[3], "")

    def addPaper(self, rho):
        # Append paper to list and update last row of table
        r = self.rowCount()
        self.beginInsertRows(QModelIndex(), r, r)
        self.paperList.append(rho)
        self.endInsertRows()
        return r

    def rowCount(self, parent=None):
        return len(self.paperList)

    def columnCount(self, parent=None):
        return 4

    def data(self, index, role=Qt.DisplayRole):
        # Columns are [code, status, ID and Name]
        # Get data from appropriate box when called.
        if role != Qt.DisplayRole:
            return QVariant()
        elif index.column() == 0:
            return self.paperList[index.row()].prefix
        elif index.column() == 1:
            return self.paperList[index.row()].status
        elif index.column() == 2:
            return self.paperList[index.row()].sid
        elif index.column() == 3:
            return self.paperList[index.row()].sname
        return QVariant()

    def headerData(self, c, orientation, role):
        # Return the correct header.
        if role != Qt.DisplayRole:
            return
        elif orientation == Qt.Horizontal:
            return self.header[c]
        return c


class IDClient(QDialog):
    def __init__(self, userName, password, server, message_port, web_port):
        # Init the client with username, password, server and port data.
        super(IDClient, self).__init__()
        # Init the messenger with server and port data.
        messenger.setServerDetails(server, message_port, web_port)
        messenger.startMessenger()
        # Ping to see if server is up.
        if not messenger.pingTest():
            self.deleteLater()
            return
        # Save username, password, and path the local temp directory for
        # image files and the class list.
        self.userName = userName
        self.password = password
        self.workingDirectory = directoryPath
        # List of papers we have to ID.
        self.paperList = []
        self.unidCount = 0
        # Fire up the interface.
        self.ui = Ui_IdentifyWindow()
        self.ui.setupUi(self)
        # Paste username into the GUI.
        self.ui.userLabel.setText(self.userName)
        # Exam model for the table of papers - associate to table in GUI.
        self.exM = ExamModel()
        self.ui.tableView.setModel(self.exM)
        # A view window for the papers so user can zoom in as needed.
        # Paste into appropriate location in gui.
        self.testImg = ExamViewWindow()
        self.ui.gridLayout_7.addWidget(self.testImg, 0, 0)
        # Start using connection to server.
        # Ask server to authenticate user and return the authentication token.
        self.requestToken()
        # Get the classlist from server for name/ID completion.
        self.getClassList()
        # Init the name/ID completers and a validator for ID
        self.setCompleters()
        # Get the predicted list from server for ID guesses.
        self.getPredictions()
        # Connect buttons and key-presses to functions.
        self.ui.idEdit.returnPressed.connect(self.enterID)
        self.ui.nameEdit.returnPressed.connect(self.enterName)
        self.ui.closeButton.clicked.connect(self.shutDown)
        self.ui.nextButton.clicked.connect(self.requestNext)
        # Make sure no button is clicked by a return-press
        self.ui.nextButton.setAutoDefault(False)
        self.ui.closeButton.setAutoDefault(False)

        # Make sure window is maximised and request a paper from server.
        self.showMaximized()
        # Get list of papers already ID'd and add to table.
        self.getAlreadyIDList()
        # Connect the view **after** list updated.
        # Connect the table's model sel-changed to appropriate function.
        self.ui.tableView.selectionModel().selectionChanged.connect(self.selChanged)
        self.requestNext()
        # make sure exam view window's view is reset....
        # very slight delay to ensure things loaded first
        QTimer.singleShot(100, self.testImg.view.resetView)

    def requestToken(self):
        """Send authorisation request (AUTH) to server. The request sends name and
        password (over ssl) to the server. If hash of password matches the one
        of file, then the server sends back an "ACK" and an authentication
        token. The token is then used to authenticate future transactions with
        the server (since password hashing is slow).
        """
        # Send and return message with messenger.
        msg = messenger.SRMsg(["AUTH", self.userName, self.password])
        # Return should be [ACK, token]
        # Either a problem or store the resulting token.
        if msg[0] == "ERR":
            ErrorMessage("Password problem")
            quit()
        else:
            self.token = msg[1]

    def getClassList(self):
        """Send request for classlist (iRCL) to server. The server then sends
        back the CSV of the classlist.
        Merge the two name-fields. Should replace this with the requirement
        of either two fields = FamilyName+GivenName or a single Name field.
        """
        # Send request for classlist (iRCL) to server
        msg = messenger.SRMsg(["iRCL", self.userName, self.token])
        # Return should be [ACK, path/filename]
        if msg[0] == "ERR":
            ErrorMessage("Classlist problem")
            quit()
        # Get the filename from the message.
        dfn = msg[1]
        fname = os.path.join(self.workingDirectory, "cl.csv")
        # Get file from dav and copy into local temp working dir as cl.csv
        messenger.getFileDav(dfn, fname)
        # create dictionaries to store the classlist
        self.studentNamesToNumbers = defaultdict(int)
        self.studentNumbersToNames = defaultdict(str)
        # Read cl.csv into those dictionaries
        with open(fname) as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            for row in reader:
                # Merge names into single field
                sn = row["surname"] + ", " + row["name"]
                self.studentNamesToNumbers[sn] = str(row["id"])
                self.studentNumbersToNames[str(row["id"])] = sn
        # Now that we've read in the classlist - tell server we got it
        # Server will remove it from the webdav server.
        msg = messenger.SRMsg(["iDWF", self.userName, self.token, dfn])
        if msg[0] == "ERR":
            ErrorMessage("Classlist problem")
            quit()
        return True

    def getPredictions(self):
        """Send request for classlist (iRPL) to server. The server then sends
        back the CSV of the predictions testnumber -> studentID.
        """
        # Send request for classlist (iRCL) to server
        msg = messenger.SRMsg(["iRPL", self.userName, self.token])
        # Return should be [ACK, path/filename]
        if msg[0] == "ERR":
            ErrorMessage("Prediction list problem")
            quit()
        # Get the filename from the message.
        dfn = msg[1]
        fname = os.path.join(self.workingDirectory, "pl.csv")
        # Get file from dav and copy into local temp working dir as cl.csv
        messenger.getFileDav(dfn, fname)
        # create dictionaries to store the classlist
        self.predictedTestToNumbers = defaultdict(int)
        # Read pl.csv into those dictionaries
        with open(fname) as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            for row in reader:
                self.predictedTestToNumbers[int(row["test"])] = str(row["id"])
        # Now that we've read in the classlist - tell server we got it
        # Server will remove it from the webdav server.
        msg = messenger.SRMsg(["iDWF", self.userName, self.token, dfn])
        if msg[0] == "ERR":
            ErrorMessage("Prediction list problem")
            quit()
        # Also tweak font size
        fnt = self.font()
        fnt.setPointSize(fnt.pointSize() * 2)
        self.ui.pNameLabel.setFont(fnt)
        fnt.setPointSize(fnt.pointSize() * 1.5)
        self.ui.pSIDLabel.setFont(fnt)
        # And if no predictions then hide that box
        if len(self.predictedTestToNumbers) == 0:
            self.ui.predictionBox.hide()

        return True

    def setCompleters(self):
        """Set up the studentname + studentnumber line-edit completers.
        Means that user can enter the first few numbers (or letters) and
        be prompted with little pop-up with list of possible completions.
        """
        # Build stringlistmodels - one for ID and one for names.
        self.sidlist = QStringListModel()
        self.snamelist = QStringListModel()
        # Feed in the numbers and names.
        self.sidlist.setStringList(list(self.studentNumbersToNames.keys()))
        self.snamelist.setStringList(list(self.studentNamesToNumbers.keys()))
        # Build the number-completer
        self.sidcompleter = QCompleter()
        self.sidcompleter.setModel(self.sidlist)
        # Build the name-completer (matches substring, not just prefix)
        self.snamecompleter = QCompleter()
        self.snamecompleter.setModel(self.snamelist)
        self.snamecompleter.setCaseSensitivity(Qt.CaseInsensitive)
        self.snamecompleter.setFilterMode(Qt.MatchContains)
        # Link the ID-completer to the ID-lineedit in the gui.
        self.ui.idEdit.setCompleter(self.sidcompleter)
        # Similarly for the name-completer
        self.ui.nameEdit.setCompleter(self.snamecompleter)
        # Make sure both lineedits have little "Clear this" buttons.
        self.ui.idEdit.setClearButtonEnabled(True)
        self.ui.nameEdit.setClearButtonEnabled(True)
        # the id-line edit needs a validator to make sure that only 8 digit numbers entered
        self.idValidator = QIntValidator(10000000, 10 ** 8 - 1)
        self.ui.idEdit.setValidator(self.idValidator)

    def shutDown(self):
        """Send the server a DNF (did not finish) message so it knows to
        take anything that this user has out-for-id-ing and return it to
        the todo pile. Then send a user-closing message so that the
        authorisation token is removed. Then finally close.
        """
        self.DNF()
        msg = messenger.SRMsg(["UCL", self.userName, self.token])
        self.close()

    def DNF(self):
        """Send the server a "did not finished" message for each paper
        in the list that has not been ID'd. The server will put these back
        onto the todo-pile.
        """
        # Go through each entry in the table - it not ID'd then send a DNF
        # to the server.
        rc = self.exM.rowCount()
        for r in range(rc):
            if self.exM.data(self.exM.index(r, 1)) != "identified":
                # Tell user DNF, user, auth-token, and paper's code.
                msg = messenger.SRMsg(
                    [
                        "iDNF",
                        self.userName,
                        self.token,
                        self.exM.data(self.exM.index(r, 0)),
                    ]
                )

    def getAlreadyIDList(self):
        # Ask server for list of previously marked papers
        msg = messenger.SRMsg(["iGAL", self.userName, self.token])
        if msg[0] == "ERR":
            return
        fname = os.path.join(self.workingDirectory, "idList.txt")
        messenger.getFileDav(msg[1], fname)
        # Ack that test received - server then deletes it from webdav
        msg = messenger.SRMsg(["iDWF", self.userName, self.token, msg[1]])
        # Add those marked papers to our paper-list
        with open(fname) as json_file:
            idList = json.load(json_file)
            for x in idList:
                self.addPaperToList(
                    Paper(x[0], fname="", stat="identified", id=x[2], name=x[3]),
                    update=False,
                )

    def selChanged(self, selnew, selold):
        # When the selection changes, update the ID and name line-edit boxes
        # with the data from the table - if it exists.
        # Update the displayed image with that of the newly selected test.
        self.ui.idEdit.setText(self.exM.data(selnew.indexes()[2]))
        self.ui.nameEdit.setText(self.exM.data(selnew.indexes()[3]))
        self.updateImage(selnew.indexes()[0].row())

    def checkFiles(self, r):
        tgv = self.exM.paperList[r].prefix
        if self.exM.paperList[r].originalFile is not "":
            return
        msg = messenger.SRMsg(["iGGI", self.userName, self.token, tgv])
        if msg[0] == "ERR":
            return
        fname = os.path.join(self.workingDirectory, "{}.png".format(msg[1]))
        tfname = msg[2]  # the temp original image file on webdav
        messenger.getFileDav(tfname, fname)
        # got original file so ask server to remove it.
        msg = messenger.SRMsg(["iDWF", self.userName, self.token, tfname])
        self.exM.paperList[r].originalFile = fname

    def updateImage(self, r=0):
        # Here the system should check if imagefile exist and grab if needed.
        self.checkFiles(r)
        # Update the test-image pixmap with the image in the indicated file.
        self.testImg.updateImage(self.exM.paperList[r].originalFile)
        # update the prediction if present
        tn = int(self.exM.paperList[r].test)
        if self.exM.paperList[r].status == "identified":
            self.ui.pSIDLabel.setText(self.exM.paperList[r].sid)
            self.ui.pNameLabel.setText(self.exM.paperList[r].sname)
            QTimer.singleShot(0, self.setuiedit)
        elif tn in self.predictedTestToNumbers:
            psid = self.predictedTestToNumbers[tn]
            pname = self.studentNumbersToNames[psid]
            self.ui.pSIDLabel.setText(psid)
            self.ui.pNameLabel.setText(pname)
            QTimer.singleShot(0, self.setuiedit)
        else:
            self.ui.pSIDLabel.setText("")
            self.ui.pNameLabel.setText("")
            QTimer.singleShot(0, self.ui.idEdit.clear)
            self.ui.idEdit.setFocus()

    def setuiedit(self):
        self.ui.idEdit.setText(self.ui.pSIDLabel.text())

    def addPaperToList(self, paper, update=True):
        # Add paper to the exam-table-model - get back the corresponding row.
        r = self.exM.addPaper(paper)
        # select that row and display the image
        if update:
            # One more unid'd paper
            self.unidCount += 1
            self.ui.tableView.selectRow(r)
            self.updateImage(r)

    def requestNext(self):
        """Ask the server for an unID'd paper (iNID). Server should return
        message [ACK, testcode, filename]. Get file from webdav, add to the
        list of papers and update the image.
        """
        # ask server for id-count update
        msg = messenger.SRMsg(["iPRC", self.userName, self.token])
        # returns [ACK, #id'd, #total]
        if msg[0] == "ACK":
            self.ui.idProgressBar.setMaximum(msg[2])
            self.ui.idProgressBar.setValue(msg[1])

        # ask server for next unid'd paper
        msg = messenger.SRMsg(["iNID", self.userName, self.token])
        if msg[0] == "ERR":
            return
        # return message is [ACK, code, filename]
        test = msg[1]
        fname = msg[2]
        # Image name will be <code>.png
        iname = os.path.join(
            self.workingDirectory, test + ".png"
        )  # windows/linux compatibility
        # Grab image from webdav and copy to <code.png>
        messenger.getFileDav(fname, iname)
        # Add the paper [code, filename, etc] to the list
        self.addPaperToList(Paper(test, iname))
        # Tell server we got the image (iGTP) - the server then deletes it.
        msg = messenger.SRMsg(["iDWF", self.userName, self.token, fname])
        # Clean up table - and set focus on the ID-lineedit so user can
        # just start typing in the next ID-number.
        self.ui.tableView.resizeColumnsToContents()
        self.ui.idEdit.setFocus()

    def identifyStudent(self, index, alreadyIDd=False):
        """User ID's the student of the current paper. Some care around whether
        or not the paper was ID'd previously. Not called directly - instead
        is called by "enterID" or "enterName" when user hits return on either
        of those lineedits.
        """
        # Pass the contents of the ID-lineedit and Name-lineedit to the exam
        # model to put data into the table.
        self.exM.identifyStudent(index, self.ui.idEdit.text(), self.ui.nameEdit.text())
        code = self.exM.data(index[0])
        if alreadyIDd:
            # If the paper was ID'd previously send return-already-ID'd (iRAD)
            # with the code, ID, name.
            msg = messenger.SRMsg(
                [
                    "iRAD",
                    self.userName,
                    self.token,
                    code,
                    self.ui.idEdit.text(),
                    self.ui.nameEdit.text(),
                ]
            )
        else:
            # If the paper was not ID'd previously send return-ID'd (iRID)
            # with the code, ID, name.
            msg = messenger.SRMsg(
                [
                    "iRID",
                    self.userName,
                    self.token,
                    code,
                    self.ui.idEdit.text(),
                    self.ui.nameEdit.text(),
                ]
            )
        if msg[0] == "ERR":
            # If an error, revert the student and clear things.
            self.exM.revertStudent(index)
            # Use timer to avoid conflict between completer and
            # clearing the line-edit. Very annoying but this fixes it.
            QTimer.singleShot(0, self.ui.idEdit.clear)
            QTimer.singleShot(0, self.ui.nameEdit.clear)
            return False
        else:
            # Use timer to avoid conflict between completer and
            # clearing the line-edit. Very annoying but this fixes it.
            QTimer.singleShot(0, self.ui.idEdit.clear)
            QTimer.singleShot(0, self.ui.nameEdit.clear)
            # Update un-id'd count.
            if not alreadyIDd:
                self.unidCount -= 1
            return True

    def moveToNextUnID(self):
        # Move to the next test in table which is not ID'd.
        rt = self.exM.rowCount()
        if rt == 0:
            return
        rstart = self.ui.tableView.selectedIndexes()[0].row()
        r = (rstart + 1) % rt
        # Be careful to not get stuck in loop if all are ID'd.
        while self.exM.data(self.exM.index(r, 1)) == "identified" and r != rstart:
            r = (r + 1) % rt
        self.ui.tableView.selectRow(r)

    def enterID(self):
        """Triggered when user hits return in the ID-lineedit.. that is
        when they have entered a full student ID.
        """
        # if no papers then simply return.
        if self.exM.rowCount() == 0:
            return
        # Grab table-index and code of current test.
        index = self.ui.tableView.selectedIndexes()
        code = self.exM.data(index[0])
        # No code then return.
        if code is None:
            return
        # Get the status of the test
        status = self.exM.data(index[1])
        alreadyIDd = False
        # If the paper is already ID'd ask the user if they want to
        # change it - set the alreadyIDd flag to true.
        if status == "identified":
            msg = SimpleMessage("Do you want to change the ID?")
            # Put message popup on top-corner of idenfier window
            msg.move(self.pos())
            if msg.exec_() == QMessageBox.No:
                return
            else:
                alreadyIDd = True
        # Check if the entered ID is in the list from the classlist.
        if self.ui.idEdit.text() in self.studentNumbersToNames:
            # If so then fill in the name-edit with the corresponding name.
            self.ui.nameEdit.setText(self.studentNumbersToNames[self.ui.idEdit.text()])
            # Ask user to confirm ID/Name
            msg = SimpleMessage(
                "Student ID {} = {}. Enter and move to next?".format(
                    self.ui.idEdit.text(), self.ui.nameEdit.text()
                )
            )
            # Put message popup on top-corner of idenfier window
            msg.move(self.pos())
            # If user says "no" then just return from function.
            if msg.exec_() == QMessageBox.No:
                return
        else:
            # Number is not in class list - ask user if they really want to
            # enter that number.
            msg = SimpleMessage(
                "Student ID {} not in list. Do you want to enter it anyway?".format(
                    self.ui.idEdit.text()
                )
            )
            # Put message popup on top-corner of idenfier window
            msg.move(self.pos())
            # If no then return from function.
            if msg.exec_() == QMessageBox.No:
                return
            # Otherwise get a name from the user (and the okay)
            name, ok = QInputDialog.getText(self, "Enter name", "Enter student name:")
            # If okay, then set name accordingly, else set name to "unknown"
            if ok:
                self.ui.nameEdit.setText(str(name))
            else:
                self.ui.nameEdit.setText("Unknown")
        # Run identify student command (which talks to server)
        if self.identifyStudent(index, alreadyIDd):
            # if successful, and everything local has been ID'd get next
            if alreadyIDd is False and self.unidCount == 0:
                self.requestNext()
            else:
                # otherwise move to the next unidentified paper.
                self.moveToNextUnID()
        return

    def enterName(self):
        """Triggered when user hits return in the name-lineedit.. that is
        when they have entered a full student ID.
        """
        # if no papers then simply return.
        if self.exM.rowCount() == 0:
            return
        # Grab table-index and code of current test.
        index = self.ui.tableView.selectedIndexes()
        code = self.exM.data(index[0])
        # No code then return.
        if code is None:
            return
        # Get the status of the test
        status = self.exM.data(index[1])
        alreadyIDd = False
        # If the paper is already ID'd ask the user if they want to
        # change it - set the alreadyIDd flag to true.
        if status == "identified":
            msg = SimpleMessage("Do you want to change the ID?")
            # Put message popup on top-corner of idenfier window
            msg.move(self.pos())
            if msg.exec_() == QMessageBox.No:
                return
            else:
                alreadyIDd = True
        # Check if the entered name is in the list from the classlist.
        if self.ui.nameEdit.text() in self.studentNamesToNumbers:
            # If so then fill in the ID-edit with the corresponding number.
            self.ui.idEdit.setText(self.studentNamesToNumbers[self.ui.nameEdit.text()])
            # Ask user to confirm ID/Name
            msg = SimpleMessage(
                "Student ID {} = {}. Enter and move to next?".format(
                    self.ui.idEdit.text(), self.ui.nameEdit.text()
                )
            )
            # Put message popup on top-corner of idenfier window
            msg.move(self.pos())
            # If user says "no" then just return from function.
            if msg.exec_() == QMessageBox.No:
                return
        else:
            # Name is not in class list - ask user if they really want to
            # enter that name.
            msg = SimpleMessage(
                "Student name {} not in list. Do you want to enter it anyway?".format(
                    self.ui.nameEdit.text()
                )
            )
            # Put message popup on top-corner of idenfier window
            msg.move(self.pos())
            # If no then return from function.
            if msg.exec_() == QMessageBox.No:
                return
            # Otherwise get a number from the user (and the okay)
            num, ok = QInputDialog.getText(
                self, "Enter number", "Enter student number:"
            )
            # If okay, then set number accordingly, else give error
            if ok:
                self.ui.idEdit.setText(str(num))
            else:
                msg = ErrorMessage("Cannot enter without a student number.")
                msg.exec_()
                return
        # Run identify student command (which talks to server)
        if self.identifyStudent(index, alreadyIDd):
            # if successful, and everything local has been ID'd get next
            if alreadyIDd is False and self.unidCount == 0:
                self.requestNext()
            else:
                # otherwise move to the next unidentified paper.
                self.moveToNextUnID()
        return