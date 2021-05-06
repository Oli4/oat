# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_add_collection_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_AddCollectionDialog(object):
    def setupUi(self, AddCollectionDialog):
        if not AddCollectionDialog.objectName():
            AddCollectionDialog.setObjectName(u"AddCollectionDialog")
        AddCollectionDialog.resize(321, 155)
        self.verticalLayout = QVBoxLayout(AddCollectionDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(AddCollectionDialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout_3.addWidget(self.label)

        self.nameEdit = QLineEdit(AddCollectionDialog)
        self.nameEdit.setObjectName(u"nameEdit")

        self.verticalLayout_3.addWidget(self.nameEdit)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(AddCollectionDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout_2.addWidget(self.label_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.od_button = QRadioButton(AddCollectionDialog)
        self.od_button.setObjectName(u"od_button")

        self.horizontalLayout.addWidget(self.od_button)

        self.os_button = QRadioButton(AddCollectionDialog)
        self.os_button.setObjectName(u"os_button")

        self.horizontalLayout.addWidget(self.os_button)

        self.na_button = QRadioButton(AddCollectionDialog)
        self.na_button.setObjectName(u"na_button")
        self.na_button.setChecked(True)

        self.horizontalLayout.addWidget(self.na_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.buttonBox = QDialogButtonBox(AddCollectionDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AddCollectionDialog)
        self.buttonBox.accepted.connect(AddCollectionDialog.accept)
        self.buttonBox.rejected.connect(AddCollectionDialog.reject)

        QMetaObject.connectSlotsByName(AddCollectionDialog)
    # setupUi

    def retranslateUi(self, AddCollectionDialog):
        AddCollectionDialog.setWindowTitle(QCoreApplication.translate("AddCollectionDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("AddCollectionDialog", u"Name", None))
        self.label_2.setText(QCoreApplication.translate("AddCollectionDialog", u"Laterality", None))
        self.od_button.setText(QCoreApplication.translate("AddCollectionDialog", u"OD", None))
        self.os_button.setText(QCoreApplication.translate("AddCollectionDialog", u"OS", None))
        self.na_button.setText(QCoreApplication.translate("AddCollectionDialog", u"NA", None))
    # retranslateUi

