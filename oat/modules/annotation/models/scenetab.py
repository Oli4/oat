from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget

from oat.modules.annotation.models.treeitemdelegate import TreeItemDelegate
from oat.modules.dialogs import AddAnnotationDialog
from oat.views.ui.ui_scene_tab import Ui_SceneTab
from oat.modules.annotation.models.treeview.itemmodel import TreeItemModel
from oat.modules.annotation.models.treeview.lineitem import TreeLineItem
from oat.models.db import LineTypeModel

import json
import numpy as np
import eyepy as ep


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

    def compute_idealRPE(self):
        try:
            rpe_height = self.ImageTreeView.model().get_layer_height("RPE")
            bm_height = self.ImageTreeView.model().get_layer_height("BM")
        except ValueError as e:
            QtWidgets.QMessageBox.warning(
                self, "Layer Warning", "Computing the idealRPE requires a BM and"
                                       " RPE annotation. \n\n{}".format(str(e)))
            return None
        ideal_rpe = ep.core.drusen.normal_rpe(
            rpe_height, bm_height, self.scene.shape)

        linetype_model = LineTypeModel(self)
        line_types = linetype_model.get_line_types()
        try:
            layer_type_dict = [l for l in line_types
                               if l["name"] == "idealRPE"][0]
        except IndexError:
            layer_type_dict = linetype_model.create_type(
                {"name": "idealRPE", "public":True, "default_color": "ff0000",
                 "description": "The ideal RPE position", })

        layer_data = {
            "annotationtype_id": layer_type_dict["id"],
            "current_color": layer_type_dict["default_color"],
            "image_id": self.scene.image_id,
            "z_value": (self.model.rowCount(
                QtCore.QModelIndex(self.model.area_index)) +
                        self.model.rowCount(
                            QtCore.QModelIndex(self.model.line_index))),
            "line_data": json.dumps({"curves": [], "points": [(x, ideal_rpe[x])
                                     for x in range(len(ideal_rpe))]})
        }
        self.add_line_annotation(layer_data)

    def add_line_annotation(self, data):
        new_item = TreeLineItem.create(
            data, type=self.model.scene.urlprefix,
            shape=self.model.scene.shape)
        self.model.appendRow(
            new_item,
            parent=QtCore.QModelIndex(self.model.line_index))


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
            self.model.getItem(previous).hide_controlls()
        if self.model.getItem(current).isVisible():
            self.model.getItem(current).grabMouse()
            self.model.getItem(current).show_controlls()

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
