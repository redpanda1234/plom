# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtCreatorFiles/ui_marker.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MarkerWindow(object):
    def setupUi(self, MarkerWindow):
        MarkerWindow.setObjectName("MarkerWindow")
        MarkerWindow.setWindowModality(QtCore.Qt.WindowModal)
        MarkerWindow.resize(1024, 768)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(MarkerWindow)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(MarkerWindow)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.infoBox = QtWidgets.QGroupBox(self.frame)
        self.infoBox.setObjectName("infoBox")
        self.formLayout_2 = QtWidgets.QFormLayout(self.infoBox)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtWidgets.QLabel(self.infoBox)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.userLabel = QtWidgets.QLabel(self.infoBox)
        self.userLabel.setText("<username>")
        self.userLabel.setObjectName("userLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.userLabel)
        self.label_5 = QtWidgets.QLabel(self.infoBox)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.maxscoreLabel = QtWidgets.QLabel(self.infoBox)
        self.maxscoreLabel.setText("<number>")
        self.maxscoreLabel.setObjectName("maxscoreLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.maxscoreLabel)
        self.verticalLayout.addWidget(self.infoBox)
        self.tableBox = QtWidgets.QGroupBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tableBox.sizePolicy().hasHeightForWidth())
        self.tableBox.setSizePolicy(sizePolicy)
        self.tableBox.setObjectName("tableBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tableBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableView = SimpleTableView(self.tableBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setMinimumSize(QtCore.QSize(250, 0))
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_2.addWidget(self.tableView)
        self.frame1 = QtWidgets.QFrame(self.tableBox)
        self.frame1.setObjectName("frame1")
        self.gridLayout = QtWidgets.QGridLayout(self.frame1)
        self.gridLayout.setContentsMargins(0, 1, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.annButton = QtWidgets.QPushButton(self.frame1)
        self.annButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.annButton.setObjectName("annButton")
        self.gridLayout.addWidget(self.annButton, 0, 0, 1, 2)
        self.getNextButton = QtWidgets.QPushButton(self.frame1)
        self.getNextButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.getNextButton.setObjectName("getNextButton")
        self.gridLayout.addWidget(self.getNextButton, 0, 2, 1, 1)
        self.deferButton = QtWidgets.QPushButton(self.frame1)
        self.deferButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.deferButton.setObjectName("deferButton")
        self.gridLayout.addWidget(self.deferButton, 1, 0, 1, 1)
        self.tagButton = QtWidgets.QPushButton(self.frame1)
        self.tagButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tagButton.setObjectName("tagButton")
        self.gridLayout.addWidget(self.tagButton, 1, 1, 1, 1)
        self.viewButton = QtWidgets.QPushButton(self.frame1)
        self.viewButton.setObjectName("viewButton")
        self.gridLayout.addWidget(self.viewButton, 1, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.frame1)
        self.frame2 = QtWidgets.QFrame(self.tableBox)
        self.frame2.setObjectName("frame2")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.frame2)
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.filterButton = QtWidgets.QPushButton(self.frame2)
        self.filterButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.filterButton.setObjectName("filterButton")
        self.horizontalLayout_21.addWidget(self.filterButton)
        self.filterInvCB = QtWidgets.QCheckBox(self.frame2)
        self.filterInvCB.setObjectName("filterInvCB")
        self.horizontalLayout_21.addWidget(self.filterInvCB)
        self.filterLE = QtWidgets.QLineEdit(self.frame2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterLE.sizePolicy().hasHeightForWidth())
        self.filterLE.setSizePolicy(sizePolicy)
        self.filterLE.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.filterLE.setMaxLength(256)
        self.filterLE.setClearButtonEnabled(True)
        self.filterLE.setObjectName("filterLE")
        self.horizontalLayout_21.addWidget(self.filterLE)
        self.verticalLayout_2.addWidget(self.frame2)
        self.verticalLayout.addWidget(self.tableBox)
        self.styleChoiceBox = QtWidgets.QGroupBox(self.frame)
        self.styleChoiceBox.setObjectName("styleChoiceBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.styleChoiceBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.markUpRB = QtWidgets.QRadioButton(self.styleChoiceBox)
        self.markUpRB.setChecked(True)
        self.markUpRB.setObjectName("markUpRB")
        self.markStyleGroup = QtWidgets.QButtonGroup(MarkerWindow)
        self.markStyleGroup.setObjectName("markStyleGroup")
        self.markStyleGroup.addButton(self.markUpRB)
        self.horizontalLayout_4.addWidget(self.markUpRB)
        self.markDownRB = QtWidgets.QRadioButton(self.styleChoiceBox)
        self.markDownRB.setChecked(False)
        self.markDownRB.setObjectName("markDownRB")
        self.markStyleGroup.addButton(self.markDownRB)
        self.horizontalLayout_4.addWidget(self.markDownRB)
        self.markTotalRB = QtWidgets.QRadioButton(self.styleChoiceBox)
        self.markTotalRB.setObjectName("markTotalRB")
        self.markStyleGroup.addButton(self.markTotalRB)
        self.horizontalLayout_4.addWidget(self.markTotalRB)
        self.verticalLayout.addWidget(self.styleChoiceBox)
        self.OptionsBox = QtWidgets.QGroupBox(self.frame)
        self.OptionsBox.setObjectName("OptionsBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.OptionsBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.leftMouseCB = QtWidgets.QCheckBox(self.OptionsBox)
        self.leftMouseCB.setObjectName("leftMouseCB")
        self.verticalLayout_3.addWidget(self.leftMouseCB)
        self.sidebarRightCB = QtWidgets.QCheckBox(self.OptionsBox)
        self.sidebarRightCB.setObjectName("sidebarRightCB")
        self.verticalLayout_3.addWidget(self.sidebarRightCB)
        self.verticalLayout.addWidget(self.OptionsBox)
        self.frameProgress = QtWidgets.QFrame(self.frame)
        self.frameProgress.setObjectName("frameProgress")
        self.layoutProgress = QtWidgets.QHBoxLayout(self.frameProgress)
        self.layoutProgress.setContentsMargins(0, -1, 0, -1)
        self.layoutProgress.setObjectName("layoutProgress")
        self.labelProgress = QtWidgets.QLabel(self.frameProgress)
        self.labelProgress.setObjectName("labelProgress")
        self.layoutProgress.addWidget(self.labelProgress)
        self.mProgressBar = QtWidgets.QProgressBar(self.frameProgress)
        self.mProgressBar.setProperty("value", 1)
        self.mProgressBar.setObjectName("mProgressBar")
        self.layoutProgress.addWidget(self.mProgressBar)
        self.verticalLayout.addWidget(self.frameProgress)
        self.frameClose = QtWidgets.QFrame(self.frame)
        self.frameClose.setObjectName("frameClose")
        self.layoutClose = QtWidgets.QHBoxLayout(self.frameClose)
        self.layoutClose.setContentsMargins(0, 0, 0, 0)
        self.layoutClose.setObjectName("layoutClose")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layoutClose.addItem(spacerItem)
        self.closeButton = QtWidgets.QPushButton(self.frameClose)
        self.closeButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.closeButton.setObjectName("closeButton")
        self.layoutClose.addWidget(self.closeButton)
        self.verticalLayout.addWidget(self.frameClose)
        self.horizontalLayout_2.addWidget(self.frame)
        self.paperBox = QtWidgets.QGroupBox(MarkerWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.paperBox.sizePolicy().hasHeightForWidth())
        self.paperBox.setSizePolicy(sizePolicy)
        self.paperBox.setObjectName("paperBox")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.paperBox)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.horizontalLayout_2.addWidget(self.paperBox)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)

        self.retranslateUi(MarkerWindow)
        QtCore.QMetaObject.connectSlotsByName(MarkerWindow)
        MarkerWindow.setTabOrder(self.tableView, self.closeButton)

    def retranslateUi(self, MarkerWindow):
        _translate = QtCore.QCoreApplication.translate
        MarkerWindow.setWindowTitle(_translate("MarkerWindow", "Mark papers"))
        self.infoBox.setTitle(_translate("MarkerWindow", "Question Info"))
        self.label_2.setText(_translate("MarkerWindow", "Username "))
        self.label_5.setText(_translate("MarkerWindow", "Max score"))
        self.tableBox.setTitle(_translate("MarkerWindow", "Paper list"))
        self.annButton.setText(_translate("MarkerWindow", "&Annotate && mark"))
        self.getNextButton.setText(_translate("MarkerWindow", "&Get next"))
        self.deferButton.setText(_translate("MarkerWindow", "Defer"))
        self.tagButton.setText(_translate("MarkerWindow", "Tag"))
        self.viewButton.setText(_translate("MarkerWindow", "View"))
        self.filterButton.setText(_translate("MarkerWindow", "Filter"))
        self.filterInvCB.setText(_translate("MarkerWindow", "Inv"))
        self.filterLE.setPlaceholderText(_translate("MarkerWindow", "Filter on tag text"))
        self.styleChoiceBox.setTitle(_translate("MarkerWindow", "Marking style"))
        self.markUpRB.setText(_translate("MarkerWindow", "Mark &Up"))
        self.markDownRB.setText(_translate("MarkerWindow", "Mark &Down"))
        self.markTotalRB.setText(_translate("MarkerWindow", "&Total"))
        self.OptionsBox.setTitle(_translate("MarkerWindow", "Options"))
        self.leftMouseCB.setToolTip(_translate("MarkerWindow", "Move keyboard shortcuts to right hand"))
        self.leftMouseCB.setText(_translate("MarkerWindow", "&Left-handed mouse"))
        self.sidebarRightCB.setText(_translate("MarkerWindow", "&Sidebar on right"))
        self.labelProgress.setText(_translate("MarkerWindow", "Progress:"))
        self.mProgressBar.setFormat(_translate("MarkerWindow", "%v of %m"))
        self.closeButton.setText(_translate("MarkerWindow", "&Close"))
        self.paperBox.setTitle(_translate("MarkerWindow", "Current paper"))
from plom.client.useful_classes import SimpleTableView
