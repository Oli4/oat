# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_2d_viewer.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Viewer2D(object):
    def setupUi(self, Viewer2D):
        Viewer2D.setObjectName("Viewer2D")
        Viewer2D.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Viewer2D)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsView2D = QtWidgets.QGraphicsView(Viewer2D)
        self.graphicsView2D.setObjectName("graphicsView2D")
        self.verticalLayout.addWidget(self.graphicsView2D)

        self.retranslateUi(Viewer2D)
        QtCore.QMetaObject.connectSlotsByName(Viewer2D)

    def retranslateUi(self, Viewer2D):
        _translate = QtCore.QCoreApplication.translate
        Viewer2D.setWindowTitle(_translate("Viewer2D", "Form"))


