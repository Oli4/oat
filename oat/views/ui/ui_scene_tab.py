# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_scene_tab.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SceneTab(object):
    def setupUi(self, SceneTab):
        SceneTab.setObjectName("SceneTab")
        SceneTab.resize(166, 249)
        self.verticalLayout = QtWidgets.QVBoxLayout(SceneTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.opacityLayout = QtWidgets.QHBoxLayout()
        self.opacityLayout.setObjectName("opacityLayout")
        self.opacitySliderLabel = QtWidgets.QLabel(SceneTab)
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.opacitySliderLabel.setFont(font)
        self.opacitySliderLabel.setObjectName("opacitySliderLabel")
        self.opacityLayout.addWidget(self.opacitySliderLabel)
        self.opacitySlider = QtWidgets.QSlider(SceneTab)
        self.opacitySlider.setOrientation(QtCore.Qt.Horizontal)
        self.opacitySlider.setObjectName("opacitySlider")
        self.opacityLayout.addWidget(self.opacitySlider)
        self.verticalLayout.addLayout(self.opacityLayout)
        self.ImageTreeView = QtWidgets.QTreeView(SceneTab)
        self.ImageTreeView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.ImageTreeView.setObjectName("ImageTreeView")
        self.verticalLayout.addWidget(self.ImageTreeView)
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.buttonsLayout.setObjectName("buttonsLayout")
        self.addButton = QtWidgets.QToolButton(SceneTab)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-add_circle-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(icon)
        self.addButton.setIconSize(QtCore.QSize(24, 24))
        self.addButton.setObjectName("addButton")
        self.buttonsLayout.addWidget(self.addButton)
        self.upButton = QtWidgets.QToolButton(SceneTab)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-arrow_upward-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.upButton.setIcon(icon1)
        self.upButton.setIconSize(QtCore.QSize(24, 24))
        self.upButton.setObjectName("upButton")
        self.buttonsLayout.addWidget(self.upButton)
        self.downButton = QtWidgets.QToolButton(SceneTab)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-arrow_downward-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downButton.setIcon(icon2)
        self.downButton.setIconSize(QtCore.QSize(24, 24))
        self.downButton.setObjectName("downButton")
        self.buttonsLayout.addWidget(self.downButton)
        self.deleteButton = QtWidgets.QToolButton(SceneTab)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-delete-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon3)
        self.deleteButton.setIconSize(QtCore.QSize(24, 24))
        self.deleteButton.setObjectName("deleteButton")
        self.buttonsLayout.addWidget(self.deleteButton)
        self.verticalLayout.addLayout(self.buttonsLayout)

        self.retranslateUi(SceneTab)
        QtCore.QMetaObject.connectSlotsByName(SceneTab)

    def retranslateUi(self, SceneTab):
        _translate = QtCore.QCoreApplication.translate
        SceneTab.setWindowTitle(_translate("SceneTab", "Form"))
        self.opacitySliderLabel.setText(_translate("SceneTab", "Opacity"))
        self.addButton.setText(_translate("SceneTab", "..."))
        self.upButton.setText(_translate("SceneTab", "..."))
        self.downButton.setText(_translate("SceneTab", "..."))
        self.deleteButton.setText(_translate("SceneTab", "..."))
