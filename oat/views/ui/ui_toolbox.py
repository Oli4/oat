# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_toolbox.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from  . import resources_rc

class Ui_Toolbox(object):
    def setupUi(self, Toolbox):
        if not Toolbox.objectName():
            Toolbox.setObjectName(u"Toolbox")
        Toolbox.resize(296, 505)
        Toolbox.setMinimumSize(QSize(250, 470))
        self.verticalLayout = QVBoxLayout(Toolbox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(Toolbox)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_3)

        self.tabWidget = QTabWidget(self.widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setElideMode(Qt.ElideNone)
        self.layers2d = QWidget()
        self.layers2d.setObjectName(u"layers2d")
        self.verticalLayout_3 = QVBoxLayout(self.layers2d)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.opacitySliderLabel_2d = QLabel(self.layers2d)
        self.opacitySliderLabel_2d.setObjectName(u"opacitySliderLabel_2d")

        self.verticalLayout_3.addWidget(self.opacitySliderLabel_2d)

        self.opacitySlider_2d = QSlider(self.layers2d)
        self.opacitySlider_2d.setObjectName(u"opacitySlider_2d")
        self.opacitySlider_2d.setOrientation(Qt.Horizontal)

        self.verticalLayout_3.addWidget(self.opacitySlider_2d)

        self.ModalityTreeView_2d = QTreeView(self.layers2d)
        self.ModalityTreeView_2d.setObjectName(u"ModalityTreeView_2d")
        self.ModalityTreeView_2d.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_3.addWidget(self.ModalityTreeView_2d)

        self.horizontalLayout_2d = QHBoxLayout()
        self.horizontalLayout_2d.setObjectName(u"horizontalLayout_2d")
        self.addButton_2d = QToolButton(self.layers2d)
        self.addButton_2d.setObjectName(u"addButton_2d")
        icon = QIcon()
        icon.addFile(u":/icons/icons/baseline-add_circle-24px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.addButton_2d.setIcon(icon)
        self.addButton_2d.setIconSize(QSize(24, 24))

        self.horizontalLayout_2d.addWidget(self.addButton_2d)

        self.upButton_2d = QToolButton(self.layers2d)
        self.upButton_2d.setObjectName(u"upButton_2d")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/baseline-arrow_upward-24px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.upButton_2d.setIcon(icon1)
        self.upButton_2d.setIconSize(QSize(24, 24))

        self.horizontalLayout_2d.addWidget(self.upButton_2d)

        self.downButton_2d = QToolButton(self.layers2d)
        self.downButton_2d.setObjectName(u"downButton_2d")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/baseline-arrow_downward-24px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.downButton_2d.setIcon(icon2)
        self.downButton_2d.setIconSize(QSize(24, 24))

        self.horizontalLayout_2d.addWidget(self.downButton_2d)

        self.deleteButton_2d = QToolButton(self.layers2d)
        self.deleteButton_2d.setObjectName(u"deleteButton_2d")
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/baseline-delete-24px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.deleteButton_2d.setIcon(icon3)
        self.deleteButton_2d.setIconSize(QSize(24, 24))

        self.horizontalLayout_2d.addWidget(self.deleteButton_2d)

        self.registerButton_2d = QToolButton(self.layers2d)
        self.registerButton_2d.setObjectName(u"registerButton_2d")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/baseline-filter-none-24px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.registerButton_2d.setIcon(icon4)
        self.registerButton_2d.setIconSize(QSize(24, 24))

        self.horizontalLayout_2d.addWidget(self.registerButton_2d)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2d)

        self.tabWidget.addTab(self.layers2d, "")
        self.layers3d = QWidget()
        self.layers3d.setObjectName(u"layers3d")
        self.verticalLayout_6 = QVBoxLayout(self.layers3d)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.opacitySliderLabel_3d = QLabel(self.layers3d)
        self.opacitySliderLabel_3d.setObjectName(u"opacitySliderLabel_3d")

        self.verticalLayout_6.addWidget(self.opacitySliderLabel_3d)

        self.opacitySlider_3d = QSlider(self.layers3d)
        self.opacitySlider_3d.setObjectName(u"opacitySlider_3d")
        self.opacitySlider_3d.setOrientation(Qt.Horizontal)

        self.verticalLayout_6.addWidget(self.opacitySlider_3d)

        self.ModalityTreeView_3d = QTreeView(self.layers3d)
        self.ModalityTreeView_3d.setObjectName(u"ModalityTreeView_3d")
        self.ModalityTreeView_3d.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_6.addWidget(self.ModalityTreeView_3d)

        self.horizontalLayout_3d = QHBoxLayout()
        self.horizontalLayout_3d.setObjectName(u"horizontalLayout_3d")
        self.addButton_3d = QToolButton(self.layers3d)
        self.addButton_3d.setObjectName(u"addButton_3d")
        self.addButton_3d.setIcon(icon)
        self.addButton_3d.setIconSize(QSize(24, 24))
        self.addButton_3d.setArrowType(Qt.NoArrow)

        self.horizontalLayout_3d.addWidget(self.addButton_3d)

        self.upButton_3d = QToolButton(self.layers3d)
        self.upButton_3d.setObjectName(u"upButton_3d")
        self.upButton_3d.setIcon(icon1)
        self.upButton_3d.setIconSize(QSize(24, 24))

        self.horizontalLayout_3d.addWidget(self.upButton_3d)

        self.downButton_3d = QToolButton(self.layers3d)
        self.downButton_3d.setObjectName(u"downButton_3d")
        self.downButton_3d.setIcon(icon2)
        self.downButton_3d.setIconSize(QSize(24, 24))

        self.horizontalLayout_3d.addWidget(self.downButton_3d)

        self.deleteButton_3d = QToolButton(self.layers3d)
        self.deleteButton_3d.setObjectName(u"deleteButton_3d")
        self.deleteButton_3d.setIcon(icon3)
        self.deleteButton_3d.setIconSize(QSize(24, 24))

        self.horizontalLayout_3d.addWidget(self.deleteButton_3d)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3d)

        self.tabWidget.addTab(self.layers3d, "")

        self.verticalLayout_2.addWidget(self.tabWidget, 0, Qt.AlignTop)


        self.verticalLayout.addWidget(self.widget)

        self.line = QFrame(Toolbox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.widget_3 = QWidget(Toolbox)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_7 = QVBoxLayout(self.widget_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 0))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_2)

        self.widget_2 = QWidget(self.widget_3)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.toolButton_8 = QToolButton(self.widget_2)
        self.toolButton_8.setObjectName(u"toolButton_8")
        self.toolButton_8.setIconSize(QSize(24, 24))

        self.gridLayout.addWidget(self.toolButton_8, 1, 3, 1, 1)

        self.toolButton_11 = QToolButton(self.widget_2)
        self.toolButton_11.setObjectName(u"toolButton_11")
        self.toolButton_11.setIconSize(QSize(24, 24))

        self.gridLayout.addWidget(self.toolButton_11, 2, 2, 1, 1)

        self.penButton = QToolButton(self.widget_2)
        self.penButton.setObjectName(u"penButton")
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/baseline-edit-24px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.penButton.setIcon(icon5)
        self.penButton.setIconSize(QSize(24, 24))

        self.gridLayout.addWidget(self.penButton, 1, 0, 1, 1)

        self.toolButton_10 = QToolButton(self.widget_2)
        self.toolButton_10.setObjectName(u"toolButton_10")
        self.toolButton_10.setIconSize(QSize(24, 24))

        self.gridLayout.addWidget(self.toolButton_10, 2, 1, 1, 1)

        self.toolButton_9 = QToolButton(self.widget_2)
        self.toolButton_9.setObjectName(u"toolButton_9")
        self.toolButton_9.setIconSize(QSize(24, 24))

        self.gridLayout.addWidget(self.toolButton_9, 2, 0, 1, 1)

        self.toolButton_7 = QToolButton(self.widget_2)
        self.toolButton_7.setObjectName(u"toolButton_7")
        self.toolButton_7.setIconSize(QSize(24, 24))

        self.gridLayout.addWidget(self.toolButton_7, 1, 1, 1, 1)

        self.toolButton_6 = QToolButton(self.widget_2)
        self.toolButton_6.setObjectName(u"toolButton_6")
        self.toolButton_6.setIconSize(QSize(24, 24))

        self.gridLayout.addWidget(self.toolButton_6, 1, 2, 1, 1)

        self.toolButton_12 = QToolButton(self.widget_2)
        self.toolButton_12.setObjectName(u"toolButton_12")
        self.toolButton_12.setIconSize(QSize(24, 24))

        self.gridLayout.addWidget(self.toolButton_12, 2, 3, 1, 1)


        self.verticalLayout_7.addWidget(self.widget_2)


        self.verticalLayout.addWidget(self.widget_3, 0, Qt.AlignTop)


        self.retranslateUi(Toolbox)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Toolbox)
    # setupUi

    def retranslateUi(self, Toolbox):
        Toolbox.setWindowTitle(QCoreApplication.translate("Toolbox", u"Form", None))
