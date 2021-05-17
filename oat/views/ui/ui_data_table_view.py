# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_data_table_view.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_DataTableView(object):
    def setupUi(self, DataTableView):
        if not DataTableView.objectName():
            DataTableView.setObjectName(u"DataTableView")
        DataTableView.resize(520, 350)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DataTableView.sizePolicy().hasHeightForWidth())
        DataTableView.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(DataTableView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.AddButton = QToolButton(DataTableView)
        self.AddButton.setObjectName(u"AddButton")

        self.verticalLayout.addWidget(self.AddButton)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetMaximumSize)
        self.PatientView = QTableView(DataTableView)
        self.PatientView.setObjectName(u"PatientView")
        sizePolicy.setHeightForWidth(self.PatientView.sizePolicy().hasHeightForWidth())
        self.PatientView.setSizePolicy(sizePolicy)
        self.PatientView.setMinimumSize(QSize(480, 300))
        self.PatientView.setAutoFillBackground(True)
        self.PatientView.setSortingEnabled(True)
        self.PatientView.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_2.addWidget(self.PatientView)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(DataTableView)

        QMetaObject.connectSlotsByName(DataTableView)
    # setupUi

    def retranslateUi(self, DataTableView):
        DataTableView.setWindowTitle(QCoreApplication.translate("DataTableView", u"Form", None))
        self.AddButton.setText(QCoreApplication.translate("DataTableView", u"Add Patient", None))
    # retranslateUi

