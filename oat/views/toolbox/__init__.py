from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from PyQt5.QtWidgets import QWidget

from oat.models.config import VISIBILITY_ROLE, POSITION_ROLE, COLOR_ROLE
from oat.models.custom_scene import CustomAbstractItemModel
from oat.views.ui.ui_layer_entry import Ui_LayerEntry
from oat.views.ui.ui_layergroup_entry import Ui_LayerGroupEntry
from oat.views.ui.ui_scene_tab import Ui_SceneTab
from oat.views.ui.ui_toolbox import Ui_Toolbox


class SceneTab(QWidget, Ui_SceneTab):
    def __init__(self, parent, scene: Qt.QGraphicsScene):
        super().__init__(parent)
        self.setupUi(self)
        self.scene = scene
        self.model = CustomAbstractItemModel(scene=self.scene, parent=self)
        self.ImageTreeView.setModel(self.model)
        self.ImageTreeView.header().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        for col in range(1, self.model.columnCount()):
            self.ImageTreeView.hideColumn(col)
        self.ImageTreeView.setHeaderHidden(True)
        # self.ImageTreeView.setUniformRowHeights(False)
        self.ImageTreeView.setItemDelegate(TreeItemDelegate(self.ImageTreeView))
        self.ImageTreeView.setRootIsDecorated(False)

        self.addButton.clicked.connect(self.add_annotation_layer)
        self.deleteButton.clicked.connect(self.remove_annotation_layer)
        self.upButton.clicked.connect(self.layer_up)
        self.downButton.clicked.connect(self.layer_down)

        # Represents AnnotationLayers as Itemgroups in scene
        # Scene needs itemsgroups attribute which returns list of itemgroups

        # Add image to treeview and make it hideable
        # self.ImageTreeView.setItemDelegate()

    def layer_up(self):
        selected = self.ImageTreeView.selectionModel().currentIndex()

        parent = selected.parent()
        row1 = selected.row()
        row2 = row1 - 1
        new_selected = selected.model().index(row2, 1, parent)

        if 0 < row1 < parent.internalPointer().childCount():
            self.model.layoutAboutToBeChanged.emit()
            self.model.switchRows(row1, row2, parent)
            self.ImageTreeView.selectionModel().select(
                new_selected, Qt.QItemSelectionModel.ClearAndSelect)
            self.model.layoutChanged.emit()

    def layer_down(self):
        selected = self.ImageTreeView.selectionModel().currentIndex()

        parent = selected.parent()
        row1 = selected.row()
        row2 = row1 + 1
        new_selected = selected.model().index(row2, 1, parent)

        if 0 <= row1 < parent.internalPointer().childCount() - 1:
            self.model.layoutAboutToBeChanged.emit()
            self.model.switchRows(row2, row1, parent)
            self.ImageTreeView.selectionModel().select(
                new_selected, Qt.QItemSelectionModel.ClearAndSelect)
            self.model.layoutChanged.emit()

    # def switch_layers(self, row1, row2):

    def add_annotation_layer(self):
        index = self.ImageTreeView.selectionModel().currentIndex()
        self.ImageTreeView.selectionModel().clear()
        self.model.layoutAboutToBeChanged.emit()

        if index.isValid():
            self.model.insertRow(index.row() + 1)
            new_row = index.row() + 1
        else:
            # if there is no current index, insert at the top.
            self.model.insertRow(self.model.rowCount())
            new_row = self.model.rowCount() - 1

        index = self.model.index(new_row, 0)
        self.ImageTreeView.selectionModel().setCurrentIndex(
            index, Qt.QItemSelectionModel.ClearAndSelect)

        self.model.layoutChanged.emit()

    def remove_annotation_layer(self):
        index = self.ImageTreeView.selectionModel().currentIndex()
        self.ImageTreeView.selectionModel().clear()
        if index.isValid():
            self.model.layoutAboutToBeChanged.emit()
            self.model.removeRow(index.row(), self.model.parent(index))
            self.model.layoutChanged.emit()


class TreeItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self.index = None
        self._visible = True

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionViewItem',
              index: QtCore.QModelIndex) -> None:
        super().paint(painter, option, index)
        self.parent().openPersistentEditor(index)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem',
                     index: QtCore.QModelIndex) -> QWidget:
        self.editor = LayerEntry(parent)
        self.editor.editorChanged.connect(self.update_model)
        self.index = index
        return self.editor

    QtCore.pyqtSlot()

    def update_model(self):
        editor = self.sender()
        self.commitData.emit(editor)

    def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
        editor.label.setText(str(index.model().data(index, POSITION_ROLE)))
        editor.set_color(str(index.model().data(index, COLOR_ROLE)))
        if index.model().data(index, role=VISIBILITY_ROLE):
            editor.show()
        else:
            editor.hide()

    def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel,
                     index: QtCore.QModelIndex) -> None:
        model.setData(index, editor, QtCore.Qt.EditRole)
        print("set editor data in model")

    def sizeHint(self, option: 'QStyleOptionViewItem',
                 index: QtCore.QModelIndex) -> QtCore.QSize:
        return LayerEntry(None).sizeHint()

class LayerGroupEntry(QWidget, Ui_LayerGroupEntry):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)


class LayerEntry(QWidget, Ui_LayerEntry):
    editorChanged = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        self.visible_icon = QtGui.QIcon()
        self.visible_icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/baseline-visibility-24px.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.hidden_icon = QtGui.QIcon()
        self.hidden_icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/baseline-visibility_off-24px.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off)

        self.visible = True
        self.hideButton.clicked.connect(self.toggle_visibility)
        self.colorButton.clicked.connect(self.set_color)

    def set_color(self, color=None):
        if not color:
            self.color = QtWidgets.QColorDialog.getColor().name()
        else:
            self.color = color
        self.colorButton.setStyleSheet(f"background-color: {self.color}")
        self.editorChanged.emit()

    def toggle_visibility(self):
        if self.visible:
            self.hide()
        else:
            self.show()
        self.editorChanged.emit()

    def hide(self):
        self.visible = False
        self.hideButton.setIcon(self.hidden_icon)

    def show(self):
        self.visible = True
        self.hideButton.setIcon(self.visible_icon)


class Toolbox(QWidget, Ui_Toolbox):
    def __init__(self, parent=None):
        """Initialize the components of the Toolbox subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.main_window = parent

        # Setting up the ImageTreeView
        self.ImageTreeView_2d.setModel(parent.data_model)
        self.ImageTreeView_2d.setItemDelegate(
            TreeItemDelegate(self.ImageTreeView_2d))
        self.ImageTreeView_2d.setHeaderHidden(True)
        self.ImageTreeView_2d.setRootIndex(
            QtCore.QModelIndex(parent.data_2D_index))
        self.ImageTreeView_2d.setUniformRowHeights(False)

        self.ImageTreeView_3d.setModel(parent.data_model)
        self.ImageTreeView_3d.setItemDelegate(
            TreeItemDelegate(self.ImageTreeView_3d))
        self.ImageTreeView_3d.setHeaderHidden(True)
        self.ImageTreeView_3d.setRootIndex(
            QtCore.QModelIndex(parent.data_3D_index))
        self.ImageTreeView_3d.setUniformRowHeights(False)

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
