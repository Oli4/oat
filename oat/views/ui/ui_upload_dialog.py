# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_upload_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UploadDialog(object):
    def setupUi(self, UploadDialog):
        UploadDialog.setObjectName("UploadDialog")
        UploadDialog.resize(400, 237)
        self.verticalLayout = QtWidgets.QVBoxLayout(UploadDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.patientLabel = QtWidgets.QLabel(UploadDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.patientLabel.setFont(font)
        self.patientLabel.setObjectName("patientLabel")
        self.verticalLayout.addWidget(self.patientLabel)
        self.patientLayout = QtWidgets.QHBoxLayout()
        self.patientLayout.setObjectName("patientLayout")
        self.patientDropdown = QtWidgets.QComboBox(UploadDialog)
        self.patientDropdown.setObjectName("patientDropdown")
        self.patientLayout.addWidget(self.patientDropdown)
        self.addPatientButton = QtWidgets.QToolButton(UploadDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-add_circle-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addPatientButton.setIcon(icon)
        self.addPatientButton.setIconSize(QtCore.QSize(24, 24))
        self.addPatientButton.setObjectName("addPatientButton")
        self.patientLayout.addWidget(self.addPatientButton)
        self.verticalLayout.addLayout(self.patientLayout)
        self.collectionLabel = QtWidgets.QLabel(UploadDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.collectionLabel.setFont(font)
        self.collectionLabel.setObjectName("collectionLabel")
        self.verticalLayout.addWidget(self.collectionLabel)
        self.collectionLayout = QtWidgets.QHBoxLayout()
        self.collectionLayout.setObjectName("collectionLayout")
        self.collectionDropdown = QtWidgets.QComboBox(UploadDialog)
        self.collectionDropdown.setObjectName("collectionDropdown")
        self.collectionLayout.addWidget(self.collectionDropdown)
        self.addCollectionButton = QtWidgets.QToolButton(UploadDialog)
        self.addCollectionButton.setIcon(icon)
        self.addCollectionButton.setIconSize(QtCore.QSize(24, 24))
        self.addCollectionButton.setObjectName("addCollectionButton")
        self.collectionLayout.addWidget(self.addCollectionButton)
        self.verticalLayout.addLayout(self.collectionLayout)
        self.fileLabel = QtWidgets.QLabel(UploadDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fileLabel.setFont(font)
        self.fileLabel.setObjectName("fileLabel")
        self.verticalLayout.addWidget(self.fileLabel)
        self.fileLayout = QtWidgets.QHBoxLayout()
        self.fileLayout.setObjectName("fileLayout")
        self.fileSelectButton = QtWidgets.QPushButton(UploadDialog)
        self.fileSelectButton.setObjectName("fileSelectButton")
        self.fileLayout.addWidget(self.fileSelectButton)
        self.fileName = QtWidgets.QLabel(UploadDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileName.sizePolicy().hasHeightForWidth())
        self.fileName.setSizePolicy(sizePolicy)
        self.fileName.setText("")
        self.fileName.setObjectName("fileName")
        self.fileLayout.addWidget(self.fileName)
        self.verticalLayout.addLayout(self.fileLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(UploadDialog)
        self.buttonBox.setEnabled(True)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(UploadDialog)
        self.buttonBox.accepted.connect(UploadDialog.accept)
        self.buttonBox.rejected.connect(UploadDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UploadDialog)

    def retranslateUi(self, UploadDialog):
        _translate = QtCore.QCoreApplication.translate
        UploadDialog.setWindowTitle(_translate("UploadDialog", "Dialog"))
        self.patientLabel.setText(_translate("UploadDialog", "Patient:"))
        self.addPatientButton.setText(_translate("UploadDialog", "+"))
        self.collectionLabel.setText(_translate("UploadDialog", "Collection"))
        self.addCollectionButton.setText(_translate("UploadDialog", "+"))
        self.fileLabel.setText(_translate("UploadDialog", "File:"))
        self.fileSelectButton.setText(_translate("UploadDialog", "Select"))


from . import resources_rc
