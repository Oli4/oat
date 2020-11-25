# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_modality_entry.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ModalityEntry(object):
    def setupUi(self, ModalityEntry):
        ModalityEntry.setObjectName("ModalityEntry")
        ModalityEntry.resize(300, 40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ModalityEntry.sizePolicy().hasHeightForWidth())
        ModalityEntry.setSizePolicy(sizePolicy)
        ModalityEntry.setMinimumSize(QtCore.QSize(300, 40))
        ModalityEntry.setMaximumSize(QtCore.QSize(300, 40))
        ModalityEntry.setAutoFillBackground(True)
        self.horizontalLayoutWidget = QtWidgets.QWidget(ModalityEntry)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 291, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hideButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hideButton.sizePolicy().hasHeightForWidth())
        self.hideButton.setSizePolicy(sizePolicy)
        self.hideButton.setMinimumSize(QtCore.QSize(30, 30))
        self.hideButton.setMaximumSize(QtCore.QSize(30, 30))
        self.hideButton.setAutoFillBackground(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-visibility-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hideButton.setIcon(icon)
        self.hideButton.setIconSize(QtCore.QSize(24, 24))
        self.hideButton.setObjectName("hideButton")
        self.horizontalLayout.addWidget(self.hideButton)
        self.graphicsView = QtWidgets.QGraphicsView(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMinimumSize(QtCore.QSize(30, 30))
        self.graphicsView.setMaximumSize(QtCore.QSize(30, 30))
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setMaximumSize(QtCore.QSize(180, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.retranslateUi(ModalityEntry)
        QtCore.QMetaObject.connectSlotsByName(ModalityEntry)

    def retranslateUi(self, ModalityEntry):
        _translate = QtCore.QCoreApplication.translate
        ModalityEntry.setWindowTitle(_translate("ModalityEntry", "Form"))
        self.hideButton.setText(_translate("ModalityEntry", "..."))
        self.label.setText(_translate("ModalityEntry", "New Modality"))


from . import resources_rc
