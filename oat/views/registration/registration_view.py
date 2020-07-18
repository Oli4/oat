import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QWidget

from oat.models import RegistrationModel
from oat.models.config import POINT_ROLE
from oat.views.ui.ui_registration_manual import Ui_RegistrationManual

logger = logging.getLogger(__name__)


class RegistrationView(QWidget, Ui_RegistrationManual):
    def __init__(self, model: RegistrationModel, parent=None):
        """Initialize the components of the Toolbox subwindow."""
        self.model = model
        super().__init__(parent)
        self.setupUi(self)

        self.key_actions = {
            QtCore.Qt.Key_W: self.tableViewPoints.up,
            QtCore.Qt.Key_A: self.tableViewPoints.last,
            QtCore.Qt.Key_S: self.tableViewPoints.down,
            QtCore.Qt.Key_D: self.tableViewPoints.next,
            QtCore.Qt.Key_Tab: self.tableViewPoints.next,
            QtCore.Qt.Key_Backspace: self.tableViewPoints.delete_current_cell,
            QtCore.Qt.Key_Delete: self.tableViewPoints.delete_current_row,
        }

        # Connect the parts
        self.tableViewPoints.setModel(self.model)
        self.tableViewPoints.setCurrentIndex(self.model.createIndex(0, 0))
        self.tableViewPoints.selectionModel().currentChanged.connect(
            self.set_scenes)
        self.graphicsViewPointSelection.featureChanged.connect(
            self.add_feature)
        self.transformationDropdown.currentTextChanged.connect(
            self.change_tmodel)
        self.gridSizeSlider.valueChanged.connect(self.change_checkerboard_size)

        # Set scenes: The first image is in the selection view and second in
        # patch view
        self.scenes = self.model.scenes
        self.set_scenes(self.model.createIndex(0, 0),
                        self.model.createIndex(0, 1))

        self.graphicsViewCheckerboard.setTransformationAnchor(
            QtWidgets.QGraphicsView.AnchorUnderMouse)

    def add_feature(self, feature: QtCore.QPoint):
        self.model.setData(self.tableViewPoints.selectionModel().currentIndex(),
                           feature, role=QtCore.Qt.EditRole)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        # Make sure images are filling the view when Widget is opened
        self.graphicsViewPointSelection.zoomToFit()
        self.graphicsViewPatch.zoomToFit()
        self.graphicsViewCheckerboard.zoomToFit()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.graphicsViewPointSelection.zoomToFit()
        self.graphicsViewPatch.zoomToFit()
        self.graphicsViewCheckerboard.zoomToFit()

    @QtCore.pyqtSlot(int)
    def change_checkerboard_size(self, size):
        self.model.checkerboard_size = size

    @QtCore.pyqtSlot(str)
    def change_tmodel(self, tmodel):
        self.model.tmodel = tmodel.lower()
        self.model.update_checkerboard()

    def center_PointSelection(self, point):
        if point:
            self.graphicsViewPointSelection.zoomToFeature()
            self.graphicsViewPointSelection.centerOn(point)
        else:
            self.graphicsViewPointSelection.zoomToFit()

    def center_Patch(self, point):
        if point:
            self.graphicsViewPatch.zoomToFeature()
            self.graphicsViewPatch.centerOn(point)
        else:
            self.graphicsViewPatch.zoomToFit()

    def match_changed(self, current_index, previous_index):
        """ Return False if model row is the same and True otherwise"""
        if previous_index.row() == current_index.row():
            return False
        else:
            return True

    def modality_changed(self, current_index, previous_index):
        """ Return False if model column is the same and True otherwise"""
        if previous_index.column() == current_index.column():
            return False
        else:
            return True

    @QtCore.pyqtSlot(QModelIndex, QModelIndex)
    def set_scenes(self, current_index: QModelIndex,
                   previous_index: QModelIndex):
        """
        :param current_index: The new model index.
        :param previous_index:
        :return:
        """
        self.graphicsViewCheckerboard.setScene(self.scenes[-1])
        self.graphicsViewCheckerboard.zoomToFit()

        feat1_index = current_index

        # Find out which image to show in the patch view
        if self.match_changed(current_index, previous_index):
            if self.modality_changed(current_index, previous_index):
                feat2_index = self.model.createIndex(current_index.row(),
                                                     previous_index.column())
            else:
                feat2_index = self.model.createIndex(
                    current_index.row(), self.graphicsViewPatch.scene().column)
        else:
            feat2_index = previous_index

        # Set GraphicsViewPointSelection to current Index
        self.graphicsViewPointSelection.setScene(
            self.scenes[feat1_index.column()])
        self.center_PointSelection(self.model.data(feat1_index,
                                                   role=POINT_ROLE))

        self.graphicsViewPatch.setScene(self.scenes[feat2_index.column()])
        self.center_Patch(self.model.data(feat2_index,
                                          role=POINT_ROLE))


    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        try:
            self.key_actions[event.key()]()
        except:
            super().keyPressEvent(event)
