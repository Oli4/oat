from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QWidget

from oat.models import RegistrationModel
from oat.views.ui import Ui_RegistrationManual


class RegistrationView(QWidget, Ui_RegistrationManual):
    def __init__(self, model: RegistrationModel, parent=None):
        """Initialize the components of the Toolbox subwindow."""
        self.model = model
        super().__init__(parent)
        self.setupUi(self)

        self.grabKeyboard()
        self.key_actions = {QtCore.Qt.Key_W: self.tableViewPoints.up,
                            QtCore.Qt.Key_A: self.tableViewPoints.last,
                            QtCore.Qt.Key_S: self.tableViewPoints.down,
                            QtCore.Qt.Key_D: self.tableViewPoints.next,
                            QtCore.Qt.Key_Tab: self.tableViewPoints.next}

        # Set table model
        self.tableViewPoints.setModel(self.model)
        self.tableViewPoints.setCurrentIndex(self.model.createIndex(0, 0))
        self.selectionModel = self.tableViewPoints.selectionModel()
        self.graphicsViewPointSelection.selectionModel = self.selectionModel
        self.tableViewPoints.selectionModel().currentChanged.connect(
            self.set_scenes)

        self.scenes = self.model.scenes

        self.graphicsViewPointSelection.setScene(self.scenes[0])
        self.graphicsViewPatch.setScene(self.scenes[1])

    @QtCore.pyqtSlot(QModelIndex, QModelIndex)
    def set_scenes(self, current_index: QModelIndex,
                   previous_index: QModelIndex):
        self.graphicsViewPointSelection.setScene(
            self.scenes[current_index.column()])
        self.graphicsViewPatch.setScene(
            self.scenes[previous_index.column()])

        try:
            self.graphicsViewPointSelection.centerOn(
                self.model.data(current_index, role=QtCore.Qt.EditRole))
        except:
            pass

        try:
            self.graphicsViewPatch.centerOn(
                self.model.data(previous_index, role=QtCore.Qt.EditRole))
        except:
            pass

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        try:
            self.key_actions[event.key()]()
        except:
            super().keyPressEvent(event)
