# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_add_dataset_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_AddDatasetDialog(object):
    def setupUi(self, AddDatasetDialog):
        if not AddDatasetDialog.objectName():
            AddDatasetDialog.setObjectName(u"AddDatasetDialog")
        AddDatasetDialog.resize(321, 155)
        self.verticalLayout = QVBoxLayout(AddDatasetDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label = QLabel(AddDatasetDialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label.setFont(font)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label)

        self.nameEdit = QLineEdit(AddDatasetDialog)
        self.nameEdit.setObjectName(u"nameEdit")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.nameEdit)

        self.label_2 = QLabel(AddDatasetDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.infoEdit = QTextEdit(AddDatasetDialog)
        self.infoEdit.setObjectName(u"infoEdit")
        self.infoEdit.setAcceptRichText(False)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.infoEdit)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.buttonBox = QDialogButtonBox(AddDatasetDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AddDatasetDialog)
        self.buttonBox.accepted.connect(AddDatasetDialog.accept)
        self.buttonBox.rejected.connect(AddDatasetDialog.reject)

        QMetaObject.connectSlotsByName(AddDatasetDialog)
    # setupUi

    def retranslateUi(self, AddDatasetDialog):
        AddDatasetDialog.setWindowTitle(QCoreApplication.translate("AddDatasetDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("AddDatasetDialog", u"Name:", None))
        self.label_2.setText(QCoreApplication.translate("AddDatasetDialog", u"Info:", None))
    # retranslateUi

