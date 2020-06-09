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
        RegistrationManual.resize(500, 351)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            RegistrationManual.sizePolicy().hasHeightForWidth())
        RegistrationManual.setSizePolicy(sizePolicy)
        RegistrationManual.setMinimumSize(QtCore.QSize(500, 350))
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(RegistrationManual)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.graphicsViewPointSelection = FeatureSelectionView(
            RegistrationManual)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graphicsViewPointSelection.sizePolicy().hasHeightForWidth())
        self.graphicsViewPointSelection.setSizePolicy(sizePolicy)
        self.graphicsViewPointSelection.setMinimumSize(QtCore.QSize(250, 250))
        self.graphicsViewPointSelection.setBaseSize(QtCore.QSize(200, 200))
        self.graphicsViewPointSelection.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewPointSelection.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewPointSelection.setObjectName(
            "graphicsViewPointSelection")
        self.verticalLayout_3.addWidget(self.graphicsViewPointSelection)
        self.tableViewPoints = FeatureTableView(RegistrationManual)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tableViewPoints.sizePolicy().hasHeightForWidth())
        self.tableViewPoints.setSizePolicy(sizePolicy)
        self.tableViewPoints.setMinimumSize(QtCore.QSize(80, 50))
        self.tableViewPoints.setBaseSize(QtCore.QSize(0, 0))
        self.tableViewPoints.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.tableViewPoints.setObjectName("tableViewPoints")
        self.verticalLayout_3.addWidget(self.tableViewPoints)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.graphicsViewPatch = CustomGraphicsView(RegistrationManual)
        self.graphicsViewPatch.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graphicsViewPatch.sizePolicy().hasHeightForWidth())
        self.graphicsViewPatch.setSizePolicy(sizePolicy)
        self.graphicsViewPatch.setMinimumSize(QtCore.QSize(50, 50))
        self.graphicsViewPatch.setBaseSize(QtCore.QSize(150, 150))
        self.graphicsViewPatch.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewPatch.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewPatch.setObjectName("graphicsViewPatch")
        self.verticalLayout_2.addWidget(self.graphicsViewPatch)
        self.graphicsViewCheckerboard = CustomGraphicsView(RegistrationManual)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.graphicsViewCheckerboard.sizePolicy().hasHeightForWidth())
        self.graphicsViewCheckerboard.setSizePolicy(sizePolicy)
        self.graphicsViewCheckerboard.setMinimumSize(QtCore.QSize(50, 50))
        self.graphicsViewCheckerboard.setBaseSize(QtCore.QSize(150, 150))
        self.graphicsViewCheckerboard.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewCheckerboard.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewCheckerboard.setObjectName("graphicsViewCheckerboard")
        self.verticalLayout_2.addWidget(self.graphicsViewCheckerboard)
        self.label_2 = QtWidgets.QLabel(RegistrationManual)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.transformationDropdown = QtWidgets.QComboBox(RegistrationManual)
        self.transformationDropdown.setObjectName("transformationDropdown")
        self.transformationDropdown.addItem("")
        self.transformationDropdown.addItem("")
        self.verticalLayout_2.addWidget(self.transformationDropdown)
        self.label = QtWidgets.QLabel(RegistrationManual)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.gridSizeSlider = QtWidgets.QSlider(RegistrationManual)
        self.gridSizeSlider.setMinimum(10)
        self.gridSizeSlider.setMaximum(200)
        self.gridSizeSlider.setProperty("value", 50)
        self.gridSizeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.gridSizeSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.gridSizeSlider.setTickInterval(10)
        self.gridSizeSlider.setObjectName("gridSizeSlider")
        self.verticalLayout_2.addWidget(self.gridSizeSlider)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.retranslateUi(RegistrationManual)
        QtCore.QMetaObject.connectSlotsByName(RegistrationManual)

    def retranslateUi(self, RegistrationManual):
        _translate = QtCore.QCoreApplication.translate
        RegistrationManual.setWindowTitle(_translate("RegistrationManual", "Form"))
        self.label_2.setText(_translate("RegistrationManual", "Transformation Model"))
        self.transformationDropdown.setItemText(0, _translate("RegistrationManual", "Affine"))
        self.transformationDropdown.setItemText(1, _translate("RegistrationManual", "Similarity"))
        self.label.setText(_translate("RegistrationManual", "Gridsize"))


from oat.views.custom import CustomGraphicsView
from oat.views.registration import FeatureSelectionView, FeatureTableView
