# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_registration_manual.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_RegistrationManual(object):
    def setupUi(self, RegistrationManual):
        RegistrationManual.setObjectName("RegistrationManual")
        RegistrationManual.resize(580, 350)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            RegistrationManual.sizePolicy().hasHeightForWidth())
        RegistrationManual.setSizePolicy(sizePolicy)
        RegistrationManual.setMinimumSize(QtCore.QSize(580, 350))
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(RegistrationManual)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.graphicsViewPointSelection = FeatureSelectionView(
            RegistrationManual)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(
            self.graphicsViewPointSelection.sizePolicy().hasHeightForWidth())
        self.graphicsViewPointSelection.setSizePolicy(sizePolicy)
        self.graphicsViewPointSelection.setMinimumSize(QtCore.QSize(200, 200))
        self.graphicsViewPointSelection.setBaseSize(QtCore.QSize(200, 200))
        self.graphicsViewPointSelection.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewPointSelection.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewPointSelection.setObjectName(
            "graphicsViewPointSelection")
        self.verticalLayout_3.addWidget(self.graphicsViewPointSelection)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem)
        self.tableViewPoints = FeatureTableView(RegistrationManual)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.tableViewPoints.sizePolicy().hasHeightForWidth())
        self.tableViewPoints.setSizePolicy(sizePolicy)
        self.tableViewPoints.setMinimumSize(QtCore.QSize(100, 100))
        self.tableViewPoints.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tableViewPoints.setBaseSize(QtCore.QSize(0, 0))
        self.tableViewPoints.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.tableViewPoints.setObjectName("tableViewPoints")
        self.verticalLayout_3.addWidget(self.tableViewPoints)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(5, 20,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.graphicsViewPatch = CustomGraphicsView(RegistrationManual)
        self.graphicsViewPatch.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(200)
        sizePolicy.setHeightForWidth(
            self.graphicsViewPatch.sizePolicy().hasHeightForWidth())
        self.graphicsViewPatch.setSizePolicy(sizePolicy)
        self.graphicsViewPatch.setMinimumSize(QtCore.QSize(160, 150))
        self.graphicsViewPatch.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.graphicsViewPatch.setSizeIncrement(QtCore.QSize(0, 0))
        self.graphicsViewPatch.setBaseSize(QtCore.QSize(100, 100))
        self.graphicsViewPatch.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewPatch.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewPatch.setObjectName("graphicsViewPatch")
        self.horizontalLayout_5.addWidget(self.graphicsViewPatch)
        spacerItem2 = QtWidgets.QSpacerItem(5, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_3 = QtWidgets.QLabel(RegistrationManual)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(160, 0))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_5.addWidget(self.label_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        spacerItem3 = QtWidgets.QSpacerItem(20, 5,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.graphicsViewCheckerboard = CustomGraphicsView(RegistrationManual)
        self.graphicsViewCheckerboard.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(200)
        sizePolicy.setHeightForWidth(
            self.graphicsViewCheckerboard.sizePolicy().hasHeightForWidth())
        self.graphicsViewCheckerboard.setSizePolicy(sizePolicy)
        self.graphicsViewCheckerboard.setMinimumSize(QtCore.QSize(160, 150))
        self.graphicsViewCheckerboard.setMaximumSize(
            QtCore.QSize(16777215, 16777215))
        self.graphicsViewCheckerboard.setSizeIncrement(QtCore.QSize(0, 0))
        self.graphicsViewCheckerboard.setBaseSize(QtCore.QSize(100, 100))
        self.graphicsViewCheckerboard.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewCheckerboard.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewCheckerboard.setObjectName("graphicsViewCheckerboard")
        self.horizontalLayout_3.addWidget(self.graphicsViewCheckerboard)
        spacerItem4 = QtWidgets.QSpacerItem(5, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem5 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem5)
        self.label = QtWidgets.QLabel(RegistrationManual)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.gridSizeSlider = QtWidgets.QSlider(RegistrationManual)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gridSizeSlider.sizePolicy().hasHeightForWidth())
        self.gridSizeSlider.setSizePolicy(sizePolicy)
        self.gridSizeSlider.setMinimum(10)
        self.gridSizeSlider.setMaximum(200)
        self.gridSizeSlider.setSingleStep(10)
        self.gridSizeSlider.setProperty("value", 60)
        self.gridSizeSlider.setSliderPosition(60)
        self.gridSizeSlider.setTracking(True)
        self.gridSizeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.gridSizeSlider.setInvertedAppearance(False)
        self.gridSizeSlider.setInvertedControls(False)
        self.gridSizeSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.gridSizeSlider.setTickInterval(10)
        self.gridSizeSlider.setObjectName("gridSizeSlider")
        self.verticalLayout_4.addWidget(self.gridSizeSlider)
        self.label_2 = QtWidgets.QLabel(RegistrationManual)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(160, 0))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.transformationDropdown = QtWidgets.QComboBox(RegistrationManual)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.transformationDropdown.sizePolicy().hasHeightForWidth())
        self.transformationDropdown.setSizePolicy(sizePolicy)
        self.transformationDropdown.setObjectName("transformationDropdown")
        self.transformationDropdown.addItem("")
        self.transformationDropdown.addItem("")
        self.verticalLayout_4.addWidget(self.transformationDropdown)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.retranslateUi(RegistrationManual)
        QtCore.QMetaObject.connectSlotsByName(RegistrationManual)

    def retranslateUi(self, RegistrationManual):
        _translate = QtCore.QCoreApplication.translate
        RegistrationManual.setWindowTitle(
            _translate("RegistrationManual", "Form"))
        self.label.setText(_translate("RegistrationManual", "Gridsize"))
        self.label_2.setText(
            _translate("RegistrationManual", "Transformation Model"))
        self.transformationDropdown.setItemText(0,
                                                _translate("RegistrationManual",
                                                           "Similarity"))
        self.transformationDropdown.setItemText(1,
                                                _translate("RegistrationManual",
                                                           "Affine"))
from oat.views.custom import CustomGraphicsView
from oat.views.registration import FeatureSelectionView, FeatureTableView
