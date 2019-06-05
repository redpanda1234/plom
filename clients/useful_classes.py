__author__ = "Andrew Rechnitzer"
__copyright__ = "Copyright (C) 2018-2019 Andrew Rechnitzer"
__credits__ = ["Andrew Rechnitzer", "Colin MacDonald", "Elvis Cai", "Matt Coles"]
__license__ = "GPLv3"
import os
import json

from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QDropEvent, QIcon, QPixmap, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QGridLayout,
    QMessageBox,
    QPushButton,
    QTableView,
    QToolButton,
    QWidget,
    QItemDelegate,
)


class ErrorMessage(QMessageBox):
    """A simple error message pop-up"""

    def __init__(self, txt):
        super(ErrorMessage, self).__init__()
        self.setText(txt)
        self.setStandardButtons(QMessageBox.Ok)


class SimpleMessage(QMessageBox):
    """A simple message pop-up with yes/no buttons and
    large font.
    """

    def __init__(self, txt):
        super(SimpleMessage, self).__init__()
        self.setText(txt)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setDefaultButton(QMessageBox.Yes)
        fnt = self.font()
        fnt.setPointSize((fnt.pointSize() * 3) // 2)
        self.setFont(fnt)


class SimpleMessageCheckBox(QMessageBox):
    """A simple message pop-up with yes/no buttons, a checkbox and
    large font.
    """

    def __init__(self, txt):
        super(SimpleMessageCheckBox, self).__init__()
        self.cb = QCheckBox("Don't show this message again")
        self.setText(txt)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setDefaultButton(QMessageBox.Yes)
        self.setCheckBox(self.cb)

        fnt = self.font()
        fnt.setPointSize((fnt.pointSize() * 3) // 2)
        self.setFont(fnt)


class SimpleTableView(QTableView):
    """A table-view widget that emits annotateSignal when
    the user hits enter or return.
    """

    # This is picked up by the marker, lets it know to annotate
    annotateSignal = pyqtSignal()

    def __init__(self, parent=None):
        super(SimpleTableView, self).__init__()
        # User can sort, cannot edit, selects by rows.
        self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def keyPressEvent(self, event):
        # If user hits enter or return, then fire off
        # the annotateSignal, else pass the event on.
        key = event.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.annotateSignal.emit()
        else:
            super(SimpleTableView, self).keyPressEvent(event)


class SimpleToolButton(QToolButton):
    """Specialise the tool button to be an icon above text."""

    def __init__(self, txt, icon):
        super(SimpleToolButton, self).__init__()
        self.setText(txt)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setIcon(QIcon(QPixmap(icon)))
        self.setIconSize(QSize(24, 24))
        self.setMinimumWidth(100)


class CommentWidget(QWidget):
    """A widget wrapper around the marked-comment table."""

    def __init__(self, parent=None):
        # layout the widget - a table and add/delete buttons.
        super(CommentWidget, self).__init__()
        grid = QGridLayout()
        # the table has 2 cols, delta&comment.
        self.CL = SimpleCommentTable(self)
        grid.addWidget(self.CL, 1, 1, 2, 3)
        self.addB = QPushButton("Add")
        self.delB = QPushButton("Delete")
        grid.addWidget(self.addB, 3, 1)
        grid.addWidget(self.delB, 3, 3)
        self.setLayout(grid)
        # connect the buttons to functions.
        self.addB.clicked.connect(self.addItem)
        self.delB.clicked.connect(self.deleteItem)

    def setStyle(self, markStyle):
        # The list needs a style-delegate because the display
        # of the delta-mark will change depending on
        # the current total mark and whether mark
        # total or up or down. Delta-marks that cannot
        # be assigned will be shaded out to indicate that
        # they will not be pasted into the window.
        self.CL.delegate.style = markStyle

    def changeMark(self, maxMark, currentMark):
        # Update the current and max mark for the lists's
        # delegate so that it knows how to display the comments
        # and deltas when the mark changes.
        self.CL.delegate.maxMark = maxMark
        self.CL.delegate.currentMark = currentMark
        self.CL.viewport().update()

    def saveComments(self):
        self.CL.saveCommentList()

    def addItem(self):
        self.CL.addItem()

    def deleteItem(self):
        self.CL.deleteItem()

    def currentItem(self):
        # grab focus and trigger a "row selected" signal
        # in the comment list
        self.CL.currentItem()
        self.setFocus()

    def nextItem(self):
        # grab focus and trigger a "row selected" signal
        # in the comment list
        self.CL.nextItem()
        self.setFocus()

    def previousItem(self):
        # grab focus and trigger a "row selected" signal
        # in the comment list
        self.CL.previousItem()
        self.setFocus()


class commentDelegate(QItemDelegate):
    """A style delegate that changes how rows of the
    comment list are displayed. In particular, the
    delta will be shaded out if it cannot be applied
    given the current mark and the max mark.
    Eg - if marking down then all positive delta are shaded
    if marking up then all negative delta are shaded
    if mark = 7/10 then any delta >= 4 is shaded.
    """

    def __init__(self):
        super(commentDelegate, self).__init__()
        self.currentMark = 0
        self.maxMark = 0
        self.style = 0

    def paint(self, painter, option, index):
        # Only run the standard delegate if flag is true.
        # else don't paint anything.
        flag = True
        # Only shade the deltas which are in col 0.
        if index.column() == 0:
            # Grab the delta value.
            delta = int(index.model().data(index, Qt.EditRole))
            if self.style == 2:
                # mark up - shade negative, or if goes past max mark
                if delta <= 0 or delta + self.currentMark > self.maxMark:
                    flag = False
            elif self.style == 3:
                # mark down - shade positive, or if goes below 0
                if delta >= 0 or delta + self.currentMark < 0:
                    flag = False
        if flag:
            QItemDelegate.paint(self, painter, option, index)


class commentRowModel(QStandardItemModel):
    """Need to alter the standrd item model so that when we
    drag/drop to rearrange things, the whole row is moved,
    not just the item. Solution found at (and then tweaked)
    https://stackoverflow.com/questions/26227885/drag-and-drop-rows-within-qtablewidget/43789304#43789304
    """

    def setData(self, index, value, role=Qt.EditRole):
        """Simple validation of data in the row. Also convert
        an escaped '\n' into an actual newline for multiline
        comments.
        """
        # check that data in column zero is numeric
        if index.column() == 0:  # try to convert value to integer
            try:
                v = int(value)  # success! is number
                if v > 0:  # if it is positive, then make sure string is "+v"
                    value = "+{}".format(v)
                # otherwise the current value is "0" or "-n".
            except ValueError:
                value = "0"  # failed, so set to 0.
        # If its column 1 then convert '\n' into actual newline in the string
        elif index.column() == 1:
            value = value.replace("\\n", "\n")
        return super().setData(index, value, role)


class SimpleCommentTable(QTableView):
    """The comment table needs to signal the annotator to tell
    it what the current comment and delta are.
    Also needs to know the current/max mark and marking style
    in order to change the shading of the delta that goes with
    each comment.

    Dragdrop rows solution found at (and tweaked)
    https://stackoverflow.com/questions/26227885/drag-and-drop-rows-within-qtablewidget/43789304#43789304
    """

    # This is picked up by the annotator and tells is what is
    # the current comment and delta
    commentSignal = pyqtSignal(list)

    def __init__(self, parent):
        super(SimpleCommentTable, self).__init__()
        # No numbers down the left-side
        self.verticalHeader().hide()
        # The comment column should be as wide as possible
        self.horizontalHeader().setStretchLastSection(True)
        # Only select one row at a time.
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Drag and drop rows to reorder and also paste into pageview
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        # When clicked, the selection changes, so must emit signal
        # to the annotator.
        self.pressed.connect(self.handleClick)

        # Use the row model defined above, to allow newlines inside comments
        self.cmodel = commentRowModel()
        # self.cmodel = QStandardItemModel()
        self.cmodel.setHorizontalHeaderLabels(["delta", "comment"])
        self.setModel(self.cmodel)
        # When editor finishes make sure current row re-selected.
        self.cmodel.itemChanged.connect(self.handleClick)
        # Use the delegate defined above to shade deltas when needed
        self.delegate = commentDelegate()
        self.setItemDelegate(self.delegate)
        # A list of [delta, comment] pairs
        self.clist = []
        # Load in from file (if it exists) and populate table.
        self.loadCommentList()
        self.populateTable()
        self.resizeRowsToContents()
        self.resizeColumnToContents(0)
        # If an item is changed resize things appropriately.
        self.cmodel.itemChanged.connect(self.resizeRowsToContents)

        # set these so that double-click enables edits, but not keypress.
        self.setEditTriggers(
            QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked
        )

    def dropEvent(self, event: QDropEvent):
        # If drag and drop from self to self.
        if not event.isAccepted() and event.source() == self:
            # grab the row number of dragged row and its data
            row = self.selectedIndexes()[0].row()
            rowData = [
                self.cmodel.index(row, 0).data(),
                self.cmodel.index(row, 1).data(),
            ]
            # Get the row on which to drop
            dropRow = self.drop_on(event)
            # If we drag from earlier row, handle index after deletion
            if row < dropRow:
                dropRow -= 1
            # Delete the original row
            self.cmodel.removeRow(row)
            # Insert it at drop position
            self.cmodel.insertRow(
                dropRow, [QStandardItem(rowData[0]), QStandardItem(rowData[1])]
            )
            # Select the dropped row
            self.selectRow(dropRow)
            # Resize the rows - they were expanding after drags for some reason
            self.resizeRowsToContents()
        else:
            super().dropEvent(event)

    def drop_on(self, event):
        # Where is the drop event - which row
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.cmodel.rowCount()
        if self.isBelow(event.pos(), index):
            return index.row() + 1
        else:
            return index.row()

    def isBelow(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.y() < rect.top() + margin:
            return False
        elif rect.bottom() < pos.y() + margin:
            return True
        # noinspection PyTypeChecker
        return (
            rect.contains(pos, True)
            and not (int(self.model().flags(index)) & Qt.ItemIsDropEnabled)
            and pos.y() >= rect.center().y()
        )

    def populateTable(self):
        # Grab [delta, comment] from the list and put into table.
        for (dlt, txt) in self.clist:
            # User can edit the text, but doesn't handle drops.
            txti = QStandardItem(txt)
            txti.setEditable(True)
            txti.setDropEnabled(False)
            # If delta>0 then should be "+n"
            if int(dlt) > 0:
                delti = QStandardItem("+{}".format(int(dlt)))
            else:
                # is zero or negative - is "0" or "-n"
                delti = QStandardItem("{}".format(dlt))
            # User can edit the delta, but doesn't handle drops.
            delti.setEditable(True)
            delti.setDropEnabled(False)
            delti.setTextAlignment(Qt.AlignCenter)
            # Append it to the table.
            self.cmodel.appendRow([delti, txti])

    def handleClick(self, index=0):
        # When an item is clicked, grab the details and emit
        # the comment signal for the annotator to read.
        if index == 0:  # make sure something is selected
            self.currentItem()
        r = self.selectedIndexes()[0].row()
        self.commentSignal.emit(
            [self.cmodel.index(r, 0).data(), self.cmodel.index(r, 1).data()]
        )

    def loadCommentList(self):
        # grab comments from the json file,
        # if no file, then populate with some simple ones
        if os.path.exists("signedCommentList.json"):
            self.clist = json.load(open("signedCommentList.json"))
        else:
            self.clist = [
                (-1, "algebra"),
                (-1, "arithmetic"),
                (-1, "huh?"),
                (0, "be careful"),
                (1, "good"),
                (1, "very nice"),
                (1, "yes"),
            ]

    def saveCommentList(self):
        # grab comments from the table, populate a list
        # export to json file.
        self.clist = []
        for r in range(self.cmodel.rowCount()):
            self.clist.append(
                (self.cmodel.index(r, 0).data(), self.cmodel.index(r, 1).data())
            )
        with open("signedCommentList.json", "w") as fname:
            json.dump(self.clist, fname)

    def addItem(self):
        # Create a [delta, comment] pair for user to edit
        # and append to end of table.
        txti = QStandardItem("EDIT ME")
        txti.setEditable(True)
        txti.setDropEnabled(False)
        delti = QStandardItem("0")
        delti.setEditable(True)
        delti.setDropEnabled(False)
        delti.setTextAlignment(Qt.AlignCenter)
        self.cmodel.appendRow([delti, txti])
        # select the new row
        self.selectRow(self.cmodel.rowCount() - 1)
        # fire up editor on the comment which is second selected index
        self.edit(self.selectedIndexes()[1])

    def deleteItem(self):
        # Remove the selected row (or do nothing if no selection)
        sel = self.selectedIndexes()
        if len(sel) == 0:
            return
        self.cmodel.removeRow(sel[0].row())

    def currentItem(self):
        # If no selected row, then select row 0.
        # else select current row - triggers a signal.
        sel = self.selectedIndexes()
        if len(sel) == 0:
            self.selectRow(0)
        else:
            self.selectRow(sel[0].row())

    def nextItem(self):
        # Select next row (wraps around)
        sel = self.selectedIndexes()
        if len(sel) == 0:
            self.selectRow(0)
        else:
            self.selectRow((sel[0].row() + 1) % self.cmodel.rowCount())

    def previousItem(self):
        # Select previous row (wraps around)
        sel = self.selectedIndexes()
        if len(sel) == 0:
            self.selectRow(0)
        else:
            self.selectRow((sel[0].row() - 1) % self.cmodel.rowCount())