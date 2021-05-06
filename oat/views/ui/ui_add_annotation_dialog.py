# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_add_annotation_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from  . import resources_rc

class Ui_AnnotationDialog(object):
    def setupUi(self, AnnotationDialog):
        if not AnnotationDialog.objectName():
            AnnotationDialog.setObjectName(u"AnnotationDialog")
        AnnotationDialog.resize(400, 244)
        self.verticalLayout = QVBoxLayout(AnnotationDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelLayoutAreas = QHBoxLayout()
        self.labelLayoutAreas.setObjectName(u"labelLayoutAreas")
        self.addAreaTypeButton = QToolButton(AnnotationDialog)
        self.addAreaTypeButton.setObjectName(u"addAreaTypeButton")
        icon = QIcon()
        icon.addFile(u":/icons/icons/baseline-add_circle-24px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.addAreaTypeButton.setIcon(icon)
        self.addAreaTypeButton.setIconSize(QSize(24, 24))

        self.labelLayoutAreas.addWidget(self.addAreaTypeButton)

        self.areaLabel = QLabel(AnnotationDialog)
        self.areaLabel.setObjectName(u"areaLabel")
        font = QFont()
        font.setBold(True)
        self.areaLabel.setFont(font)

        self.labelLayoutAreas.addWidget(self.areaLabel)


        self.verticalLayout.addLayout(self.labelLayoutAreas)

        self.areaLayout = QVBoxLayout()
        self.areaLayout.setObjectName(u"areaLayout")

        self.verticalLayout.addLayout(self.areaLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(AnnotationDialog)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.modalitiesCheckBox = QCheckBox(AnnotationDialog)
        self.modalitiesCheckBox.setObjectName(u"modalitiesCheckBox")
        self.modalitiesCheckBox.setEnabled(True)
        self.modalitiesCheckBox.setCheckable(True)
        self.modalitiesCheckBox.setChecked(False)
        self.modalitiesCheckBox.setTristate(False)

        self.horizontalLayout.addWidget(self.modalitiesCheckBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line = QFrame(AnnotationDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.labelLayoutLayers = QHBoxLayout()
        self.labelLayoutLayers.setObjectName(u"labelLayoutLayers")
        self.addLayerTypeButton = QToolButton(AnnotationDialog)
        self.addLayerTypeButton.setObjectName(u"addLayerTypeButton")
        self.addLayerTypeButton.setIcon(icon)
        self.addLayerTypeButton.setIconSize(QSize(24, 24))

        self.labelLayoutLayers.addWidget(self.addLayerTypeButton)

        self.layerLabel = QLabel(AnnotationDialog)
        self.layerLabel.setObjectName(u"layerLabel")
        self.layerLabel.setFont(font)

        self.labelLayoutLayers.addWidget(self.layerLabel)


        self.verticalLayout.addLayout(self.labelLayoutLayers)

        self.layerLayout = QVBoxLayout()
        self.layerLayout.setObjectName(u"layerLayout")

        self.verticalLayout.addLayout(self.layerLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(AnnotationDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.slicesCheckBox = QCheckBox(AnnotationDialog)
        self.slicesCheckBox.setObjectName(u"slicesCheckBox")

        self.horizontalLayout_2.addWidget(self.slicesCheckBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(AnnotationDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setEnabled(True)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AnnotationDialog)
        self.buttonBox.accepted.connect(AnnotationDialog.accept)
        self.buttonBox.rejected.connect(AnnotationDialog.reject)

        QMetaObject.connectSlotsByName(AnnotationDialog)
    # setupUi

    def retranslateUi(self, AnnotationDialog):
        AnnotationDialog.setWindowTitle(QCoreApplication.translate("AnnotationDialog", u"Dialog", None))
        self.addAreaTypeButton.setText(QCoreApplication.translate("AnnotationDialog", u"+", None))
        self.areaLabel.setText(QCoreApplication.translate("AnnotationDialog", u"Areas:", None))
        self.label.setText(QCoreApplication.translate("AnnotationDialog", u"Settings:", None))
        self.modalitiesCheckBox.setText(QCoreApplication.translate("AnnotationDialog", u"Add to all modalities", None))
        self.addLayerTypeButton.setText(QCoreApplication.translate("AnnotationDialog", u"...", None))
        self.layerLabel.setText(QCoreApplication.translate("AnnotationDialog", u"Layers:", None))
        self.label_2.setText(QCoreApplication.translate("AnnotationDialog", u"Settings:", None))
        self.slicesCheckBox.setText(QCoreApplication.translate("AnnotationDialog", u"Add to all slices", None))
    # retranslateUi

