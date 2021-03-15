import requests
from PyQt5 import Qt, QtCore, QtWidgets
from PyQt5.QtCore import QAbstractItemModel

from oat import config
from oat.modules.annotation.models.treeview.areaitem import TreeAreaItem
from oat.modules.annotation.models.treeview.lineitem import TreeLineItemDB
from oat.modules.annotation.models.treeview.itemgroup import ItemGroup


class TreeItemModel(QAbstractItemModel):
    def __init__(self, scene: Qt.QGraphicsScene, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)
        self.scene = scene
        self.prefix = scene.urlprefix
        self.root_item = ItemGroup()

        self.area_root = ItemGroup(name="Areas")
        self.appendRow(self.area_root)
        self.area_index = QtCore.QPersistentModelIndex(self.index(0,0))

        if self.prefix == "slice":
            self.line_root = ItemGroup(name="Lines")
            self.appendRow(self.line_root)
            self.line_index = QtCore.QPersistentModelIndex(self.index(1, 0))


        self.scene.addItem(self.root_item)
        self.get_annotations()

    def get_layer_height(self, layer):
        layer_item = [self.line_root.child(i)
                      for i in range(self.line_root.childCount())
                      if self.line_root.child(i).data("name") == layer]
        if len(layer_item) == 0:
            raise ValueError(f'The requested layer "{layer}" is not available')
        if len(layer_item) > 1:
            raise ValueError(f'Make sure that there is only a single Layer of Type "{layer}"')
        return layer_item[0].as_array()


    def rowCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        parent_item = self.getItem(parent)
        if type(parent_item) in [TreeLineItemDB, TreeAreaItem]:
            return 0
        return parent_item.childCount()

    def columnCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        return self.root_item.columnCount()

    def data(self, index: QtCore.QModelIndex(), role=None):
        if role == QtCore.Qt.EditRole:
            item = self.getItem(index)
            if type(item) is ItemGroup:
                item_data = {key: item.data(key) for key in
                             ["visible", "z_value", "name"]}
            else:
                item_data = {key: item.data(key) for key in
                             ["current_color", "visible", "z_value", "name"]}
            return item_data

        if role == QtCore.Qt.DisplayRole:
            return "bla"
            #return self.getItem(index).data("annotationtype")["name"]

    def index(self, row, column, parent=QtCore.QModelIndex(), *args, **kwargs):
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QtCore.QModelIndex()

    def parent(self, index: QtCore.QModelIndex):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parentItem()

        if parentItem is None:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def get_annotations(self):
        self._get_area_annotations()
        if self.prefix == "slice":
            self._get_line_annotations()

    def _get_line_annotations(self):
        image_id = self.scene.image_id

        r = requests.get(
            f"{config.api_server}/{self.prefix}lineannotations/image/{image_id}",
            headers=config.auth_header)

        if r.status_code == 200:
            for data in sorted(r.json(), key=lambda x: x["z_value"]):
                item = TreeLineItemDB(data=data, shape=self.scene.shape)
                self.appendRow(item, parent=QtCore.QModelIndex(self.line_index))

    def _get_area_annotations(self):
        # Retrive image annotations and create tree item for every annotation
        image_id = self.scene.image_id

        r = requests.get(
            f"{config.api_server}/{self.prefix}areaannotations/image/{image_id}",
            headers=config.auth_header)
        if r.status_code == 200:
            for data in sorted(r.json(), key=lambda x: x["z_value"]):
                item = TreeAreaItem(data=data, type=self.prefix,
                                    shape=self.scene.shape)
                self.appendRow(item, parent=QtCore.QModelIndex(self.area_index))

    def headerData(self, column, Qt_Orientation, role=None):
        if role != QtCore.Qt.DisplayRole:
            return None
        return [str(x) for x in range(8)][column]

    def getItem(self, index: QtCore.QModelIndex):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self.root_item

    def flags(self, index: QtCore.QModelIndex()):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEditable | QAbstractItemModel.flags(self, index)

    # Provide support for editing and resizing

    def setData(self, index: QtCore.QModelIndex, value, role=None):
        if role == QtCore.Qt.EditRole:
            item = self.getItem(index)
            if type(item) is ItemGroup:
                for k, v in {"visible": value.visible,
                             "name": value.label.text()}.items():
                    item.setData(k, v)
                return True
            else:
                for k, v in {"current_color": value.color,
                             "visible": value.visible,
                             "name": value.label.text()}.items():
                    item.setData(k, v)
                return True
        return False

    #def insertRows(self, row, count, parent=QtCore.QModelIndex(), *args,
    #               **kwargs):
    #    """ Insert count rows before the given row under the given parent """
    #    self.beginInsertRows(parent, row, row + count - 1)
    #    self.getItem(parent).insertChildren(row, count)
    #    self.endInsertRows()
    #    self.scene.update()
    #    return True

    def appendRow(self, data, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, self.rowCount(parent),
                             self.rowCount(parent))
        self.getItem(parent).appendChild(data)
        self.endInsertRows()
        self.scene.update()

    def switchRows(self, row1, row2, parent=QtCore.QModelIndex()):
        self.beginMoveRows(parent, row1, row1, parent, row2+1)
        self.getItem(parent).switchChildren(row1, row2)
        self.endMoveRows()
        self.scene.update()

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        if parent.isValid() and parent.internalPointer() != self.root_item:
            self.beginRemoveRows(parent, row, row + count - 1)
            parent = self.getItem(parent)
            parent.removeChildren(row, count)
            self.endRemoveRows()
            self.scene.update()
            return True
        return False
