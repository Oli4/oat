# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_new_layer_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_NewLayerDialog(object):
    def setupUi(self, NewLayerDialog):
        if not NewLayerDialog.objectName():
            NewLayerDialog.setObjectName(u"NewLayerDialog")
        NewLayerDialog.resize(285, 185)
        self.verticalLayout = QVBoxLayout(NewLayerDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(NewLayerDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(NewLayerDialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(NewLayerDialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.comboBox = QComboBox(NewLayerDialog)
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
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_2.addWidget(self.comboBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(NewLayerDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(NewLayerDialog)
        self.buttonBox.accepted.connect(NewLayerDialog.accept)
        self.buttonBox.rejected.connect(NewLayerDialog.reject)

        QMetaObject.connectSlotsByName(NewLayerDialog)
    # setupUi

    def retranslateUi(self, NewLayerDialog):
        NewLayerDialog.setWindowTitle(QCoreApplication.translate("NewLayerDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("NewLayerDialog", u"Layer Name:", None))
        self.label_2.setText(QCoreApplication.translate("NewLayerDialog", u"Layer Type:", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("NewLayerDialog", u"Line Layer", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("NewLayerDialog", u"Area Layer", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("NewLayerDialog", u"ImageLayer", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("NewLayerDialog", u"OCT Layer", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("NewLayerDialog", u"NIR Layer", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("NewLayerDialog", u"CFP Layer", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("NewLayerDialog", u"HRF Layer", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("NewLayerDialog", u"Drusen layer", None))
        self.comboBox.setItemText(8, QCoreApplication.translate("NewLayerDialog", u"RPE Layer", None))
        self.comboBox.setItemText(9, QCoreApplication.translate("NewLayerDialog", u"BM Layer", None))
        self.comboBox.setItemText(10, QCoreApplication.translate("NewLayerDialog", u"EZ Layer", None))

    # retranslateUi

