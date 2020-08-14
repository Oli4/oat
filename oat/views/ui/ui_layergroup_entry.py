# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_layergroup_entry.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LayerGroupEntry(object):
    def setupUi(self, LayerGroupEntry):
        LayerGroupEntry.setObjectName("LayerGroupEntry")
        LayerGroupEntry.resize(200, 30)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LayerGroupEntry.sizePolicy().hasHeightForWidth())
        LayerGroupEntry.setSizePolicy(sizePolicy)
        LayerGroupEntry.setMinimumSize(QtCore.QSize(200, 30))
        LayerGroupEntry.setMaximumSize(QtCore.QSize(350, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        LayerGroupEntry.setFont(font)
        LayerGroupEntry.setAutoFillBackground(True)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(LayerGroupEntry)
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.hideButton = QtWidgets.QToolButton(LayerGroupEntry)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hideButton.sizePolicy().hasHeightForWidth())
        self.hideButton.setSizePolicy(sizePolicy)
        self.hideButton.setMinimumSize(QtCore.QSize(26, 26))
        self.hideButton.setMaximumSize(QtCore.QSize(26, 26))
        self.hideButton.setAutoFillBackground(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-visibility-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hideButton.setIcon(icon)
        self.hideButton.setIconSize(QtCore.QSize(24, 24))
        self.hideButton.setObjectName("hideButton")
        self.horizontalLayout_2.addWidget(self.hideButton)
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(LayerGroupEntry)
        self.label.setMinimumSize(QtCore.QSize(0, 26))
        self.label.setMaximumSize(QtCore.QSize(180, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)

        self.retranslateUi(LayerGroupEntry)
        QtCore.QMetaObject.connectSlotsByName(LayerGroupEntry)

    def retranslateUi(self, LayerGroupEntry):
        _translate = QtCore.QCoreApplication.translate
        LayerGroupEntry.setWindowTitle(_translate("LayerGroupEntry", "Form"))
        self.hideButton.setText(_translate("LayerGroupEntry", "..."))
        self.label.setText(_translate("LayerGroupEntry", "Layer Group Name"))
from . import resources_rc
