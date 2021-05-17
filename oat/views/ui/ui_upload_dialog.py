# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_upload_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from  . import resources_rc

class Ui_UploadDialog(object):
    def setupUi(self, UploadDialog):
        if not UploadDialog.objectName():
            UploadDialog.setObjectName(u"UploadDialog")
        UploadDialog.resize(400, 237)
        self.verticalLayout = QVBoxLayout(UploadDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.patientLabel = QLabel(UploadDialog)
        self.patientLabel.setObjectName(u"patientLabel")
        font = QFont()
        font.setBold(True)
        self.patientLabel.setFont(font)

        self.verticalLayout.addWidget(self.patientLabel)

        self.patientLayout = QHBoxLayout()
        self.patientLayout.setObjectName(u"patientLayout")
        self.patientDropdown = QComboBox(UploadDialog)
        self.patientDropdown.setObjectName(u"patientDropdown")

        self.patientLayout.addWidget(self.patientDropdown)

        self.addPatientButton = QToolButton(UploadDialog)
        self.addPatientButton.setObjectName(u"addPatientButton")
        icon = QIcon()
        icon.addFile(u":/icons/icons/baseline-add_circle-24px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.addPatientButton.setIcon(icon)
        self.addPatientButton.setIconSize(QSize(24, 24))

        self.patientLayout.addWidget(self.addPatientButton)


        self.verticalLayout.addLayout(self.patientLayout)

        self.collectionLabel = QLabel(UploadDialog)
        self.collectionLabel.setObjectName(u"collectionLabel")
        self.collectionLabel.setFont(font)

        self.verticalLayout.addWidget(self.collectionLabel)

        self.collectionLayout = QHBoxLayout()
        self.collectionLayout.setObjectName(u"collectionLayout")
        self.collectionDropdown = QComboBox(UploadDialog)
        self.collectionDropdown.setObjectName(u"collectionDropdown")

        self.collectionLayout.addWidget(self.collectionDropdown)

        self.addCollectionButton = QToolButton(UploadDialog)
        self.addCollectionButton.setObjectName(u"addCollectionButton")
        self.addCollectionButton.setIcon(icon)
        self.addCollectionButton.setIconSize(QSize(24, 24))

        self.collectionLayout.addWidget(self.addCollectionButton)


        self.verticalLayout.addLayout(self.collectionLayout)

        self.fileLabel = QLabel(UploadDialog)
        self.fileLabel.setObjectName(u"fileLabel")
        self.fileLabel.setFont(font)

        self.verticalLayout.addWidget(self.fileLabel)

        self.fileLayout = QHBoxLayout()
        self.fileLayout.setObjectName(u"fileLayout")
        self.fileSelectButton = QPushButton(UploadDialog)
        self.fileSelectButton.setObjectName(u"fileSelectButton")

        self.fileLayout.addWidget(self.fileSelectButton)

        self.fileName = QLabel(UploadDialog)
        self.fileName.setObjectName(u"fileName")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileName.sizePolicy().hasHeightForWidth())
        self.fileName.setSizePolicy(sizePolicy)

        self.fileLayout.addWidget(self.fileName)


        self.verticalLayout.addLayout(self.fileLayout)

        self.buttonBox = QDialogButtonBox(UploadDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setEnabled(True)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(UploadDialog)
        self.buttonBox.accepted.connect(UploadDialog.accept)
        self.buttonBox.rejected.connect(UploadDialog.reject)

        QMetaObject.connectSlotsByName(UploadDialog)
    # setupUi

    def retranslateUi(self, UploadDialog):
        UploadDialog.setWindowTitle(QCoreApplication.translate("UploadDialog", u"Dialog", None))
        self.patientLabel.setText(QCoreApplication.translate("UploadDialog", u"Patient:", None))
        self.addPatientButton.setText(QCoreApplication.translate("UploadDialog", u"+", None))
        self.collectionLabel.setText(QCoreApplication.translate("UploadDialog", u"Collection", None))
        self.addCollectionButton.setText(QCoreApplication.translate("UploadDialog", u"+", None))
        self.fileLabel.setText(QCoreApplication.translate("UploadDialog", u"File:", None))
        self.fileSelectButton.setText(QCoreApplication.translate("UploadDialog", u"Select", None))
        self.fileName.setText("")
    # retranslateUi

