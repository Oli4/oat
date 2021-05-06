# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_data_navigation_dock.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from  . import resources_rc

class Ui_dataNavigationDock(object):
    def setupUi(self, dataNavigationDock):
        if not dataNavigationDock.objectName():
            dataNavigationDock.setObjectName(u"dataNavigationDock")
        dataNavigationDock.resize(350, 432)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dataNavigationDock.sizePolicy().hasHeightForWidth())
        dataNavigationDock.setSizePolicy(sizePolicy)
        dataNavigationDock.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.dockWidgetContents.setMinimumSize(QSize(350, 200))
        self.verticalLayout_2 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.dockWidgetContents)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.datasetComboBox = QComboBox(self.dockWidgetContents)
        self.datasetComboBox.setObjectName(u"datasetComboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.datasetComboBox)


        self.horizontalLayout.addLayout(self.formLayout)

        self.toolButton = QToolButton(self.dockWidgetContents)
        self.toolButton.setObjectName(u"toolButton")
        icon = QIcon()
        icon.addFile(u":/icons/icons/baseline-add_circle-24px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.toolButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tableView = QTableView(self.dockWidgetContents)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_3.addWidget(self.tableView)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.addButton = QToolButton(self.dockWidgetContents)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setIcon(icon)
        self.addButton.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.addButton)

        self.deleteButton = QToolButton(self.dockWidgetContents)
        self.deleteButton.setObjectName(u"deleteButton")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/baseline-delete-24px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.deleteButton.setIcon(icon1)
        self.deleteButton.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.deleteButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.registerButton = QPushButton(self.dockWidgetContents)
        self.registerButton.setObjectName(u"registerButton")

        self.verticalLayout.addWidget(self.registerButton)

        self.annotateButton = QPushButton(self.dockWidgetContents)
        self.annotateButton.setObjectName(u"annotateButton")

        self.verticalLayout.addWidget(self.annotateButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        dataNavigationDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(dataNavigationDock)

        QMetaObject.connectSlotsByName(dataNavigationDock)
    # setupUi

    def retranslateUi(self, dataNavigationDock):
        dataNavigationDock.setWindowTitle("")
        self.label.setText(QCoreApplication.translate("dataNavigationDock", u"Dataset:", None))
        self.toolButton.setText(QCoreApplication.translate("dataNavigationDock", u"...", None))
        self.addButton.setText(QCoreApplication.translate("dataNavigationDock", u"...", None))
        self.deleteButton.setText(QCoreApplication.translate("dataNavigationDock", u"...", None))
        self.registerButton.setText(QCoreApplication.translate("dataNavigationDock", u"Register", None))
        self.annotateButton.setText(QCoreApplication.translate("dataNavigationDock", u"Annotate", None))
    # retranslateUi

