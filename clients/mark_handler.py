__author__ = "Andrew Rechnitzer"
__copyright__ = "Copyright (C) 2018-2019 Andrew Rechnitzer"
__credits__ = ["Andrew Rechnitzer", "Colin MacDonald", "Elvis Cai", "Matt Coles"]
__license__ = "GPLv3"

from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QGridLayout,
    QStackedWidget,
    QLabel,
    QSizePolicy,
)
from PyQt5.QtCore import pyqtSignal, Qt


class MarkHandler(QWidget):
    # When a mark or delta is set, these signals will be emitted.
    markSetSignal = pyqtSignal(int)
    deltaSetSignal = pyqtSignal(int)

    def __init__(self, maxScore):
        super(MarkHandler, self).__init__()
        # Set max score/mark
        self.maxScore = maxScore
        # Set current score/mark.
        self.currentScore = 0
        # One button for each possible mark, and a dictionary to store them.
        self.numButtons = self.maxScore
        self.markButtons = {}
        # Styling for buttons
        self.redStyle = (
            "border: 2px solid #ff0000; background: "
            "qlineargradient(x1:0,y1:0,x2:1,y2:0, stop: 0 #ff0000, "
            "stop: 0.3 #ffcccc, stop: 0.7 #ffcccc, stop: 1 #ff0000);"
        )
        self.greenStyle = (
            "border: 2px solid #00aaaa; background: "
            "qlineargradient(x1:0,y1:0,x2:0,y2:1, stop: 0 #00dddd, "
            "stop: 1 #00aaaa); "
        )
        # By default we set style to marking-UP.
        self.style = "Up"
        # Set up a current-score/mark label at top of widget.
        self.scoreL = QLabel("")
        fnt = self.scoreL.font()
        fnt.setPointSize(fnt.pointSize() * 2)
        self.scoreL.setFont(fnt)
        self.scoreL.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.scoreL.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )

    def setStyle(self, markStyle):
        """Sets the mark entry style - either total, up or down
        Total - user just clicks the total mark.
        Up - score starts at zero and increments.
        Down - score starts at max and decrements.
        """
        # if passed a marking style, then set up accordingly.
        if markStyle == 1:
            self.setMarkingTotal()
        elif markStyle == 3:
            self.setMarkingDown()
        else:
            # Default to mark-up.
            self.setMarkingUp()

    def setMarkingUp(self):
        self.setMark(0)
        grid = QGridLayout()
        self.pdmb = QPushButton()

        if self.numButtons > 5:
            ncolumn = 3
        else:
            ncolumn = 2

        grid.addWidget(self.scoreL, 0, 0, 1, 2)
        for k in range(0, self.numButtons + 1):
            self.markButtons["p{}".format(k)] = QPushButton("+&{}".format(k))
            grid.addWidget(
                self.markButtons["p{}".format(k)], k // ncolumn + 1, k % ncolumn, 1, 1
            )
            self.markButtons["p{}".format(k)].clicked.connect(self.setDeltaMark)
            self.markButtons["p{}".format(k)].setSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            )

        self.setLayout(grid)
        self.style = "Up"

    def setMarkingDown(self):
        self.setMark(self.maxScore)
        grid = QGridLayout()
        self.pdmb = QPushButton()

        if self.numButtons > 5:
            ncolumn = 3
        else:
            ncolumn = 2

        grid.addWidget(self.scoreL, 0, 0, 1, 2)
        for k in range(1, self.numButtons + 1):
            self.markButtons["m{}".format(k)] = QPushButton("-&{}".format(k))
            grid.addWidget(
                self.markButtons["m{}".format(k)], k // ncolumn + 1, k % ncolumn, 1, 1
            )
            self.markButtons["m{}".format(k)].clicked.connect(self.setDeltaMark)
            self.markButtons["m{}".format(k)].setSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            )

        self.setLayout(grid)
        self.markSetSignal.emit(self.currentScore)
        self.style = "Down"

    def setMarkingTotal(self):
        grid = QGridLayout()
        self.ptmb = QPushButton()

        if self.maxScore > 5:
            ncolumn = 3
        else:
            ncolumn = 2

        for k in range(0, self.maxScore + 1):
            self.markButtons["{}".format(k)] = QPushButton("&{}".format(k))
            grid.addWidget(self.markButtons["{}".format(k)], k // ncolumn, k % ncolumn)
            self.markButtons["{}".format(k)].clicked.connect(self.setTotalMark)
            self.markButtons["{}".format(k)].setSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            )

        self.setLayout(grid)
        self.markSetSignal.emit(self.currentScore)
        self.style = "Total"

    def setDeltaMark(self):
        self.pdmb.setStyleSheet("")
        self.pdmb = self.sender()
        self.pdmb.setStyleSheet(self.greenStyle)
        self.currentDelta = int(self.sender().text().replace("&", ""))
        self.deltaSetSignal.emit(self.currentDelta)

    def setTotalMark(self):
        self.ptmb.setStyleSheet("")
        self.ptmb = self.sender()
        self.ptmb.setStyleSheet(self.redStyle)
        self.currentScore = int(self.sender().text().replace("&", ""))
        self.markSetSignal.emit(self.currentScore)

    def setMark(self, newScore):
        self.currentScore = newScore
        self.scoreL.setText("{} / {}".format(self.currentScore, self.maxScore))
        self.markSetSignal.emit(self.currentScore)

    def clearButtonStyle(self):
        if self.style == "Total":
            pass  # don't clear the styling when marking total.
        else:
            self.pdmb.setStyleSheet("")