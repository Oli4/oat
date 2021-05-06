# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_datasetmanager_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from  . import resources_rc

class Ui_DatasetManagerDialog(object):
    def setupUi(self, DatasetManagerDialog):
        if not DatasetManagerDialog.objectName():
            DatasetManagerDialog.setObjectName(u"DatasetManagerDialog")
        DatasetManagerDialog.resize(622, 381)
        self.horizontalLayout = QHBoxLayout(DatasetManagerDialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label = QLabel(DatasetManagerDialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label.setFont(font)

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.addDatasetButton = QToolButton(DatasetManagerDialog)
        self.addDatasetButton.setObjectName(u"addDatasetButton")
        icon = QIcon()
        icon.addFile(u":/icons/icons/baseline-add_circle-24px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.addDatasetButton.setIcon(icon)
        self.addDatasetButton.setIconSize(QSize(24, 24))

        self.horizontalLayout_5.addWidget(self.addDatasetButton)

        self.deleteDatasetButton = QToolButton(DatasetManagerDialog)
        self.deleteDatasetButton.setObjectName(u"deleteDatasetButton")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/baseline-delete-24px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.deleteDatasetButton.setIcon(icon1)
        self.deleteDatasetButton.setIconSize(QSize(24, 24))

        self.horizontalLayout_5.addWidget(self.deleteDatasetButton)


        self.formLayout_3.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_5)


        self.verticalLayout_4.addLayout(self.formLayout_3)

        self.datasetTableView = QTableView(DatasetManagerDialog)
        self.datasetTableView.setObjectName(u"datasetTableView")
        self.datasetTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.datasetTableView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_4.addWidget(self.datasetTableView)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.frame = QFrame(DatasetManagerDialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout_2.addWidget(self.label_2)

        self.descriptionTextEdit = QTextEdit(self.frame)
        self.descriptionTextEdit.setObjectName(u"descriptionTextEdit")
        self.descriptionTextEdit.setAcceptRichText(True)

        self.verticalLayout_2.addWidget(self.descriptionTextEdit)


        self.horizontalLayout_6.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.addCollaboratorButton = QToolButton(self.frame)
        self.addCollaboratorButton.setObjectName(u"addCollaboratorButton")
        self.addCollaboratorButton.setIcon(icon)
        self.addCollaboratorButton.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.addCollaboratorButton)

        self.deleteCollaboratorButton = QToolButton(self.frame)
        self.deleteCollaboratorButton.setObjectName(u"deleteCollaboratorButton")
        self.deleteCollaboratorButton.setIcon(icon1)
        self.deleteCollaboratorButton.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.deleteCollaboratorButton)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_3)


        self.verticalLayout_3.addLayout(self.formLayout)

        self.collaboratorsTableView = QTableView(self.frame)
        self.collaboratorsTableView.setObjectName(u"collaboratorsTableView")
        self.collaboratorsTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.collaboratorsTableView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_3.addWidget(self.collaboratorsTableView)

        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.addCollectionButton = QToolButton(self.frame)
        self.addCollectionButton.setObjectName(u"addCollectionButton")
        self.addCollectionButton.setIcon(icon)
        self.addCollectionButton.setIconSize(QSize(24, 24))

        self.horizontalLayout_4.addWidget(self.addCollectionButton)

        self.deleteCollectionButton = QToolButton(self.frame)
        self.deleteCollectionButton.setObjectName(u"deleteCollectionButton")
        self.deleteCollectionButton.setIcon(icon1)
        self.deleteCollectionButton.setIconSize(QSize(24, 24))

        self.horizontalLayout_4.addWidget(self.deleteCollectionButton)


        self.formLayout_2.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_4)


        self.verticalLayout_3.addLayout(self.formLayout_2)

        self.collectionsTableView = QTableView(self.frame)
        self.collectionsTableView.setObjectName(u"collectionsTableView")
        self.collectionsTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.collectionsTableView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_3.addWidget(self.collectionsTableView)


        self.horizontalLayout_6.addLayout(self.verticalLayout_3)


        self.horizontalLayout_2.addWidget(self.frame)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(DatasetManagerDialog)

        QMetaObject.connectSlotsByName(DatasetManagerDialog)
    # setupUi

    def retranslateUi(self, DatasetManagerDialog):
        DatasetManagerDialog.setWindowTitle(QCoreApplication.translate("DatasetManagerDialog", u"Dataset Manager", None))
        self.label.setText(QCoreApplication.translate("DatasetManagerDialog", u"Datasets:", None))
#if QT_CONFIG(tooltip)
        self.addDatasetButton.setToolTip(QCoreApplication.translate("DatasetManagerDialog", u"Add a new dataset", None))
#endif // QT_CONFIG(tooltip)
        self.addDatasetButton.setText(QCoreApplication.translate("DatasetManagerDialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.deleteDatasetButton.setToolTip(QCoreApplication.translate("DatasetManagerDialog", u"Delete the selected dataset", None))
#endif // QT_CONFIG(tooltip)
        self.deleteDatasetButton.setText(QCoreApplication.translate("DatasetManagerDialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.datasetTableView.setToolTip(QCoreApplication.translate("DatasetManagerDialog", u"All datasets you can manage", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("DatasetManagerDialog", u"Description:", None))
#if QT_CONFIG(tooltip)
        self.descriptionTextEdit.setToolTip(QCoreApplication.translate("DatasetManagerDialog", u"Description of the current dataset", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("DatasetManagerDialog", u"Collaborators:", None))
#if QT_CONFIG(tooltip)
        self.addCollaboratorButton.setToolTip(QCoreApplication.translate("DatasetManagerDialog", u"Add a collaborator to the current dataset", None))
#endif // QT_CONFIG(tooltip)
        self.addCollaboratorButton.setText(QCoreApplication.translate("DatasetManagerDialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.deleteCollaboratorButton.setToolTip(QCoreApplication.translate("DatasetManagerDialog", u"Remove a collaborator from the current dataset", None))
#endif // QT_CONFIG(tooltip)
        self.deleteCollaboratorButton.setText(QCoreApplication.translate("DatasetManagerDialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.collaboratorsTableView.setToolTip(QCoreApplication.translate("DatasetManagerDialog", u"Collaborators have access to the respective dataset", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("DatasetManagerDialog", u"Collections:", None))
#if QT_CONFIG(tooltip)
        self.addCollectionButton.setToolTip(QCoreApplication.translate("DatasetManagerDialog", u"Add collection to current dataset", None))
#endif // QT_CONFIG(tooltip)
        self.addCollectionButton.setText(QCoreApplication.translate("DatasetManagerDialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.deleteCollectionButton.setToolTip(QCoreApplication.translate("DatasetManagerDialog", u"Remove collection from current dataset", None))
#endif // QT_CONFIG(tooltip)
        self.deleteCollectionButton.setText(QCoreApplication.translate("DatasetManagerDialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.collectionsTableView.setToolTip(QCoreApplication.translate("DatasetManagerDialog", u"Collections in the curent dataset", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

