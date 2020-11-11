# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_add_collection_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddCollectionDialog(object):
    def setupUi(self, AddCollectionDialog):
        AddCollectionDialog.setObjectName("AddCollectionDialog")
        AddCollectionDialog.resize(321, 107)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddCollectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(AddCollectionDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.nameEdit = QtWidgets.QLineEdit(AddCollectionDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.verticalLayout_3.addWidget(self.nameEdit)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddCollectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddCollectionDialog)
        self.buttonBox.accepted.connect(AddCollectionDialog.accept)
        self.buttonBox.rejected.connect(AddCollectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddCollectionDialog)

    def retranslateUi(self, AddCollectionDialog):
        _translate = QtCore.QCoreApplication.translate
        AddCollectionDialog.setWindowTitle(_translate("AddCollectionDialog", "Dialog"))
        self.label.setText(_translate("AddCollectionDialog", "Name"))
