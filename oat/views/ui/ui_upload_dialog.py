# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_upload_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UploadDialog(object):
    def setupUi(self, UploadDialog):
        UploadDialog.setObjectName("UploadDialog")
        UploadDialog.resize(400, 153)
        self.verticalLayout = QtWidgets.QVBoxLayout(UploadDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(UploadDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.patientDropdown = QtWidgets.QComboBox(UploadDialog)
        self.patientDropdown.setObjectName("patientDropdown")
        self.horizontalLayout_2.addWidget(self.patientDropdown)
        self.addPatientButton = QtWidgets.QToolButton(UploadDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/baseline-add_circle-24px.svg"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addPatientButton.setIcon(icon)
        self.addPatientButton.setIconSize(QtCore.QSize(24, 24))
        self.addPatientButton.setObjectName("addPatientButton")
        self.horizontalLayout_2.addWidget(self.addPatientButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_2 = QtWidgets.QLabel(UploadDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fileSelectButton = QtWidgets.QPushButton(UploadDialog)
        self.fileSelectButton.setObjectName("fileSelectButton")
        self.horizontalLayout.addWidget(self.fileSelectButton)
        self.fileName = QtWidgets.QLabel(UploadDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fileName.sizePolicy().hasHeightForWidth())
        self.fileName.setSizePolicy(sizePolicy)
        self.fileName.setText("")
        self.fileName.setObjectName("fileName")
        self.horizontalLayout.addWidget(self.fileName)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(UploadDialog)
        self.buttonBox.setEnabled(True)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
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
        self.label.setText(_translate("UploadDialog", "Patient:"))
        self.addPatientButton.setText(_translate("UploadDialog", "+"))
        self.label_2.setText(_translate("UploadDialog", "File:"))
        self.fileSelectButton.setText(_translate("UploadDialog", "Select"))
