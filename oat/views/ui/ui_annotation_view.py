# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_annotation_view.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from  . import resources_rc

class Ui_AnnotationView(object):
    def setupUi(self, AnnotationView):
        if not AnnotationView.objectName():
            AnnotationView.setObjectName(u"AnnotationView")
        AnnotationView.resize(856, 488)
        self.horizontalLayout = QHBoxLayout(AnnotationView)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.data_widget = QWidget(AnnotationView)
        self.data_widget.setObjectName(u"data_widget")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(200)
        sizePolicy.setHeightForWidth(self.data_widget.sizePolicy().hasHeightForWidth())
        self.data_widget.setSizePolicy(sizePolicy)
        self.data_widget.setAutoFillBackground(False)
        self.data_widget.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.data_widget)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.addWidget(self.data_widget)

        self.widget_2 = QWidget(AnnotationView)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.layerOverview = QTabWidget(self.widget_2)
        self.layerOverview.setObjectName(u"layerOverview")
        sizePolicy1.setHeightForWidth(self.layerOverview.sizePolicy().hasHeightForWidth())
        self.layerOverview.setSizePolicy(sizePolicy1)
        self.layerOverview.setMinimumSize(QSize(170, 250))
        self.layerOverview.setElideMode(Qt.ElideNone)

        self.verticalLayout_2.addWidget(self.layerOverview)


        self.horizontalLayout.addWidget(self.widget_2)


        self.retranslateUi(AnnotationView)

        self.layerOverview.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(AnnotationView)
    # setupUi

    def retranslateUi(self, AnnotationView):
        AnnotationView.setWindowTitle(QCoreApplication.translate("AnnotationView", u"Multimodal Annotation", None))
    # retranslateUi

