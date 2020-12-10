import base64
from typing import List, Dict

import numpy as np
import requests
import zlib
from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtCore import QAbstractItemModel
import qimage2ndarray

from oat import config


class TreeGraphicsItem(Qt.QGraphicsPixmapItem):
    _defaults = {"visible": True, "mask": "", "upperleft_x": 0,
                 "upperleft_y": 0,
                 "size_x": 0, "size_y": 0}

    def __init__(self, *args, parent=None, data=None, is_panel=True,
                 type="enface", shape, **kwargs):
        """ Provide data to create a new annotation or the id of an existing
        annotation.
        """
        super().__init__(*args, parent=parent, **kwargs)
        self.shape = shape
        #self.setOffset(Qt.QPointF(-0.5, -0.5))
        self.paintable = False
        if is_panel:
            self.paintable=True
            self.type = type
            # Dict of pixels for every
            self._data = data
            height, width = self.shape
            self.qimage = Qt.QImage(width, height,
                                    Qt.QImage.Format_ARGB32)
            color = Qt.QColor()
            color.setNamedColor(f"#{self.current_color}")
            self.qimage.fill(color)
            self.alpha_array = qimage2ndarray.alpha_view(self.qimage)
            self.setPixmap(Qt.QPixmap())
            self.set_data()


            self.pixels = self._data["mask"]
            self.changed = False
            self.setFlag(Qt.QGraphicsItem.ItemIsFocusable)
            self.timer = QtCore.QTimer()
            self.timer.start(2500)
            self.timer.timeout.connect(self.sync)

            [setattr(self, key, value) for key, value in self._data.items()]

    def update_pixmap(self):
        pixmap = self.pixmap()
        pixmap.convertFromImage(self.qimage)
        self.setPixmap(pixmap)

    def set_data(self):
        self.alpha_array[...] = 0.0
        y_start = self._data["upperleft_y"]
        y_end = self._data["upperleft_y"] + self._data["size_y"]
        x_start = self._data["upperleft_x"]
        x_end = self._data["upperleft_x"] + self._data["size_x"]

        if self._data["mask"] != "":
            mask = base64.b64decode(self._data["mask"])
            mask = zlib.decompress(mask)
            size = self._data["size_x"] * self._data["size_y"]
            shape = (self._data["size_y"], self._data["size_x"])
            mask = np.unpackbits(
                np.frombuffer(mask, dtype=np.uint8))[:size].reshape(shape)
            self.alpha_array[y_start:y_end,x_start:x_end] = mask.astype(float)*255
            self.update_pixmap()


    @classmethod
    def create(cls, data, shape, parent=None, type="enface"):
        data = {**cls._defaults, **data}
        item_data = cls.post_annotation(data, type=type)
        return cls(data=item_data, parent=parent, is_panel=True, type=type,
                   shape=shape)

    @classmethod
    def from_annotation_id(cls, id, parent=None, type="enface"):
        item_data = cls.get_annotation(id, type=type)
        return cls(data=item_data, parent=parent, is_panel=True, type=type)

    @staticmethod
    def post_annotation(data, type="enface"):
        response = requests.post(
            f"{config.api_server}/{type}areaannotations/",
            headers=config.auth_header, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Status Code: {response.status_code}\n"
                             f"{response.json()}")

    @staticmethod
    def get_annotation(annotation_id, type="enface"):
        if type not in ["enface", "slice"]:
            msg = f"Parameter type has to be (enface|slice) not {type}"
            raise ValueError(msg)

        response = requests.get(
            f"{config.api_server}/{type}areaannotations/{annotation_id}",
            headers=config.auth_header)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Status Code: {response.status_code}\n"
                             f"{response.json()}")

    @staticmethod
    def put_annotation(annotation_id, data, type="enface"):
        response = requests.put(
            f"{config.api_server}/{type}areaannotations/{annotation_id}",
            json=data, headers=config.auth_header)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Status Code: {response.status_code}\n"
                             f"{response.json()}")

    @staticmethod
    def delete_annotation(annotation_id, type="enface"):
        response = requests.delete(
            f"{config.api_server}/{type}areaannotations/{annotation_id}",
            headers=config.auth_header)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Status Code: {response.status_code}\n"
                             f"{response.json()}")

    @property
    def view(self):
        return self.scene().views()[0]

    def mousePressEvent(self, event):
        self.view.tool.mouse_press_handler(self, event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.view.tool.mouse_release_handler(self, event)
        event.accept()

    def keyPressEvent(self, event):
        self.view.tool.key_press_handler(self, event)
        event.accept()

    def keyReleaseEvent(self, event):
        self.view.tool.key_release_handler(self, event)
        event.accept()

    def mouseMoveEvent(self, event):
        self.view.tool.mouse_move_handler(self, event)
        event.accept()

    def sync(self):
        # Upload local changes if the layer is active
        if self.changed:
            mask = self.alpha_array == 255.0
            mask = np.packbits(mask).tobytes()
            mask = zlib.compress(mask)
            mask = base64.b64encode(mask).decode("ascii")
            self._data.update(mask=mask, size_x=self.shape[1], size_y=self.shape[0],
                              upperleft_y=0, upperleft_x=0)
            self._data = self.put_annotation(annotation_id=self._data["id"],
                                             data=self._data, type=self.type)
            self.set_data()
            self.changed=False

    def add_pixels(self, pos, mask):
        size_x, size_y = mask.shape
        offset_x = pos.x() - (size_x - 1) / 2
        offset_y = pos.y() - (size_y - 1) / 2

        for ix, iy in np.ndindex(mask.shape):
            if mask[ix, iy]:
                self.alpha_array[int(offset_y+iy), int(offset_x+ix)] = 255.0

        self.update_pixmap()
        self.changed = True

    def remove_pixels(self, pos, mask):
        size_x, size_y = mask.shape
        offset_x = pos.x() - (size_x - 1) / 2
        offset_y = pos.y() - (size_y - 1) / 2
        for ix, iy in np.ndindex(mask.shape):
            if mask[ix, iy]:
                self.alpha_array[int(offset_y + iy), int(offset_x + ix)] = 0.0

        self.update_pixmap()
        self.changed = True

    # Functions to make the QGraphicsItemGroup work as a item in a model tree

    @property
    def visible(self):
        return self.isVisible()

    @visible.setter
    def visible(self, value):
        self.setVisible(value)

    @property
    def z_value(self):
        return self.zValue()

    @z_value.setter
    def z_value(self, value):
        self.setZValue(value)

    @property
    def current_color(self):
        return self._data["current_color"]

    @current_color.setter
    def current_color(self, value):
        self._data["current_color"] = value
        color = Qt.QColor()
        color.setNamedColor(f"#{self.current_color}")
        self.qimage.fill(color)
        self.set_data()
        self.update_pixmap()

    def childNumber(self):
        if self.parentItem():
            return self.parentItem().childItems().index(self)
        return 0

    def childCount(self):
        return len(self.childItems())

    def child(self, number: int):
        if number < 0 or number >= self.childCount():
            return False
        return self.childItems()[number]

    def columnCount(self):
        return 1

    def data(self, column: str):
        if column not in self._data:
            raise Exception(f"column {column} not in data")
        return getattr(self, column)

    def setData(self, column: str, value):
        if column not in self._data or type(self._data[column]) != type(value):
            return False
        setattr(self, column, value)
        self.scene().update(self.scene().sceneRect())
        return True

    def appendChild(self, data: "TreeGraphicsItem"):
        items = self.childItems()

        if items:
            z_value = int(items[-1].zValue() + 1)
        else:
            z_value = 0

        data.z_value = z_value
        data.setParentItem(self)

    def insertChildren(self, row: int, count: int, data: List[Dict] = None):
        if row < 0:
            return False

        items = self.childItems()

        if items:
            z = int(items[-1].zValue() + 1)
        else:
            z = 0
        z_values = list(range(z, z + count))
        # if self.childCount() == 0:
        #    z_values = list(range(0, count))

        # If no other item: Set z-Values from 0 to -count
        # elif row == 0:
        #    z_values = np.linspace(0, items[0].zValue(), count + 2)[1:-1]

        # If appended: Set z-Value of last item + 1
        # elif row == self.childCount():
        #    z_values = [items[-1].zValue() + i for i in range(1, count + 1)]

        # If inserted: Set z-Values to linspace between last and next items z_value
        # else:
        #    z_values = [items[-1].zValue() + i for i in range(1, count + 1)]
        # z_values = np.linspace(items[row-1].zValue(),
        #                       items[row].zValue(), count + 2)[1:-1]

        for i, z_value in enumerate(z_values):
            if data:
                item_data = data[i]
            else:
                item_data = {}
            item_data.update(z_value=z_value)
            layer = TreeGraphicsItem(data=item_data)
            layer.setParentItem(self)

    def removeChildren(self, row: int, count: int):
        if row < 0 or row > self.childCount():
            raise Exception("what went wrong here?")
        items = self.childItems()

        for i in range(row, row + count):
            item = items[i]
            item.scene().removeItem(item)
            self.delete_annotation(item._data["id"], item.type)

    def switchChildren(self, row1: int, row2: int):
        child1 = self.child(row1)
        child2 = self.child(row2)

        child1_z = child1.zValue()
        child2_z = child2.zValue()
        child1.setData("z_value", child2_z)
        child2.setData("z_value", child1_z)


class TreeItemModel(QAbstractItemModel):
    def __init__(self, scene: Qt.QGraphicsScene, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)
        self.scene = scene
        self.prefix = scene.urlprefix
        self.root_item = TreeGraphicsItem(is_panel=False, shape=(0,0))
        self.scene.addItem(self.root_item)
        self.get_annotations()

    def rowCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        parent_item = self.getItem(parent)
        return parent_item.childCount()

    def columnCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        return self.root_item.columnCount()

    def data(self, index: QtCore.QModelIndex(), role=None):
        if role == QtCore.Qt.EditRole:
            item = self.getItem(index)

            annotation_data = {key: item.data(key) for key in
                               ["current_color", "visible", "z_value"]}
            type_data = {"name": item.data("annotationtype")["name"]}
            return {**annotation_data, **type_data}

        if role == QtCore.Qt.DisplayRole:
            return self.getItem(index).data("annotationtype")["name"]

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
        # Retrive image annotations and create tree item for every annotation
        image_id = self.scene.image_id

        r = requests.get(
            f"{config.api_server}/{self.prefix}areaannotations/image/{image_id}",
            headers=config.auth_header)
        if r.status_code == 200:
            for data in sorted(r.json(), key=lambda x: x["z_value"]):
                self.appendRow(
                    TreeGraphicsItem(data=data, type=self.prefix,
                                     is_panel=True, shape=self.scene.shape))

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
            for k, v in {"current_color": value.color,
                         "visible": value.visible,
                         "name": value.label.text()}.items():
                item.setData(k, v)
            return True
        return False

    def insertRows(self, row, count, parent=QtCore.QModelIndex(), *args,
                   **kwargs):
        """ Insert count rows before the given row under the given parent """
        self.beginInsertRows(parent, row, row + count - 1)
        self.getItem(parent).insertChildren(row, count)
        self.endInsertRows()
        self.scene.update()
        return True

    def appendRow(self, data: TreeGraphicsItem, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, self.rowCount(), self.rowCount())
        self.getItem(parent).appendChild(data)
        self.endInsertRows()
        self.scene.update()

    def switchRows(self, row1, row2, parent=QtCore.QModelIndex()):
        self.beginMoveRows(parent, row1, row1, parent, row2)
        self.getItem(parent).switchChildren(row1, row2)
        self.endMoveRows()
        self.scene.update()

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        if parent.isValid():
            self.beginRemoveRows(parent, row, row + count - 1)
            parent = self.getItem(parent)
            parent.removeChildren(row, count)
            self.endRemoveRows()
            self.scene.update()
            return True
        return False
