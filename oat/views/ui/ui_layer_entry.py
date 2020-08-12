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
        LayerEntry.resize(243, 60)
        LayerEntry.setMinimumSize(QtCore.QSize(150, 60))
        LayerEntry.setMaximumSize(QtCore.QSize(16777215, 60))
        self.horizontalLayout = QtWidgets.QHBoxLayout(LayerEntry)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hideButton = QtWidgets.QToolButton(LayerEntry)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-visibility-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hideButton.setIcon(icon)
        self.hideButton.setIconSize(QtCore.QSize(24, 24))
        self.hideButton.setObjectName("hideButton")
        self.horizontalLayout.addWidget(self.hideButton)
        self.line = QtWidgets.QFrame(LayerEntry)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.LayerName = QtWidgets.QLineEdit(LayerEntry)
        self.LayerName.setObjectName("LayerName")
        self.horizontalLayout.addWidget(self.LayerName)
        self.settingButton = QtWidgets.QToolButton(LayerEntry)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-settings-20px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settingButton.setIcon(icon1)
        self.settingButton.setIconSize(QtCore.QSize(24, 24))
        self.settingButton.setObjectName("settingButton")
        self.horizontalLayout.addWidget(self.settingButton)
        self.saveButton = QtWidgets.QToolButton(LayerEntry)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-save-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton.setIcon(icon2)
        self.saveButton.setIconSize(QtCore.QSize(24, 24))
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)

        self.retranslateUi(LayerEntry)
        QtCore.QMetaObject.connectSlotsByName(LayerEntry)

    def retranslateUi(self, LayerEntry):
        _translate = QtCore.QCoreApplication.translate
        LayerEntry.setWindowTitle(_translate("LayerEntry", "Form"))
        self.hideButton.setText(_translate("LayerEntry", "..."))
        self.LayerName.setText(_translate("LayerEntry", "New Layer"))
        self.settingButton.setText(_translate("LayerEntry", "..."))
        self.saveButton.setText(_translate("LayerEntry", "..."))
from . import resources_rc
