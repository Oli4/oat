# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_data_navigation_dock.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dataNavigationDock(object):
    def setupUi(self, dataNavigationDock):
        dataNavigationDock.setObjectName("dataNavigationDock")
        dataNavigationDock.resize(350, 432)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dataNavigationDock.sizePolicy().hasHeightForWidth())
        dataNavigationDock.setSizePolicy(sizePolicy)
        dataNavigationDock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        dataNavigationDock.setWindowTitle("")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setMinimumSize(QtCore.QSize(350, 200))
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableView = QtWidgets.QTableView(self.dockWidgetContents)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout.addWidget(self.tableView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.registerButton = QtWidgets.QPushButton(self.dockWidgetContents)
        self.registerButton.setObjectName("registerButton")
        self.verticalLayout.addWidget(self.registerButton)
        self.annotateButton = QtWidgets.QPushButton(self.dockWidgetContents)
        self.annotateButton.setObjectName("annotateButton")
        self.verticalLayout.addWidget(self.annotateButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        dataNavigationDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(dataNavigationDock)
        QtCore.QMetaObject.connectSlotsByName(dataNavigationDock)

    def retranslateUi(self, dataNavigationDock):
        _translate = QtCore.QCoreApplication.translate
        self.registerButton.setText(_translate("dataNavigationDock", "Register"))
        self.annotateButton.setText(_translate("dataNavigationDock", "Annotate"))


