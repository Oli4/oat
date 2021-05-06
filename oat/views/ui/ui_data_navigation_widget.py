# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_data_navigation_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from  . import resources_rc

class Ui_dataNavigationWidget(object):
    def setupUi(self, dataNavigationWidget):
        if not dataNavigationWidget.objectName():
            dataNavigationWidget.setObjectName(u"dataNavigationWidget")
        dataNavigationWidget.resize(350, 500)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dataNavigationWidget.sizePolicy().hasHeightForWidth())
        dataNavigationWidget.setSizePolicy(sizePolicy)
        dataNavigationWidget.setMinimumSize(QSize(350, 500))
        self.horizontalLayout_4 = QHBoxLayout(dataNavigationWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.tableView = QTableView(dataNavigationWidget)
        self.tableView.setObjectName(u"tableView")

        self.horizontalLayout_4.addWidget(self.tableView)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.registerButton = QPushButton(dataNavigationWidget)
        self.registerButton.setObjectName(u"registerButton")

        self.verticalLayout.addWidget(self.registerButton)

        self.annotateButton = QPushButton(dataNavigationWidget)
        self.annotateButton.setObjectName(u"annotateButton")

        self.verticalLayout.addWidget(self.annotateButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_4.addLayout(self.verticalLayout)


        self.retranslateUi(dataNavigationWidget)

        QMetaObject.connectSlotsByName(dataNavigationWidget)
    # setupUi

    def retranslateUi(self, dataNavigationWidget):
        dataNavigationWidget.setWindowTitle(QCoreApplication.translate("dataNavigationWidget", u"Data Collections", None))
        self.registerButton.setText(QCoreApplication.translate("dataNavigationWidget", u"Register", None))
        self.annotateButton.setText(QCoreApplication.translate("dataNavigationWidget", u"Annotate", None))
    # retranslateUi

