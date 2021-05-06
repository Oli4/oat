# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_data_overview.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from  . import resources_rc

class Ui_OverviewView(object):
    def setupUi(self, OverviewView):
        if not OverviewView.objectName():
            OverviewView.setObjectName(u"OverviewView")
        OverviewView.resize(277, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OverviewView.sizePolicy().hasHeightForWidth())
        OverviewView.setSizePolicy(sizePolicy)
        OverviewView.setMinimumSize(QSize(200, 500))
        self.verticalLayout = QVBoxLayout(OverviewView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(OverviewView)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(6, -1, -1, -1)
        self.datasetComboBox = QComboBox(OverviewView)
        self.datasetComboBox.setObjectName(u"datasetComboBox")

        self.horizontalLayout_5.addWidget(self.datasetComboBox)

        self.editDatasetButton = QToolButton(OverviewView)
        self.editDatasetButton.setObjectName(u"editDatasetButton")
        icon = QIcon()
        icon.addFile(u":/icons/icons/baseline-settings-20px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.editDatasetButton.setIcon(icon)
        self.editDatasetButton.setIconSize(QSize(24, 24))

        self.horizontalLayout_5.addWidget(self.editDatasetButton)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_5)


        self.horizontalLayout.addLayout(self.formLayout)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line = QFrame(OverviewView)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_2 = QLabel(OverviewView)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.annotateButton = QPushButton(OverviewView)
        self.annotateButton.setObjectName(u"annotateButton")

        self.horizontalLayout_3.addWidget(self.annotateButton)

        self.registerButton = QPushButton(OverviewView)
        self.registerButton.setObjectName(u"registerButton")

        self.horizontalLayout_3.addWidget(self.registerButton)


        self.formLayout_2.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_3)


        self.verticalLayout_3.addLayout(self.formLayout_2)

        self.tableView = QTableView(OverviewView)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.horizontalHeader().setCascadingSectionResizes(True)

        self.verticalLayout_3.addWidget(self.tableView)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(OverviewView)

        QMetaObject.connectSlotsByName(OverviewView)
    # setupUi

    def retranslateUi(self, OverviewView):
        OverviewView.setWindowTitle(QCoreApplication.translate("OverviewView", u"Data Collections", None))
        self.label.setText(QCoreApplication.translate("OverviewView", u"Dataset:", None))
#if QT_CONFIG(tooltip)
        self.editDatasetButton.setToolTip(QCoreApplication.translate("OverviewView", u"Open the dataset manager", None))
#endif // QT_CONFIG(tooltip)
        self.editDatasetButton.setText(QCoreApplication.translate("OverviewView", u"...", None))
        self.label_2.setText(QCoreApplication.translate("OverviewView", u"Collections:", None))
#if QT_CONFIG(tooltip)
        self.annotateButton.setToolTip(QCoreApplication.translate("OverviewView", u"Annotate the selected collection", None))
#endif // QT_CONFIG(tooltip)
        self.annotateButton.setText(QCoreApplication.translate("OverviewView", u"Annotate", None))
#if QT_CONFIG(tooltip)
        self.registerButton.setToolTip(QCoreApplication.translate("OverviewView", u"Register the selected collection", None))
#endif // QT_CONFIG(tooltip)
        self.registerButton.setText(QCoreApplication.translate("OverviewView", u"Register", None))
#if QT_CONFIG(tooltip)
        self.tableView.setToolTip(QCoreApplication.translate("OverviewView", u"Collections in the current dataset", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

