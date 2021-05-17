# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_add_areaannotation_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from  . import resources_rc

class Ui_AreaAnnotationDialog(object):
    def setupUi(self, AreaAnnotationDialog):
        if not AreaAnnotationDialog.objectName():
            AreaAnnotationDialog.setObjectName(u"AreaAnnotationDialog")
        AreaAnnotationDialog.resize(400, 159)
        self.verticalLayout = QVBoxLayout(AreaAnnotationDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.typeLabel = QLabel(AreaAnnotationDialog)
        self.typeLabel.setObjectName(u"typeLabel")
        font = QFont()
        font.setBold(True)
        self.typeLabel.setFont(font)

        self.verticalLayout.addWidget(self.typeLabel)

        self.typeLayout = QHBoxLayout()
        self.typeLayout.setObjectName(u"typeLayout")
        self.typeDropdown = QComboBox(AreaAnnotationDialog)
        self.typeDropdown.setObjectName(u"typeDropdown")

        self.typeLayout.addWidget(self.typeDropdown)

        self.addTypeButton = QToolButton(AreaAnnotationDialog)
        self.addTypeButton.setObjectName(u"addTypeButton")
        icon = QIcon()
        icon.addFile(u":/icons/icons/baseline-add_circle-24px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.addTypeButton.setIcon(icon)
        self.addTypeButton.setIconSize(QSize(24, 24))

        self.typeLayout.addWidget(self.addTypeButton)


        self.verticalLayout.addLayout(self.typeLayout)

        self.label = QLabel(AreaAnnotationDialog)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBox = QCheckBox(AreaAnnotationDialog)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout.addWidget(self.checkBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_2 = QLabel(AreaAnnotationDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_3 = QCheckBox(AreaAnnotationDialog)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.horizontalLayout_2.addWidget(self.checkBox_3)

        self.checkBox_2 = QCheckBox(AreaAnnotationDialog)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setEnabled(False)
        self.checkBox_2.setCheckable(True)
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setTristate(False)

        self.horizontalLayout_2.addWidget(self.checkBox_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(AreaAnnotationDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setEnabled(True)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AreaAnnotationDialog)
        self.buttonBox.accepted.connect(AreaAnnotationDialog.accept)
        self.buttonBox.rejected.connect(AreaAnnotationDialog.reject)

        QMetaObject.connectSlotsByName(AreaAnnotationDialog)
    # setupUi

    def retranslateUi(self, AreaAnnotationDialog):
        AreaAnnotationDialog.setWindowTitle(QCoreApplication.translate("AreaAnnotationDialog", u"Dialog", None))
        self.typeLabel.setText(QCoreApplication.translate("AreaAnnotationDialog", u"Areas:", None))
        self.addTypeButton.setText(QCoreApplication.translate("AreaAnnotationDialog", u"+", None))
        self.label.setText(QCoreApplication.translate("AreaAnnotationDialog", u"Layers:", None))
        self.checkBox.setText(QCoreApplication.translate("AreaAnnotationDialog", u"CheckBox", None))
        self.label_2.setText(QCoreApplication.translate("AreaAnnotationDialog", u"Settings:", None))
        self.checkBox_3.setText(QCoreApplication.translate("AreaAnnotationDialog", u"Add to all B-Scans", None))
        self.checkBox_2.setText(QCoreApplication.translate("AreaAnnotationDialog", u"Add to all modalities", None))
    # retranslateUi

