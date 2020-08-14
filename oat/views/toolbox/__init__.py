from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from PyQt5.QtWidgets import QWidget

from oat.models import ModalityTreeItem

from oat.views.ui.ui_layergroup_entry import Ui_LayerGroupEntry
from oat.views.ui.ui_layer_entry import Ui_LayerEntry
from oat.views.ui.ui_toolbox import Ui_Toolbox


from oat.views.ui.ui_scene_tab import Ui_SceneTab
class SceneTab(QWidget, Ui_SceneTab):
    def __init__(self, parent, scene):
        super().__init__(parent)
        self.setupUi(self)
        self.scene=scene
        #self.ModalityTreeView.setModel()
        #self.ModalityTreeView.setItemDelegate()

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
            editor = LayerGroupEntry(parent)
        else:
            editor = LayerEntry(parent)

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
            size = LayerGroupEntry(None).size()
        else:
            size = LayerEntry(None).size()

        return size

class LayerGroupEntry(QWidget, Ui_LayerGroupEntry):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

class LayerEntry(QWidget, Ui_LayerEntry):
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
