# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_add_patient_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_AddPatientDialog(object):
    def setupUi(self, AddPatientDialog):
        if not AddPatientDialog.objectName():
            AddPatientDialog.setObjectName(u"AddPatientDialog")
        AddPatientDialog.resize(321, 160)
        self.verticalLayout = QVBoxLayout(AddPatientDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(AddPatientDialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout_2.addWidget(self.label)

        self.pseudonymEdit = QLineEdit(AddPatientDialog)
        self.pseudonymEdit.setObjectName(u"pseudonymEdit")

        self.verticalLayout_2.addWidget(self.pseudonymEdit)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(AddPatientDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout_3.addWidget(self.label_2)

        self.genderBox = QComboBox(AddPatientDialog)
        self.genderBox.addItem("")
        self.genderBox.addItem("")
        self.genderBox.addItem("")
        self.genderBox.setObjectName(u"genderBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.genderBox.sizePolicy().hasHeightForWidth())
        self.genderBox.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.genderBox)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_3 = QLabel(AddPatientDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout_4.addWidget(self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.birthdayRadioButton = QRadioButton(AddPatientDialog)
        self.birthdayRadioButton.setObjectName(u"birthdayRadioButton")
        self.birthdayRadioButton.setChecked(True)

        self.horizontalLayout_2.addWidget(self.birthdayRadioButton)

        self.birthdayEdit = QDateEdit(AddPatientDialog)
        self.birthdayEdit.setObjectName(u"birthdayEdit")
        self.birthdayEdit.setEnabled(True)
        self.birthdayEdit.setCurrentSection(QDateTimeEdit.DaySection)
        self.birthdayEdit.setCalendarPopup(True)

        self.horizontalLayout_2.addWidget(self.birthdayEdit)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addLayout(self.verticalLayout_4)

        self.buttonBox = QDialogButtonBox(AddPatientDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AddPatientDialog)
        self.buttonBox.accepted.connect(AddPatientDialog.accept)
        self.buttonBox.rejected.connect(AddPatientDialog.reject)

        QMetaObject.connectSlotsByName(AddPatientDialog)
    # setupUi

    def retranslateUi(self, AddPatientDialog):
        AddPatientDialog.setWindowTitle(QCoreApplication.translate("AddPatientDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("AddPatientDialog", u"Pseudonym", None))
        self.label_2.setText(QCoreApplication.translate("AddPatientDialog", u"Gender", None))
        self.genderBox.setItemText(0, QCoreApplication.translate("AddPatientDialog", u"Unknown", None))
        self.genderBox.setItemText(1, QCoreApplication.translate("AddPatientDialog", u"Female", None))
        self.genderBox.setItemText(2, QCoreApplication.translate("AddPatientDialog", u"Male", None))

        self.label_3.setText(QCoreApplication.translate("AddPatientDialog", u"Birthday", None))
        self.birthdayRadioButton.setText(QCoreApplication.translate("AddPatientDialog", u"Unknown", None))
    # retranslateUi

