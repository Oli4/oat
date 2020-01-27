# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_segmentation_entry.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SegmentationEntry(object):
    def setupUi(self, SegmentationEntry):
        SegmentationEntry.setObjectName("SegmentationEntry")
        SegmentationEntry.resize(300, 38)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SegmentationEntry.sizePolicy().hasHeightForWidth())
        SegmentationEntry.setSizePolicy(sizePolicy)
        SegmentationEntry.setMaximumSize(QtCore.QSize(300, 38))
        self.horizontalLayoutWidget = QtWidgets.QWidget(SegmentationEntry)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 291, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hideButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.hideButton.setAutoFillBackground(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-visibility-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hideButton.setIcon(icon)
        self.hideButton.setIconSize(QtCore.QSize(24, 24))
        self.hideButton.setObjectName("hideButton")
        self.horizontalLayout.addWidget(self.hideButton)
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setMaximumSize(QtCore.QSize(180, 34))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.retranslateUi(SegmentationEntry)
        QtCore.QMetaObject.connectSlotsByName(SegmentationEntry)

    def retranslateUi(self, SegmentationEntry):
        _translate = QtCore.QCoreApplication.translate
        SegmentationEntry.setWindowTitle(_translate("SegmentationEntry", "Form"))
        self.hideButton.setText(_translate("SegmentationEntry", "..."))
        self.label.setText(_translate("SegmentationEntry", "New Segmentation"))


from . import resources_rc
