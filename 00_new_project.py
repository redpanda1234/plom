import sys
import os
import shutil
import locale
from PyQt5.QtWidgets import QApplication, QDialog, QErrorMessage, QFileDialog, QGridLayout, QMessageBox, QPushButton, QTreeWidget, QTreeWidgetItem, QWidget
from resources.uiFiles.ui_launcher import Ui_Launcher

directories = ['build', 'finishing', 'imageServer', 'resources', 'scanAndGroup']
directories += ['build/examsToPrint', 'build/sourceVersions']
directories += ['scanAndGroup/decodedPages', 'scanAndGroup/pageImages/', 'scanAndGroup/readyForMarking', 'scanAndGroup/scannedExams']
directories += ['imageServer/markedPapers']
directories += ['clients', 'clients/uiFiles', 'clients/icons']
directories += ['finishing/frontPages', 'finishing/reassembled/']

files = ['resources/testspecification.py']
files += ['build/01_construct_a_specification.py', 'build/cleanAll.py', 'build/02_build_tests_from_spec.py', 'build/mergeAndCodePages.py', 'build/buildTestPDFs.py', 'build/testspecification.py']
files += [
'scanAndGroup/03_scans_to_page_images.py', 'scanAndGroup/cleanAll.py', 'scanAndGroup/04_decode_images.py', 'scanAndGroup/extractQRAndOrient.py', 'scanAndGroup/05_missing_pages.py', 'scanAndGroup/manualPageIdentifier.py', 'scanAndGroup/06_group_pages.py', 'scanAndGroup/testspecification.py']

files += ['imageServer/authenticate.py', 'imageServer/davconf.conf', 'imageServer/mark_manager.py', 'imageServer/examviewwindow.py', 'imageServer/mark_storage.py', 'imageServer/id_storage.py',  'imageServer/identify_manager.py', 'imageServer/userManager.py', 'imageServer/image_server.py']

files += ['clients/mlp_client.py', 'clients/mlp_marker.py', 'clients/mlp_identifier.py', 'clients/mlp_annotator.py', 'clients/mlp_messenger.py', 'clients/mlp_useful.py', 'clients/mlp_markentry.py', 'clients/pageview.py', 'clients/pagescene.py', 'clients/tools.py', 'clients/examviewwindow.py', 'clients/reorientationwindow.py']

files += ['clients/uiFiles/ui_annotator.py', 'clients/uiFiles/ui_chooser.py', 'clients/uiFiles/ui_identify.py', 'clients/uiFiles/ui_marker.py']

files += ['clients/icons/cross.svg', 'clients/icons/pan.svg', 'clients/icons/text.svg', 'clients/icons/delete.svg', 'clients/icons/pen.svg', 'clients/icons/tick.svg', 'clients/icons/line.svg', 'clients/icons/rectangle.svg', 'clients/icons/undo.svg', 'clients/icons/move.svg', 'clients/icons/redo.svg', 'clients/icons/zoom.svg']

files += [
'finishing/07_check_completed.py', 'finishing/coverPageBuilder.py', 'finishing/08_build_cover_pages.py', 'finishing/testReassembler.py', 'finishing/09_reassemble.py', 'finishing/testspecification.py'
]

class ErrorMessage(QMessageBox):
    def __init__(self, txt):
        super(ErrorMessage, self).__init__()
        self.setText(txt)
        self.setStandardButtons(QMessageBox.Ok)

class SimpleMessage(QMessageBox):
    def __init__(self, txt):
        super(SimpleMessage, self).__init__()
        self.setText(txt)
        self.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        self.setDefaultButton(QMessageBox.Yes)

