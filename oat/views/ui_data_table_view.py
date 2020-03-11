# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_data_table_view.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DataTableView(object):
    def setupUi(self, DataTableView):
        DataTableView.setObjectName("DataTableView")
        DataTableView.resize(833, 333)
        self.verticalLayout = QtWidgets.QVBoxLayout(DataTableView)
        self.verticalLayout.setObjectName("verticalLayout")
        self.PatientView = QtWidgets.QTableView(DataTableView)
        self.PatientView.setObjectName("PatientView")
        self.verticalLayout.addWidget(self.PatientView)

        self.retranslateUi(DataTableView)
        QtCore.QMetaObject.connectSlotsByName(DataTableView)

    def retranslateUi(self, DataTableView):
        _translate = QtCore.QCoreApplication.translate
        DataTableView.setWindowTitle(_translate("DataTableView", "Form"))
