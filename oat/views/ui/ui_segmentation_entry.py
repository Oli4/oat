# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_segmentation_entry.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from  . import resources_rc

class Ui_SegmentationEntry(object):
    def setupUi(self, SegmentationEntry):
        if not SegmentationEntry.objectName():
            SegmentationEntry.setObjectName(u"SegmentationEntry")
        SegmentationEntry.resize(300, 37)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SegmentationEntry.sizePolicy().hasHeightForWidth())
        SegmentationEntry.setSizePolicy(sizePolicy)
        SegmentationEntry.setMinimumSize(QSize(0, 37))
        SegmentationEntry.setMaximumSize(QSize(300, 37))
        SegmentationEntry.setAutoFillBackground(True)
        self.horizontalLayoutWidget = QWidget(SegmentationEntry)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 291, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.hideButton = QToolButton(self.horizontalLayoutWidget)
        self.hideButton.setObjectName(u"hideButton")
        sizePolicy.setHeightForWidth(self.hideButton.sizePolicy().hasHeightForWidth())
        self.hideButton.setSizePolicy(sizePolicy)
        self.hideButton.setMinimumSize(QSize(30, 30))
        self.hideButton.setMaximumSize(QSize(30, 30))
        self.hideButton.setAutoFillBackground(False)
        icon = QIcon()
        icon.addFile(u":/icons/icons/baseline-visibility-24px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.hideButton.setIcon(icon)
        self.hideButton.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.hideButton)

        self.horizontalSpacer = QSpacerItem(30, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(180, 30))
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)


        self.retranslateUi(SegmentationEntry)

        QMetaObject.connectSlotsByName(SegmentationEntry)
    # setupUi

    def retranslateUi(self, SegmentationEntry):
        SegmentationEntry.setWindowTitle(QCoreApplication.translate("SegmentationEntry", u"Form", None))
        self.hideButton.setText(QCoreApplication.translate("SegmentationEntry", u"...", None))
        self.label.setText(QCoreApplication.translate("SegmentationEntry", u"New Segmentation", None))
    # retranslateUi

