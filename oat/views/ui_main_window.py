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
        MainWindow.resize(836, 613)
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
        self.action2D_Viewr = QtWidgets.QAction(MainWindow)
        self.action2D_Viewr.setCheckable(True)
        self.action2D_Viewr.setChecked(False)
        self.action2D_Viewr.setEnabled(True)
        self.action2D_Viewr.setObjectName("action2D_Viewr")
        self.action3D_Viewer = QtWidgets.QAction(MainWindow)
        self.action3D_Viewer.setCheckable(True)
        self.action3D_Viewer.setObjectName("action3D_Viewer")
        self.actionToolbox = QtWidgets.QAction(MainWindow)
        self.actionToolbox.setCheckable(True)
        self.actionToolbox.setObjectName("actionToolbox")
        self.menuImport.addAction(self.action_vol)
        self.menuFile.addAction(self.actionOpen_Project)
        self.menuFile.addAction(self.menuImport.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionSave)
        self.menuWindows.addAction(self.action2D_Viewr)
        self.menuWindows.addAction(self.action3D_Viewer)
        self.menuWindows.addAction(self.actionToolbox)
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
        self.action2D_Viewr.setText(_translate("MainWindow", "2D Viewer"))
        self.action3D_Viewer.setText(_translate("MainWindow", "3D Viewer"))
        self.actionToolbox.setText(_translate("MainWindow", "Toolbox"))


