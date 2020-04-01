# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_data_table_view.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_DataTableView(object):
    def setupUi(self, DataTableView):
        DataTableView.setObjectName("DataTableView")
        DataTableView.resize(520, 350)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            DataTableView.sizePolicy().hasHeightForWidth())
        DataTableView.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(DataTableView)
        self.verticalLayout.setObjectName("verticalLayout")
        self.AddButton = QtWidgets.QToolButton(DataTableView)
        self.AddButton.setObjectName("AddButton")
        self.verticalLayout.addWidget(self.AddButton)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(
            QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.PatientView = QtWidgets.QTableView(DataTableView)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.PatientView.sizePolicy().hasHeightForWidth())
        self.PatientView.setSizePolicy(sizePolicy)
        self.PatientView.setMinimumSize(QtCore.QSize(480, 300))
        self.PatientView.setAutoFillBackground(True)
        self.PatientView.setSortingEnabled(True)
        self.PatientView.setObjectName("PatientView")
        self.PatientView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.PatientView)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(DataTableView)
        QtCore.QMetaObject.connectSlotsByName(DataTableView)

    def retranslateUi(self, DataTableView):
        _translate = QtCore.QCoreApplication.translate
        DataTableView.setWindowTitle(_translate("DataTableView", "Form"))
        self.AddButton.setText(_translate("DataTableView", "Add Patient"))