#if QT_CONFIG(accessibility)
        Toolbox.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.label_3.setText(QCoreApplication.translate("Toolbox", u"Layers", None))
        self.opacitySliderLabel_2d.setText(QCoreApplication.translate("Toolbox", u"Opacity", None))
        self.addButton_2d.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.upButton_2d.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.downButton_2d.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.deleteButton_2d.setText(QCoreApplication.translate("Toolbox", u"...", None))
#if QT_CONFIG(tooltip)
        self.registerButton_2d.setToolTip(QCoreApplication.translate("Toolbox", u"Register selected images", None))
#endif // QT_CONFIG(tooltip)
        self.registerButton_2d.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.layers2d), QCoreApplication.translate("Toolbox", u"2D", None))
        self.opacitySliderLabel_3d.setText(QCoreApplication.translate("Toolbox", u"Opacity", None))
        self.addButton_3d.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.upButton_3d.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.downButton_3d.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.deleteButton_3d.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.layers3d), QCoreApplication.translate("Toolbox", u"3D", None))
        self.label_2.setText(QCoreApplication.translate("Toolbox", u"Tools", None))
        self.toolButton_8.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.toolButton_11.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.penButton.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.toolButton_10.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.toolButton_9.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.toolButton_7.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.toolButton_6.setText(QCoreApplication.translate("Toolbox", u"...", None))
        self.toolButton_12.setText(QCoreApplication.translate("Toolbox", u"...", None))
    # retranslateUi

