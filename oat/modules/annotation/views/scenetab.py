from PyQt5 import Qt, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget

from oat.modules.annotation import TreeItemModel
from oat.modules.annotation.views.treeitemdelegate import TreeItemDelegate
from oat.views.dialogs import AddAnnotationDialog
from oat.views.ui.ui_scene_tab import Ui_SceneTab


class SceneTab(QWidget, Ui_SceneTab):
    def __init__(self, parent, scene: Qt.QGraphicsScene):
        super().__init__(parent)
        self.setupUi(self)
        self.scene = scene
        self.model = TreeItemModel(scene=self.scene, parent=self)
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
        self.ImageTreeView.selectionModel().currentChanged.connect(
            self.on_currentChanged)

        self.opacitySlider.valueChanged.connect(self.set_opacity)

        self.upButton.setEnabled(False)
        self.downButton.setEnabled(False)
        self.upButton.hide()
        self.downButton.hide()

    @QtCore.pyqtSlot('QModelIndex', 'QModelIndex')
    def on_currentChanged(self, current, previous):
        self.scene.setActivePanel(current.internalPointer())

    def set_opacity(self, value):
        self.model.root_item.setOpacity(value / 100)

    def layer_up(self):
        selected = self.ImageTreeView.selectionModel().currentIndex()

        parent = selected.parent()
        row1 = selected.row()
        row2 = row1 - 1

        if 0 < row1 < parent.internalPointer().childCount():
            self.model.layoutAboutToBeChanged.emit()
            self.model.switchRows(row1, row2, parent)
            self.model.layoutChanged.emit()
            self.scene.update()
            self.ImageTreeView.closePersistentEditor()

    def layer_down(self):
        selected = self.ImageTreeView.selectionModel().currentIndex()

        parent = selected.parent()
        row1 = selected.row()
        row2 = row1 + 1

        if 0 <= row1 < parent.internalPointer().childCount() - 1:
            self.model.layoutAboutToBeChanged.emit()
            self.model.switchRows(row2, row1, parent)
            self.model.layoutChanged.emit()
            self.scene.update()

    def add_annotation_layer(self):
        dialog = AddAnnotationDialog(self.model)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.model = TreeItemModel(scene=self.scene, parent=self)
            self.ImageTreeView.setModel(self.model)
            self.model.layoutChanged.emit()
            self.scene.update()

    def remove_annotation_layer(self):
        index = self.ImageTreeView.selectionModel().currentIndex()
        if index.isValid():
            self.model.layoutAboutToBeChanged.emit()
            self.model.removeRows(index.row(), 1, index.parent())
            self.model.layoutChanged.emit()
            self.scene.update()
            # self.ImageTreeView.selectionModel().clear()
