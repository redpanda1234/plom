# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../qtCreatorFiles/ui_annotator_lefthandmouse.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_annotator_lhm(object):
    def setupUi(self, annotator_lhm):
        annotator_lhm.setObjectName("annotator_lhm")
        annotator_lhm.setWindowModality(QtCore.Qt.WindowModal)
        annotator_lhm.resize(862, 670)
        self.gridLayout = QtWidgets.QGridLayout(annotator_lhm)
        self.gridLayout.setObjectName("gridLayout")
        self.pageFrame = QtWidgets.QFrame(annotator_lhm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageFrame.sizePolicy().hasHeightForWidth())
        self.pageFrame.setSizePolicy(sizePolicy)
        self.pageFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pageFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pageFrame.setObjectName("pageFrame")
        self.pageFrameGrid = QtWidgets.QGridLayout(self.pageFrame)
        self.pageFrameGrid.setContentsMargins(3, 3, 3, 3)
        self.pageFrameGrid.setObjectName("pageFrameGrid")
        self.gridLayout.addWidget(self.pageFrame, 0, 0, 5, 1)
        self.hideableBox = QtWidgets.QFrame(annotator_lhm)
        self.hideableBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hideableBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hideableBox.setObjectName("hideableBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.hideableBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.hideableBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame = QtWidgets.QFrame(self.groupBox)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 1, 0, 1, 1)
        self.keyHelpButton = QtWidgets.QPushButton(self.frame)
        self.keyHelpButton.setObjectName("keyHelpButton")
        self.gridLayout_4.addWidget(self.keyHelpButton, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 1, 2, 1, 1)
        self.toolLineEdit = QtWidgets.QLineEdit(self.frame)
        self.toolLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.toolLineEdit.setReadOnly(True)
        self.toolLineEdit.setObjectName("toolLineEdit")
        self.gridLayout_4.addWidget(self.toolLineEdit, 0, 0, 1, 3)
        self.gridLayout_3.addWidget(self.frame, 3, 0, 1, 5)
        self.textButton = QtWidgets.QToolButton(self.groupBox)
        self.textButton.setObjectName("textButton")
        self.gridLayout_3.addWidget(self.textButton, 1, 0, 1, 1)
        self.undoButton = QtWidgets.QToolButton(self.groupBox)
        self.undoButton.setObjectName("undoButton")
        self.gridLayout_3.addWidget(self.undoButton, 1, 3, 1, 1)
        self.tickButton = QtWidgets.QToolButton(self.groupBox)
        self.tickButton.setToolTipDuration(-1)
        self.tickButton.setObjectName("tickButton")
        self.gridLayout_3.addWidget(self.tickButton, 1, 2, 1, 1)
        self.panButton = QtWidgets.QToolButton(self.groupBox)
        self.panButton.setObjectName("panButton")
        self.gridLayout_3.addWidget(self.panButton, 0, 4, 1, 1)
        self.boxButton = QtWidgets.QToolButton(self.groupBox)
        self.boxButton.setObjectName("boxButton")
        self.gridLayout_3.addWidget(self.boxButton, 2, 2, 1, 1)
        self.zoomButton = QtWidgets.QToolButton(self.groupBox)
        self.zoomButton.setObjectName("zoomButton")
        self.gridLayout_3.addWidget(self.zoomButton, 1, 4, 1, 1)
        self.moveButton = QtWidgets.QToolButton(self.groupBox)
        self.moveButton.setObjectName("moveButton")
        self.gridLayout_3.addWidget(self.moveButton, 2, 4, 1, 1)
        self.deleteButton = QtWidgets.QToolButton(self.groupBox)
        self.deleteButton.setObjectName("deleteButton")
        self.gridLayout_3.addWidget(self.deleteButton, 2, 3, 1, 1)
        self.commentDownButton = QtWidgets.QToolButton(self.groupBox)
        self.commentDownButton.setToolTipDuration(-1)
        self.commentDownButton.setObjectName("commentDownButton")
        self.gridLayout_3.addWidget(self.commentDownButton, 2, 1, 1, 1)
        self.commentButton = QtWidgets.QToolButton(self.groupBox)
        self.commentButton.setToolTipDuration(-1)
        self.commentButton.setObjectName("commentButton")
        self.gridLayout_3.addWidget(self.commentButton, 1, 1, 1, 1)
        self.crossButton = QtWidgets.QToolButton(self.groupBox)
        self.crossButton.setObjectName("crossButton")
        self.gridLayout_3.addWidget(self.crossButton, 0, 2, 1, 1)
        self.redoButton = QtWidgets.QToolButton(self.groupBox)
        self.redoButton.setObjectName("redoButton")
        self.gridLayout_3.addWidget(self.redoButton, 0, 3, 1, 1)
        self.lineButton = QtWidgets.QToolButton(self.groupBox)
        self.lineButton.setObjectName("lineButton")
        self.gridLayout_3.addWidget(self.lineButton, 2, 0, 1, 1)
        self.penButton = QtWidgets.QToolButton(self.groupBox)
        self.penButton.setObjectName("penButton")
        self.gridLayout_3.addWidget(self.penButton, 0, 0, 1, 1)
        self.commentUpButton = QtWidgets.QToolButton(self.groupBox)
        self.commentUpButton.setToolTipDuration(-1)
        self.commentUpButton.setObjectName("commentUpButton")
        self.gridLayout_3.addWidget(self.commentUpButton, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.markBox = QtWidgets.QGroupBox(self.hideableBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.markBox.sizePolicy().hasHeightForWidth())
        self.markBox.setSizePolicy(sizePolicy)
        self.markBox.setObjectName("markBox")
        self.markGrid = QtWidgets.QGridLayout(self.markBox)
        self.markGrid.setContentsMargins(3, 3, 3, 3)
        self.markGrid.setSpacing(3)
        self.markGrid.setObjectName("markGrid")
        self.verticalLayout.addWidget(self.markBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.hideableBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.commentGrid = QtWidgets.QGridLayout(self.groupBox_3)
        self.commentGrid.setContentsMargins(3, 3, 3, 3)
        self.commentGrid.setSpacing(3)
        self.commentGrid.setObjectName("commentGrid")
        self.verticalLayout.addWidget(self.groupBox_3)
        self.frame_2 = QtWidgets.QFrame(self.hideableBox)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.finishedButton = QtWidgets.QPushButton(self.frame_2)
        self.finishedButton.setObjectName("finishedButton")
        self.gridLayout_2.addWidget(self.finishedButton, 0, 0, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(self.frame_2)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout_2.addWidget(self.cancelButton, 0, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 1, 1, 1)
        self.finishNoRelaunchButton = QtWidgets.QPushButton(self.frame_2)
        self.finishNoRelaunchButton.setObjectName("finishNoRelaunchButton")
        self.gridLayout_2.addWidget(self.finishNoRelaunchButton, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 0, 3, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)
        self.gridLayout.addWidget(self.hideableBox, 1, 1, 4, 1)
        self.hideButton = QtWidgets.QPushButton(annotator_lhm)
        self.hideButton.setObjectName("hideButton")
        self.gridLayout.addWidget(self.hideButton, 0, 1, 1, 1)

        self.retranslateUi(annotator_lhm)
        QtCore.QMetaObject.connectSlotsByName(annotator_lhm)
        annotator_lhm.setTabOrder(self.finishedButton, self.cancelButton)

    def retranslateUi(self, annotator_lhm):
        _translate = QtCore.QCoreApplication.translate
        annotator_lhm.setWindowTitle(_translate("annotator_lhm", "Annotate paper"))
        self.groupBox.setTitle(_translate("annotator_lhm", "Tools"))
        self.keyHelpButton.setText(_translate("annotator_lhm", "Key Help"))
        self.textButton.setToolTip(_translate("annotator_lhm", "press h"))
        self.textButton.setText(_translate("annotator_lhm", "..."))
        self.undoButton.setToolTip(_translate("annotator_lhm", "press l"))
        self.undoButton.setText(_translate("annotator_lhm", "..."))
        self.tickButton.setToolTip(_translate("annotator_lhm", "press k"))
        self.tickButton.setText(_translate("annotator_lhm", "..."))
        self.panButton.setToolTip(_translate("annotator_lhm", "press p"))
        self.panButton.setText(_translate("annotator_lhm", "..."))
        self.boxButton.setToolTip(_translate("annotator_lhm", "press comma"))
        self.boxButton.setText(_translate("annotator_lhm", "..."))
        self.zoomButton.setToolTip(_translate("annotator_lhm", "press semi-colon"))
        self.zoomButton.setText(_translate("annotator_lhm", "..."))
        self.moveButton.setToolTip(_translate("annotator_lhm", "press /"))
        self.moveButton.setText(_translate("annotator_lhm", "..."))
        self.deleteButton.setToolTip(_translate("annotator_lhm", "press period"))
        self.deleteButton.setText(_translate("annotator_lhm", "..."))
        self.commentDownButton.setToolTip(_translate("annotator_lhm", "press m"))
        self.commentDownButton.setText(_translate("annotator_lhm", "..."))
        self.commentButton.setToolTip(_translate("annotator_lhm", "press j"))
        self.commentButton.setText(_translate("annotator_lhm", "..."))
        self.crossButton.setToolTip(_translate("annotator_lhm", "press i"))
        self.crossButton.setText(_translate("annotator_lhm", "..."))
        self.redoButton.setToolTip(_translate("annotator_lhm", "press o"))
        self.redoButton.setText(_translate("annotator_lhm", "..."))
        self.lineButton.setToolTip(_translate("annotator_lhm", "press n"))
        self.lineButton.setText(_translate("annotator_lhm", "..."))
        self.penButton.setToolTip(_translate("annotator_lhm", "press y"))
        self.penButton.setText(_translate("annotator_lhm", "..."))
        self.commentUpButton.setToolTip(_translate("annotator_lhm", "press u"))
        self.commentUpButton.setText(_translate("annotator_lhm", "..."))
        self.markBox.setTitle(_translate("annotator_lhm", "Enter Mark"))
        self.groupBox_3.setTitle(_translate("annotator_lhm", "Comment list"))
        self.finishedButton.setText(_translate("annotator_lhm", "End && \n"
" Next"))
        self.cancelButton.setText(_translate("annotator_lhm", "&Cancel"))
        self.finishNoRelaunchButton.setText(_translate("annotator_lhm", "End && \n"
" Return"))
        self.hideButton.setText(_translate("annotator_lhm", "Hide"))
