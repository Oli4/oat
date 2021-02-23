from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget

from oat.modules.annotation.models.treeitemdelegate import TreeItemDelegate
from oat.modules.dialogs import AddAnnotationDialog
from oat.views.ui.ui_scene_tab import Ui_SceneTab
from oat.modules.annotation.models.treeview.itemmodel import TreeItemModel


class SceneTab(QWidget, Ui_SceneTab):
    def __init__(self, scene: "CustomGraphicsScene", parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.scene = scene
        self.model = TreeItemModel(self.scene)
        self.configure_imageTreeView()


        self.addButton.clicked.connect(self.add_annotation_layer)
        self.deleteButton.clicked.connect(self.remove_annotation_layer)
        self.upButton.clicked.connect(self.layer_up)
        self.downButton.clicked.connect(self.layer_down)


        self.opacitySlider.valueChanged.connect(self.set_opacity)

        #self.upButton.setEnabled(False)
        #self.downButton.setEnabled(False)
        #self.upButton.hide()
        #self.downButton.hide()

    def configure_imageTreeView(self):
        self.ImageTreeView.setModel(self.model)
        self.ImageTreeView.header().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        for col in range(1, self.model.columnCount()):
            self.ImageTreeView.hideColumn(col)
        self.ImageTreeView.setHeaderHidden(True)
        self.ImageTreeView.setItemDelegate(TreeItemDelegate(self.ImageTreeView))
        self.ImageTreeView.setRootIsDecorated(False)
        self.ImageTreeView.selectionModel().currentRowChanged.connect(
            self.on_currentChanged)
        self.ImageTreeView.expandAll()


    @QtCore.pyqtSlot('QModelIndex', 'QModelIndex')
    def on_currentChanged(self, current, previous):
        if self.model.getItem(previous) == self.model.scene.mouseGrabberItem():
            self.model.getItem(previous).ungrabMouse()
        if self.model.getItem(current).isVisible():
            self.model.getItem(current).grabMouse()

    def set_opacity(self, value):
        self.model.root_item.setOpacity(value / 100)

    def layer_up(self):
        selected = self.ImageTreeView.selectionModel().currentIndex()

        parent = selected.parent()
        row1 = selected.row()
        row2 = row1 - 1

        if 0 < row1 <= parent.internalPointer().childCount():
            self.model.switchRows(row2, row1, parent)
            #self.ImageTreeView.selectionModel().currentRowChanged.emit(
            #    self.model.index(row1, 0, parent),
            #    self.model.index(row2, 0, parent))

    def layer_down(self):
        selected = self.ImageTreeView.selectionModel().currentIndex()

        parent = selected.parent()
        row1 = selected.row()
        row2 = row1 + 1

        if 0 <= row1 < parent.internalPointer().childCount() - 1:
            self.model.switchRows(row1, row2, parent)
            #self.ImageTreeView.selectionModel().currentRowChanged.emit(
            #    self.model.index(row1, 0, parent),
            #    self.model.index(row2, 0, parent))

    def add_annotation_layer(self):
        tab_widget = self.parent().parent()
        dialog = AddAnnotationDialog(tab_widget)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.model.layoutChanged.emit()
            self.scene.update()

    def remove_annotation_layer(self):
        index = self.ImageTreeView.selectionModel().currentIndex()
        if index.isValid():
            self.model.layoutAboutToBeChanged.emit()
            self.model.removeRows(index.row(), 1, index.parent())
            self.model.layoutChanged.emit()
            self.scene.update()
