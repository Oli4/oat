# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_3d_viewer.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Viewer3D(object):
    def setupUi(self, Viewer3D):
        Viewer3D.setObjectName("Viewer3D")
        Viewer3D.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Viewer3D)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.graphicsView3D = CustomGraphicsView(Viewer3D)
        self.graphicsView3D.setMinimumSize(QtCore.QSize(400, 400))
        self.graphicsView3D.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView3D.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView3D.setObjectName("graphicsView3D")
        self.verticalLayout_2.addWidget(self.graphicsView3D)
        self.spinBox = QtWidgets.QSpinBox(Viewer3D)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout_2.addWidget(self.spinBox)

        self.retranslateUi(Viewer3D)
        QtCore.QMetaObject.connectSlotsByName(Viewer3D)

    def retranslateUi(self, Viewer3D):
        _translate = QtCore.QCoreApplication.translate
        Viewer3D.setWindowTitle(_translate("Viewer3D", "Form"))
from oat.views.custom import CustomGraphicsView
