# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_layer_entry.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LayerEntry(object):
    def setupUi(self, LayerEntry):
        LayerEntry.setObjectName("LayerEntry")
        LayerEntry.resize(150, 30)
        LayerEntry.setMinimumSize(QtCore.QSize(150, 30))
        LayerEntry.setMaximumSize(QtCore.QSize(300, 30))
        self.horizontalLayout = QtWidgets.QHBoxLayout(LayerEntry)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hideButton = QtWidgets.QToolButton(LayerEntry)
        self.hideButton.setMinimumSize(QtCore.QSize(26, 26))
        self.hideButton.setMaximumSize(QtCore.QSize(26, 26))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-visibility-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hideButton.setIcon(icon)
        self.hideButton.setIconSize(QtCore.QSize(24, 24))
        self.hideButton.setObjectName("hideButton")
        self.horizontalLayout.addWidget(self.hideButton)
        self.color_label = QtWidgets.QLabel(LayerEntry)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.color_label.sizePolicy().hasHeightForWidth())
        self.color_label.setSizePolicy(sizePolicy)
        self.color_label.setMinimumSize(QtCore.QSize(25, 25))
        self.color_label.setMaximumSize(QtCore.QSize(25, 25))
        self.color_label.setAutoFillBackground(False)
        self.color_label.setStyleSheet("background-color: rgb(138, 226, 52);")
        self.color_label.setText("")
        self.color_label.setObjectName("color_label")
        self.horizontalLayout.addWidget(self.color_label)
        self.label = QtWidgets.QLabel(LayerEntry)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.settingButton = QtWidgets.QToolButton(LayerEntry)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingButton.sizePolicy().hasHeightForWidth())
        self.settingButton.setSizePolicy(sizePolicy)
        self.settingButton.setMinimumSize(QtCore.QSize(26, 26))
        self.settingButton.setMaximumSize(QtCore.QSize(26, 26))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-settings-20px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settingButton.setIcon(icon1)
        self.settingButton.setIconSize(QtCore.QSize(24, 24))
        self.settingButton.setObjectName("settingButton")
        self.horizontalLayout.addWidget(self.settingButton)

        self.retranslateUi(LayerEntry)
        QtCore.QMetaObject.connectSlotsByName(LayerEntry)

    def retranslateUi(self, LayerEntry):
        _translate = QtCore.QCoreApplication.translate
        LayerEntry.setWindowTitle(_translate("LayerEntry", "Form"))
        self.hideButton.setText(_translate("LayerEntry", "..."))
        self.label.setText(_translate("LayerEntry", "Layer Name"))
        self.settingButton.setText(_translate("LayerEntry", "..."))
from . import resources_rc
