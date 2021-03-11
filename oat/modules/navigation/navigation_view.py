import logging

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QWidget

from oat.models import CollectionsModel
from oat.models.config import DATA_ROLE
from oat.views.ui.ui_data_overview import Ui_OverviewView

logger = logging.getLogger(__name__)


class NavigationView(QWidget, Ui_OverviewView):
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

    def toggle_buttons(self):
        data = self.model.data(self.tableView.selectionModel().currentIndex(), role=DATA_ROLE)
        if len(data["enfaceimages"]) > 0 or len(data["volumeimages"]) > 0:
            self.annotateButton.setEnabled(True)
        else:
            self.annotateButton.setEnabled(False)

        if len(data["enfaceimages"]) == 2:
            self.registerButton.setEnabled(True)
        else:
            self.registerButton.setEnabled(False)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        try:
            self.key_actions[event.key()]()
        except:
            super().keyPressEvent(event)
