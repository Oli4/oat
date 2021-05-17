# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_registration_manual.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from oat.modules.registration.views.featuretable_view import FeatureTableView
from oat.modules.registration.views.featureselection_view import FeatureSelectionView
from oat.modules.registration.views.graphicsview import CustomGraphicsView

from  . import resources_rc

class Ui_RegistrationManual(object):
    def setupUi(self, RegistrationManual):
        if not RegistrationManual.objectName():
            RegistrationManual.setObjectName(u"RegistrationManual")
        RegistrationManual.resize(820, 490)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RegistrationManual.sizePolicy().hasHeightForWidth())
        RegistrationManual.setSizePolicy(sizePolicy)
        RegistrationManual.setMinimumSize(QSize(820, 490))
        self.horizontalLayout_4 = QHBoxLayout(RegistrationManual)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.graphicsViewPointSelection = FeatureSelectionView(RegistrationManual)
        self.graphicsViewPointSelection.setObjectName(u"graphicsViewPointSelection")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(50)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.graphicsViewPointSelection.sizePolicy().hasHeightForWidth())
        self.graphicsViewPointSelection.setSizePolicy(sizePolicy1)
        self.graphicsViewPointSelection.setMinimumSize(QSize(300, 300))
        self.graphicsViewPointSelection.setBaseSize(QSize(200, 200))
        self.graphicsViewPointSelection.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsViewPointSelection.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.horizontalLayout.addWidget(self.graphicsViewPointSelection)

        self.horizontalSpacer = QSpacerItem(2, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.graphicsViewCheckerboard = CustomGraphicsView(RegistrationManual)
        self.graphicsViewCheckerboard.setObjectName(u"graphicsViewCheckerboard")
        self.graphicsViewCheckerboard.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.graphicsViewCheckerboard.sizePolicy().hasHeightForWidth())
        self.graphicsViewCheckerboard.setSizePolicy(sizePolicy1)
        self.graphicsViewCheckerboard.setMinimumSize(QSize(300, 300))
        self.graphicsViewCheckerboard.setMaximumSize(QSize(16777215, 16777215))
        self.graphicsViewCheckerboard.setSizeIncrement(QSize(0, 0))
        self.graphicsViewCheckerboard.setBaseSize(QSize(200, 200))
        self.graphicsViewCheckerboard.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsViewCheckerboard.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.horizontalLayout.addWidget(self.graphicsViewCheckerboard)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(2, 2, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.graphicsViewPatch = CustomGraphicsView(RegistrationManual)
        self.graphicsViewPatch.setObjectName(u"graphicsViewPatch")
        self.graphicsViewPatch.setEnabled(True)
        sizePolicy.setHeightForWidth(self.graphicsViewPatch.sizePolicy().hasHeightForWidth())
        self.graphicsViewPatch.setSizePolicy(sizePolicy)
        self.graphicsViewPatch.setMinimumSize(QSize(150, 150))
        self.graphicsViewPatch.setMaximumSize(QSize(150, 150))
        self.graphicsViewPatch.setSizeIncrement(QSize(0, 0))
        self.graphicsViewPatch.setBaseSize(QSize(100, 100))
        self.graphicsViewPatch.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsViewPatch.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.horizontalLayout_5.addWidget(self.graphicsViewPatch)

        self.horizontalSpacer_2 = QSpacerItem(2, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.tableViewPoints = FeatureTableView(RegistrationManual)
        self.tableViewPoints.setObjectName(u"tableViewPoints")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableViewPoints.sizePolicy().hasHeightForWidth())
        self.tableViewPoints.setSizePolicy(sizePolicy2)
        self.tableViewPoints.setMinimumSize(QSize(300, 100))
        self.tableViewPoints.setMaximumSize(QSize(16777215, 150))
        self.tableViewPoints.setBaseSize(QSize(0, 0))
        self.tableViewPoints.setSelectionMode(QAbstractItemView.SingleSelection)

        self.horizontalLayout_5.addWidget(self.tableViewPoints)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.horizontalSpacer_3 = QSpacerItem(2, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(RegistrationManual)
        self.label.setObjectName(u"label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy3)

        self.verticalLayout_4.addWidget(self.label)

        self.gridSizeSlider = QSlider(RegistrationManual)
        self.gridSizeSlider.setObjectName(u"gridSizeSlider")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.gridSizeSlider.sizePolicy().hasHeightForWidth())
        self.gridSizeSlider.setSizePolicy(sizePolicy4)
        self.gridSizeSlider.setMinimum(10)
        self.gridSizeSlider.setMaximum(200)
        self.gridSizeSlider.setSingleStep(10)
        self.gridSizeSlider.setValue(60)
        self.gridSizeSlider.setSliderPosition(60)
        self.gridSizeSlider.setTracking(True)
        self.gridSizeSlider.setOrientation(Qt.Horizontal)
        self.gridSizeSlider.setInvertedAppearance(False)
        self.gridSizeSlider.setInvertedControls(False)
        self.gridSizeSlider.setTickPosition(QSlider.TicksBelow)
        self.gridSizeSlider.setTickInterval(10)

        self.verticalLayout_4.addWidget(self.gridSizeSlider)

        self.label_2 = QLabel(RegistrationManual)
        self.label_2.setObjectName(u"label_2")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy5)
        self.label_2.setMinimumSize(QSize(160, 0))

        self.verticalLayout_4.addWidget(self.label_2)

        self.transformationDropdown = QComboBox(RegistrationManual)
        self.transformationDropdown.addItem("")
        self.transformationDropdown.addItem("")
        self.transformationDropdown.setObjectName(u"transformationDropdown")
        sizePolicy4.setHeightForWidth(self.transformationDropdown.sizePolicy().hasHeightForWidth())
        self.transformationDropdown.setSizePolicy(sizePolicy4)

        self.verticalLayout_4.addWidget(self.transformationDropdown)

        self.exportButton = QToolButton(RegistrationManual)
        self.exportButton.setObjectName(u"exportButton")
        sizePolicy4.setHeightForWidth(self.exportButton.sizePolicy().hasHeightForWidth())
        self.exportButton.setSizePolicy(sizePolicy4)

        self.verticalLayout_4.addWidget(self.exportButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)


        self.retranslateUi(RegistrationManual)

        QMetaObject.connectSlotsByName(RegistrationManual)
    # setupUi

    def retranslateUi(self, RegistrationManual):
        RegistrationManual.setWindowTitle(QCoreApplication.translate("RegistrationManual", u"Form", None))
        self.label.setText(QCoreApplication.translate("RegistrationManual", u"Gridsize", None))
        self.label_2.setText(QCoreApplication.translate("RegistrationManual", u"Transformation Model", None))
        self.transformationDropdown.setItemText(0, QCoreApplication.translate("RegistrationManual", u"Similarity", None))
        self.transformationDropdown.setItemText(1, QCoreApplication.translate("RegistrationManual", u"Affine", None))

        self.exportButton.setText(QCoreApplication.translate("RegistrationManual", u"Export", None))
    # retranslateUi

