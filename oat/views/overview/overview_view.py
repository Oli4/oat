import logging

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QWidget

from oat.models import CollectionsModel
from oat.models.config import DATA_ROLE
from oat.views.ui.ui_data_overview import Ui_OverviewView

logger = logging.getLogger(__name__)


class OverviewView(QWidget, Ui_OverviewView):
    def __init__(self, model: CollectionsModel, parent=None):
        """Initialize the components of the Toolbox subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.model = QtCore.QSortFilterProxyModel(self)
        self.model.setSourceModel(model)
        self.tableView.setModel(self.model)
        self.tableView.setSortingEnabled(True)

        filtered_columns = [x for x in range(self.model.columnCount())
                            if self.model.headerData(x, QtCore.Qt.Horizontal)
                            not in ["name", "patient_id", "registered"]]

        for i in filtered_columns:
            self.tableView.setColumnHidden(i, True)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.selectionModel().currentChanged.connect(
            self.toggle_buttons)

        self.toggle_buttons()

        # self.annotateButton.clicked.connect(self.annotate_collection)
        # self.registerButton.clicked.connect(self.register_collection)

        self.key_actions = {
            # QtCore.Qt.Key_W: self.tableView.up,
            # QtCore.Qt.Key_A: self.tableView.last,
            # QtCore.Qt.Key_S: self.tableView.down,
            # QtCore.Qt.Key_D: self.tableView.next,
            # QtCore.Qt.Key_Tab: self.tableView.next,
            # QtCore.Qt.Key_Backspace: self.tableView.delete_current_cell,
            # QtCore.Qt.Key_Delete: self.tableView.delete_current_row,
        }

        # Connect the parts

        # Set scenes: The first image is in the selection view and second in
        # patch view
        # self.scenes = self.model.scenes
        # self.set_scenes(self.model.createIndex(0, 0),
        #                self.model.createIndex(0, 1))

    def toggle_buttons(self):
        data = self.model.data(self.tableView.selectionModel().currentIndex(), role=DATA_ROLE)
        if len(data["enfaceimages"]) == 1 and len(data["volumeimages"]) == 1:
            self.annotateButton.setEnabled(True)
            self.registerButton.setEnabled(True)
        else:
            self.annotateButton.setEnabled(False)
            self.registerButton.setEnabled(False)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        # Make sure images are filling the view when Widget is opened
        pass
        # self.graphicsViewPointSelection.zoomToFit()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        pass
        # self.graphicsViewPointSelection.zoomToFit()

    @QtCore.pyqtSlot(QModelIndex, QModelIndex)
    def set_scenes(self, current_index: QModelIndex,
                   previous_index: QModelIndex):
        pass
        """
        :param current_index: The new model index.
        :param previous_index:
        :return:
        
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
        """

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        try:
            self.key_actions[event.key()]()
        except:
            super().keyPressEvent(event)
