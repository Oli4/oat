from PyQt5 import QtCore, Qt, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

from .ui_2d_viewer import Ui_Viewer2D
from .ui_3d_viewer import Ui_Viewer3D
from .ui_add_patient_dialog import Ui_AddPatientDialog
from .ui_data_table_view import Ui_DataTableView
from .ui_layer_entry import Ui_LayerEntry
from .ui_login_dialog import Ui_LoginDialog
from .ui_main_window import Ui_MainWindow
from .ui_modality_entry import Ui_ModalityEntry
from .ui_registration_manual import Ui_RegistrationManual
from .ui_segmentation_entry import Ui_SegmentationEntry
from .ui_toolbox import Ui_Toolbox
from .ui_upload_dialog import Ui_UploadDialog
from ..models import ModalityTreeItem


class TreeItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self._visible = None

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionViewItem',
              index: QtCore.QModelIndex) -> None:
        if isinstance(self.parent(), QtWidgets.QAbstractItemView) or \
                isinstance(self.parent(), ModalityTreeItem):
            self.parent().openPersistentEditor(index)
        super().paint(painter, option, index)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem',
                     index: QtCore.QModelIndex) -> QWidget:
        if not index.model().itemFromIndex(index).parent():
            editor = ModalityEntry(parent)
        else:
            editor = SegmentationEntry(parent)

        editor.hideButton.clicked.connect(self.visibilityChanged)

        return editor

    @QtCore.pyqtSlot()
    def visibilityChanged(self):
        self._visible = not self._visible
        editor = self.sender().parent().parent()
        self.commitData.emit(editor)

    def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
        editor.label.setText(index.model().data(index, Qt.UserRole + 2))

        icon = QtGui.QIcon()
        if index.model().data(index, Qt.UserRole + 1):
            icon.addPixmap(
                QtGui.QPixmap(":/icons/icons/baseline-visibility-24px.svg"),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off)
            editor.hideButton.setIcon(icon)
            self._visible = True
        else:
            icon.addPixmap(
                QtGui.QPixmap(":/icons/icons/baseline-visibility_off-24px.svg"),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off)
            editor.hideButton.setIcon(icon)
            self._visible = False

    def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel,
                     index: QtCore.QModelIndex) -> None:
        model.setData(index, self._visible, Qt.UserRole + 1)

    def sizeHint(self, option: 'QStyleOptionViewItem',
                 index: QtCore.QModelIndex) -> QtCore.QSize:
        if not index.model().itemFromIndex(index).parent():
            size = ModalityEntry(None).size()
        else:
            size = SegmentationEntry(None).size()

        return size


class ModalityEntry(QWidget, Ui_ModalityEntry):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)


class SegmentationEntry(QWidget, Ui_SegmentationEntry):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)


class Toolbox(QWidget, Ui_Toolbox):
    def __init__(self, parent=None):
        """Initialize the components of the Toolbox subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.main_window = parent

        # Setting up the ModalityTreeView
        self.ModalityTreeView_2d.setModel(parent.data_model)
        self.ModalityTreeView_2d.setItemDelegate(
            TreeItemDelegate(self.ModalityTreeView_2d))
        self.ModalityTreeView_2d.setHeaderHidden(True)
        self.ModalityTreeView_2d.setRootIndex(
            QtCore.QModelIndex(parent.data_2D_index))
        self.ModalityTreeView_2d.setUniformRowHeights(False)

        self.ModalityTreeView_3d.setModel(parent.data_model)
        self.ModalityTreeView_3d.setItemDelegate(
            TreeItemDelegate(self.ModalityTreeView_3d))
        self.ModalityTreeView_3d.setHeaderHidden(True)
        self.ModalityTreeView_3d.setRootIndex(
            QtCore.QModelIndex(parent.data_3D_index))
        self.ModalityTreeView_3d.setUniformRowHeights(False)

        # self.addButton_2d.clicked.connect(self.create_layer_2d)
        # self.addButton_3d.clicked.connect(self.create_layer_3d)

        self.registerButton_2d.clicked.connect(
            self.main_window.create_registration_view)

    def closeEvent(self, evnt):
        evnt.ignore()
        self.setWindowState(QtCore.Qt.WindowMinimized)


class LayerTreeView(QtWidgets.QTreeView):
    def __init__(self, model, parent):
        super().__init__(parent)
        self.setModel(model)
        model.setView(self)
        root = model.index(0, 0)
        self.setCurrentIndex(root)
        self.setHeaderHidden(True)
