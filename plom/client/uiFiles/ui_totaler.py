# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../qtCreatorFiles/ui_totaler.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TotalWindow(object):
    def setupUi(self, TotalWindow):
        TotalWindow.setObjectName("TotalWindow")
        TotalWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        TotalWindow.resize(1062, 660)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(TotalWindow.sizePolicy().hasHeightForWidth())
        TotalWindow.setSizePolicy(sizePolicy)
        TotalWindow.setBaseSize(QtCore.QSize(0, 0))
        self.gridLayout_5 = QtWidgets.QGridLayout(TotalWindow)
        self.gridLayout_5.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeButton = QtWidgets.QPushButton(TotalWindow)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.gridLayout_5.addLayout(self.horizontalLayout, 4, 0, 1, 1)
        self.widget_2 = QtWidgets.QWidget(TotalWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.paperBox = QtWidgets.QGroupBox(self.widget_2)
        self.paperBox.setObjectName("paperBox")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.paperBox)
        self.gridLayout_7.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_4.addWidget(self.paperBox, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.widget_2, 0, 1, 5, 1)
        self.widget = QtWidgets.QWidget(TotalWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.totalBox = QtWidgets.QGroupBox(self.widget)
        self.totalBox.setObjectName("totalBox")
        self.formLayout = QtWidgets.QFormLayout(self.totalBox)
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setObjectName("formLayout")
        self.markLabel = QtWidgets.QLabel(self.totalBox)
        self.markLabel.setObjectName("markLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.markLabel)
        self.totalEdit = QtWidgets.QLineEdit(self.totalBox)
        self.totalEdit.setObjectName("totalEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.totalEdit)
        self.gridLayout_3.addWidget(self.totalBox, 2, 0, 1, 1)
        self.nextButton = QtWidgets.QPushButton(self.widget)
        self.nextButton.setObjectName("nextButton")
        self.gridLayout_3.addWidget(self.nextButton, 3, 0, 1, 1)
        self.userBox = QtWidgets.QGroupBox(self.widget)
        self.userBox.setObjectName("userBox")
        self.gridLayout = QtWidgets.QGridLayout(self.userBox)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.userLabel = QtWidgets.QLabel(self.userBox)
        self.userLabel.setObjectName("userLabel")
        self.gridLayout.addWidget(self.userLabel, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.userBox, 0, 0, 1, 1)
        self.tableBox = QtWidgets.QGroupBox(self.widget)
        self.tableBox.setObjectName("tableBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tableBox)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableView = QtWidgets.QTableView(self.tableBox)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.gridLayout_2.addWidget(self.tableView, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.tableBox, 4, 0, 1, 1)
        self.gridLayout_5.addWidget(self.widget, 0, 0, 1, 1)
        self.progressGroupBox = QtWidgets.QGroupBox(TotalWindow)
        self.progressGroupBox.setObjectName("progressGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.progressGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.idProgressBar = QtWidgets.QProgressBar(self.progressGroupBox)
        self.idProgressBar.setMaximum(1)
        self.idProgressBar.setProperty("value", 0)
        self.idProgressBar.setObjectName("idProgressBar")
        self.verticalLayout.addWidget(self.idProgressBar)
        self.gridLayout_5.addWidget(self.progressGroupBox, 1, 0, 1, 1)

        self.retranslateUi(TotalWindow)
        QtCore.QMetaObject.connectSlotsByName(TotalWindow)
        TotalWindow.setTabOrder(self.totalEdit, self.tableView)
        TotalWindow.setTabOrder(self.tableView, self.nextButton)
        TotalWindow.setTabOrder(self.nextButton, self.closeButton)

    def retranslateUi(self, TotalWindow):
        _translate = QtCore.QCoreApplication.translate
        TotalWindow.setWindowTitle(_translate("TotalWindow", "Enter total mark"))
        self.closeButton.setText(_translate("TotalWindow", "&Close"))
        self.paperBox.setTitle(_translate("TotalWindow", "Current paper"))
        self.totalBox.setTitle(_translate("TotalWindow", "Enter total out of "))
        self.markLabel.setText(_translate("TotalWindow", "Total"))
        self.nextButton.setText(_translate("TotalWindow", "&Get next"))
        self.userBox.setTitle(_translate("TotalWindow", "User"))
        self.userLabel.setText(_translate("TotalWindow", "Username"))
        self.tableBox.setTitle(_translate("TotalWindow", "Table of papers"))
        self.progressGroupBox.setTitle(_translate("TotalWindow", "Progress"))
        self.idProgressBar.setFormat(_translate("TotalWindow", "%v of %m"))

