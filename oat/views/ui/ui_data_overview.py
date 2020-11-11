# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_data_overview.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_OverviewView(object):
    def setupUi(self, OverviewView):
        OverviewView.setObjectName("OverviewView")
        OverviewView.resize(350, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OverviewView.sizePolicy().hasHeightForWidth())
        OverviewView.setSizePolicy(sizePolicy)
        OverviewView.setMinimumSize(QtCore.QSize(350, 500))
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(OverviewView)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tableView = QtWidgets.QTableView(OverviewView)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout_4.addWidget(self.tableView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.registerButton = QtWidgets.QPushButton(OverviewView)
        self.registerButton.setObjectName("registerButton")
        self.verticalLayout.addWidget(self.registerButton)
        self.annotateButton = QtWidgets.QPushButton(OverviewView)
        self.annotateButton.setObjectName("annotateButton")
        self.verticalLayout.addWidget(self.annotateButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.retranslateUi(OverviewView)
        QtCore.QMetaObject.connectSlotsByName(OverviewView)

    def retranslateUi(self, OverviewView):
        _translate = QtCore.QCoreApplication.translate
        OverviewView.setWindowTitle(_translate("OverviewView", "Form"))
        self.registerButton.setText(_translate("OverviewView", "Register"))
        self.annotateButton.setText(_translate("OverviewView", "Annotate"))
