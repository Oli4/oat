# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(836, 637)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName("mdiArea")
        self.verticalLayout.addWidget(self.mdiArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 836, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuImport = QtWidgets.QMenu(self.menuFile)
        self.menuImport.setObjectName("menuImport")
        self.menuWindows = QtWidgets.QMenu(self.menubar)
        self.menuWindows.setObjectName("menuWindows")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionOpen_Project = QtWidgets.QAction(MainWindow)
        self.actionOpen_Project.setObjectName("actionOpen_Project")
        self.action_vol = QtWidgets.QAction(MainWindow)
        self.action_vol.setEnabled(True)
        self.action_vol.setObjectName("action_vol")
        self.actionToggle2D = QtWidgets.QAction(MainWindow)
        self.actionToggle2D.setCheckable(True)
        self.actionToggle2D.setChecked(True)
        self.actionToggle2D.setEnabled(True)
        self.actionToggle2D.setObjectName("actionToggle2D")
        self.actionToggle3D = QtWidgets.QAction(MainWindow)
        self.actionToggle3D.setCheckable(True)
        self.actionToggle3D.setChecked(True)
        self.actionToggle3D.setObjectName("actionToggle3D")
        self.actionToogleToolbox = QtWidgets.QAction(MainWindow)
        self.actionToogleToolbox.setCheckable(True)
        self.actionToogleToolbox.setChecked(True)
        self.actionToogleToolbox.setObjectName("actionToogleToolbox")
        self.menuImport.addAction(self.action_vol)
        self.menuFile.addAction(self.actionOpen_Project)
        self.menuFile.addAction(self.menuImport.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionSave)
        self.menuWindows.addAction(self.actionToggle2D)
        self.menuWindows.addAction(self.actionToggle3D)
        self.menuWindows.addAction(self.actionToogleToolbox)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuWindows.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuImport.setTitle(_translate("MainWindow", "Import"))
        self.menuWindows.setTitle(_translate("MainWindow", "Windows"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionOpen_Project.setText(_translate("MainWindow", "Open Project"))
        self.action_vol.setText(_translate("MainWindow", ".vol (HE raw Export)"))
        self.actionToggle2D.setText(_translate("MainWindow", "2D Viewer"))
        self.actionToggle3D.setText(_translate("MainWindow", "3D Viewer"))
        self.actionToogleToolbox.setText(_translate("MainWindow", "Toolbox"))


