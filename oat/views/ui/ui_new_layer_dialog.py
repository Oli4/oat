# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_new_layer_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_NewLayerDialog(object):
    def setupUi(self, NewLayerDialog):
        NewLayerDialog.setObjectName("NewLayerDialog")
        NewLayerDialog.resize(285, 185)
        self.verticalLayout = QtWidgets.QVBoxLayout(NewLayerDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(NewLayerDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(NewLayerDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(NewLayerDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBox = QtWidgets.QComboBox(NewLayerDialog)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewLayerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(NewLayerDialog)
        self.buttonBox.accepted.connect(NewLayerDialog.accept)
        self.buttonBox.rejected.connect(NewLayerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewLayerDialog)

    def retranslateUi(self, NewLayerDialog):
        _translate = QtCore.QCoreApplication.translate
        NewLayerDialog.setWindowTitle(_translate("NewLayerDialog", "Dialog"))
        self.label.setText(_translate("NewLayerDialog", "Layer Name:"))
        self.label_2.setText(_translate("NewLayerDialog", "Layer Type:"))
        self.comboBox.setItemText(0, _translate("NewLayerDialog", "Line Layer"))
        self.comboBox.setItemText(1, _translate("NewLayerDialog", "Area Layer"))
        self.comboBox.setItemText(2, _translate("NewLayerDialog", "ImageLayer"))
        self.comboBox.setItemText(3, _translate("NewLayerDialog", "OCT Layer"))
        self.comboBox.setItemText(4, _translate("NewLayerDialog", "NIR Layer"))
        self.comboBox.setItemText(5, _translate("NewLayerDialog", "CFP Layer"))
        self.comboBox.setItemText(6, _translate("NewLayerDialog", "HRF Layer"))
        self.comboBox.setItemText(7, _translate("NewLayerDialog", "Drusen layer"))
        self.comboBox.setItemText(8, _translate("NewLayerDialog", "RPE Layer"))
        self.comboBox.setItemText(9, _translate("NewLayerDialog", "BM Layer"))
        self.comboBox.setItemText(10, _translate("NewLayerDialog", "EZ Layer"))
