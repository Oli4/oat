# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_login_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        if not LoginDialog.objectName():
            LoginDialog.setObjectName(u"LoginDialog")
        LoginDialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(LoginDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(LoginDialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.dbDropdown = QComboBox(LoginDialog)
        self.dbDropdown.setObjectName(u"dbDropdown")
        self.dbDropdown.setEditable(True)

        self.horizontalLayout_3.addWidget(self.dbDropdown)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(LoginDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.username = QLineEdit(LoginDialog)
        self.username.setObjectName(u"username")

        self.horizontalLayout.addWidget(self.username)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(LoginDialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.password = QLineEdit(LoginDialog)
        self.password.setObjectName(u"password")
        self.password.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_2.addWidget(self.password)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(LoginDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(LoginDialog)
        self.buttonBox.rejected.connect(LoginDialog.reject)

        QMetaObject.connectSlotsByName(LoginDialog)
    # setupUi

    def retranslateUi(self, LoginDialog):
        LoginDialog.setWindowTitle(QCoreApplication.translate("LoginDialog", u"Dialog", None))
        self.label_3.setText(QCoreApplication.translate("LoginDialog", u"Database", None))
        self.label.setText(QCoreApplication.translate("LoginDialog", u"Username:", None))
        self.label_2.setText(QCoreApplication.translate("LoginDialog", u"Password:", None))
    # retranslateUi

