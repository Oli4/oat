import logging


from PySide6 import QtCore, QtGui, QtWidgets

from oat.models.config import DATA_ROLE, ID_ROLE, EMPTY_ROLE
from oat.views.ui.ui_data_overview import Ui_OverviewView
from oat.modules.dialogs.datasetmanager import DatasetManagerDialog

logger = logging.getLogger(__name__)

class CustomQSortFilterProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.dataset_id = None

    def filterAcceptsRow(self, source_row: int, source_parent: QtCore.QModelIndex) -> bool:
        accept_row = True
        index = self.sourceModel().index(source_row, 0, source_parent)
        data = self.sourceModel().data(index, DATA_ROLE)
        if len(data["enfaceimage_ids"] + data["volumeimage_ids"]) == 0:
            accept_row = False
        if self.dataset_id is not None:
            if self.dataset_id not in data["dataset_ids"]:
                accept_row = False

        return accept_row

    def filterAcceptsColumn(self, source_column:int, source_parent:QtCore.QModelIndex) -> bool:
        header = self.sourceModel().headerData(source_column, QtCore.Qt.Horizontal)
        if header in ["Name", "Laterality", "Patient Pseudonym"]:
            return True
        else:
            return False

class NavigationView(QtWidgets.QWidget, Ui_OverviewView):
    def __init__(self, models, parent=None):
        """Initialize the components of the Toolbox subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.datasets_model = models["datasets"]
        self.collections_model = models["collections"]

        self.model = CustomQSortFilterProxyModel(self)
        self.model.setSourceModel(self.collections_model)


        self.tableView.setModel(self.model)
        self.tableView.setSortingEnabled(True)

        self.tableView.verticalHeader().setVisible(False)
        self.tableView.selectionModel().currentChanged.connect(
            self.toggle_buttons)

        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
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

        self.datasetComboBox.setModel(self.datasets_model)
        self.datasetComboBox.currentIndexChanged.connect(self.update_collections)
        self.update_collections()

        self.editDatasetButton.clicked.connect(self.open_dataset_manager)

        #self.context_menu = QtWidgets.QMenu()
        delete_action = QtGui.QAction("Remove", self.tableView)
        delete_action.triggered.connect(self.delete_collection)
        self.tableView.addAction(delete_action)

    def delete_collection(self):
        self.model.removeRow(self.tableView.currentIndex().row(), QtCore.QModelIndex())

    def update_collections(self):
        self.model.dataset_id = int(self.datasetComboBox.currentData(role=ID_ROLE))
        self.model.invalidate()

    def open_dataset_manager(self):


        dialog = DatasetManagerDialog(self.datasets_model)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.datasets_model.layoutChanged.emit()

    def toggle_buttons(self):
        data = self.model.data(self.tableView.selectionModel().currentIndex(), role=DATA_ROLE)
        if len(data["enfaceimage_ids"]) > 0 or len(data["volumeimage_ids"]) > 0:
            self.annotateButton.setEnabled(True)
        else:
            self.annotateButton.setEnabled(False)

        if len(data["enfaceimage_ids"]) == 2:
            self.registerButton.setEnabled(True)
        else:
            self.registerButton.setEnabled(False)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        try:
            self.key_actions[event.key()]()
        except:
            super().keyPressEvent(event)