class LeftToDo(QDialog):
    def __init__(self):
        super(LeftToDo, self).__init__()
        tasks = {}
        tasks['Right now'] = ['Go to project']
        tasks['Build'] = ['Name test', 'Set number of source tests', 'Copy source tests into place', 'Set up page grouping', 'Set up version choices for page groups', 'Set total number of tests to produce']
        tasks['Run the test'] = ['Print tests', 'Run test', 'Make students happy', 'Scan tests']
        tasks['Scan and Group'] = ['Copy test scans to scannedExams', 'Convert scans to page images', 'Decode page images', 'Check for missing pages', 'Group page images into page-groups']
        tasks['Image server'] = ['Make sure you have access to two ports', 'Set up users', 'Run the image server', 'Check progress with ID-manager', 'Check progress with Marking-manager']
        tasks['Clients'] = ['Give markers client apps']
        tasks['Finishing'] = ['Check tests are completed', 'Build cover pages', 'Reassemble papers']

        self.setWindowTitle("What to do next")
        self.setModal(True)
        grid = QGridLayout()

        self.taskTW = QTreeWidget()
        self.taskTW.setColumnCount(1)
        self.taskTW.setHeaderLabel('Tasks')
        grid.addWidget(self.taskTW, 1, 1, 3, 2)
        for t in tasks:
            tmp = QTreeWidgetItem(self.taskTW)
            tmp.setText(0, t)
            self.taskTW.addTopLevelItem(tmp)
            for tx in tasks[t]:
                tmp2 = QTreeWidgetItem(tmp)
                tmp2.setText(0, tx)
                tmp.addChild(tmp2)

        self.taskTW.adjustSize()

        self.closeB = QPushButton("Close")
        grid.addWidget(self.closeB, 4, 4)
        self.closeB.clicked.connect(self.accept)
        self.setLayout(grid)


def buildDirs(projPath):
    for dir in directories:
        try:
            os.mkdir(projPath+"/"+dir)
        except:
            pass

def copyFiles(projPath):
    for fname in files:
        try:
            shutil.copyfile(fname, projPath+'/'+fname)
        except:
            pass

def buildKey(projPath):
    print("Building new ssl key/certificate for server")
    # Command to generate the self-signed key:
    #     openssl req -x509 -newkey rsa:2048 -keyout selfsigned.key -nodes -out selfsigned.cert -sha256 -days 1000
    sslcmd = "openssl req -x509 -sha256 -newkey rsa:2048 -keyout {}/resources/mlp.key -nodes -out {}/resources/mlp-selfsigned.crt -days 1000".format(projPath, projPath)
    sslcmd += " -subj \'/C={}/ST=./L=./CN=localhost\'".format(locale.getdefaultlocale()[0][-2:])
    print(sslcmd)
    os.system(sslcmd)


def doThings(projPath):
    try:
        os.mkdir(projPath)
    except FileExistsError:
        msg = SimpleMessage('Directory {} already exists. Okay to continue?'.format(projPath))
        if msg.exec_() == QMessageBox.No:
            return

    msg = ErrorMessage('Building directories and moving scripts')
    msg.exec_()
    buildDirs(projPath)
    copyFiles(projPath)

    msg = ErrorMessage('Building new ssl key for image server')
    msg.exec_()
    buildKey(projPath)

    msg = ErrorMessage('Set manager password')
    msg.exec_()
    cpwd = os.getcwd()
    os.chdir(projPath+'/imageServer')
    os.system('python3 userManager.py')
    os.chdir(cpwd)

    msg = LeftToDo()
    msg.exec_()

class ProjectLauncher(QWidget):
    def __init__(self):
        super(ProjectLauncher, self).__init__()
        self.projPath = None
        self.ui = Ui_Launcher()
        self.ui.setupUi(self)

        self.ui.setLocButton.clicked.connect(self.getDirectory)
        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.createButton.clicked.connect(self.createProject)

    def getDirectory(self):
        home = os.getenv("HOME")
        dir = QFileDialog.getExistingDirectory(self, "Choose a location for your project", home, QFileDialog.ShowDirsOnly|QFileDialog.DontResolveSymlinks)
        if os.path.isdir(dir):
            self.ui.directoryLE.setText(dir)

    def createProject(self):
        self.projName = self.ui.nameLE.text()
        if self.projName.isalnum():
            self.projPath = self.ui.directoryLE.text() + '/' + self.projName
            doThings(self.projPath)
        else:
            msg = ErrorMessage('Project name must be an alphanumeric string')
            msg.exec_()
            return
        self.close()

app = QApplication(sys.argv)
window = ProjectLauncher()
window.show()
rv = app.exec_()
sys.exit(rv)