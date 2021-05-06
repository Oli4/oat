import logging


from PySide6 import QtCore, QtGui, QtWidgets

from oat.models.config import DATA_ROLE, ID_ROLE, EMPTY_ROLE
from oat.views.ui.ui_data_overview import Ui_OverviewView
from oat.modules.dialogs.datasetmanager import DatasetManagerDialog

logger = logging.getLogger(__name__)

class CustomQSortFilterProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def filterAcceptsRow(self, source_row: int, source_parent: QtCore.QModelIndex) -> bool:
        model = self.sourceModel()
        index = model.index(source_row, 0, source_parent)
        return not model.data(index, EMPTY_ROLE)

    def filterAcceptsColumn(self, source_column:int, source_parent:QtCore.QModelIndex) -> bool:
        header = self.sourceModel().headerData(source_column, QtCore.Qt.Horizontal)
        if header in ["Name", "Laterality", "Patient Pseudonym"]:
            return True
        else:
            return False

class NavigationView(QtWidgets.QWidget, Ui_OverviewView):
    def __init__(self, datasets_model, collections_model, parent=None):
        """Initialize the components of the Toolbox subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.datasets_model = datasets_model
        self.collections_model = collections_model

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
        self.editDatasetButton.clicked.connect(self.open_dataset_manager)

    def update_collections(self):
        self.collections_model.dataset_id = self.datasetComboBox.currentData(
            role=ID_ROLE)

    def open_dataset_manager(self):
        dialog = DatasetManagerDialog()
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
