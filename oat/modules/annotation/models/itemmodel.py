import base64
from typing import List, Dict

import numpy as np
import requests
import zlib
from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtCore import QAbstractItemModel

from oat import config


class TreeGraphicsItem(Qt.QGraphicsItem):
    _defaults = {"visible": True, "mask": "", "upperleft_x": 0,
                 "upperleft_y": 0,
                 "size_x": 0, "size_y": 0}

    def __init__(self, *args, parent=None, data=None, is_panel=True,
                 type="enface", **kwargs):
        """ Provide data to create a new annotation or the id of an existing
        annotation.
        """
        super().__init__(*args, parent=parent, **kwargs)
        if is_panel:
            self.type = type
            # Dict of pixels for every
            self._pixels = {}
            self._data = data
            self.pixels = self._data["mask"]
            self.setFlag(Qt.QGraphicsItem.ItemIsPanel)
            self.timer = QtCore.QTimer()
            self.timer.start(2500)
            self.timer.timeout.connect(self.sync)

            [setattr(self, key, value) for key, value in self._data.items()]

    @classmethod
    def create(cls, data, parent=None, type="enface"):
        data = {**cls._defaults, **data}
        item_data = cls.post_annotation(data, type=type)
        return cls(data=item_data, parent=parent, is_panel=True, type=type)

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

    def sync(self):
        # Upload local changes if the layer is active
        if self.isActive():
            # Check for changes in the DB - any entries newer than the last update
            #
            pixels = self.pixels
            bounding_rect = pixels.boundingRect()
            shape = (bounding_rect.height(), bounding_rect.width())
            upperleft_x, upperleft_y = bounding_rect.topLeft().x(), \
                                       bounding_rect.topLeft().y()
            mask = np.zeros(shape, dtype=bool)
            for pixel in self.pixels:
                mask[pixel.y() - upperleft_y, pixel.x() - upperleft_x] = True

            mask = np.packbits(mask).tobytes()
            mask = zlib.compress(mask)
            mask = base64.b64encode(mask).decode("ascii")
            self._data.update(mask=mask, size_x=shape[1], size_y=shape[0],
                              upperleft_y=upperleft_y, upperleft_x=upperleft_x)
            self._data = self.put_annotation(annotation_id=self._data["id"],
                                             data=self._data, type=self.type)
            self.pixels = self._data["mask"]

    @property
    def pixels(self):
        img_id = self.scene().image_id
        if not img_id in self._pixels:
            self._pixels[img_id] = Qt.QPolygon()
        return self._pixels[img_id]

    @pixels.setter
    def pixels(self, value):
        img_id = self._data["image_id"]
        if value == "":
            self._pixels[img_id] = Qt.QPolygon()
        else:
            mask = base64.b64decode(value)
            mask = zlib.decompress(mask)
            size = self._data["size_x"] * self._data["size_y"]
            shape = (self._data["size_y"], self._data["size_x"])
            mask = np.unpackbits(
                np.frombuffer(mask, dtype=np.uint8))[:size].reshape(shape)

            if img_id in self._pixels:
                old_area = self._pixels[img_id].boundingRect()
            else:
                old_area = False

            self._pixels[img_id] = Qt.QPolygon()
            for pos_y, pos_x in zip(*np.nonzero(mask)):
                pos_x = pos_x + self._data["upperleft_x"]
                pos_y = pos_y + self._data["upperleft_y"]
                self._pixels[img_id].append(
                    Qt.QPoint(pos_x, pos_y))
            area = self._pixels[img_id].boundingRect()

            if old_area:
                area = old_area.united(area)

            self.update(Qt.QRectF(area))

    def flags(self) -> 'QGraphicsItem.GraphicsItemFlags':
        return Qt.QGraphicsItem.ItemIsPanel

    def add_pixel(self, pos):
        if not self.pixels.contains(pos):
            if 0 <= pos.x() < self.scene().shape[1] and \
                    0 <= pos.y() < self.scene().shape[0]:
                self.pixels.append(pos)
                self.update(pos.x(), pos.y(), 1, 1)

    def remove_pixel(self, pos):
        i = self.pixels.indexOf(pos)
        if i != -1:
            self.pixels.remove(i)
            self.update(pos.x(), pos.y(), 1, 1)

    def boundingRect(self) -> QtCore.QRectF:
        # print(self.pixels.boundingRect().x(), self.pixels.boundingRect().y())
        # TODO Return only the bounding region around all points
        return self.scene().sceneRect()

    def paint(self, painter: QtGui.QPainter,
              option: 'QStyleOptionGraphicsItem',
              widget) -> None:
        if self.isPanel():
            pen = Qt.QPen()
            pen.setWidth(1)
            color = Qt.QColor()
            color.setNamedColor(f"#{self.current_color}")
            pen.setBrush(color)
            painter.setPen(pen)
            painter.drawPoints(self.pixels)

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
            print(self._data)
            raise Exception(f"column {column} not in data")
        return getattr(self, column)

    def setData(self, column: str, value):
        if column not in self._data or type(self._data[column]) != type(value):
            return False
        setattr(self, column, value)
        self.scene().update(self.boundingRect())
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
        if scene.base_name in ["NIR", "Enface", "CFP"]:
            self.prefix = "enface"
        elif scene.base_name == "OCT":
            self.prefix = "slice"
        self.root_item = TreeGraphicsItem(is_panel=False)
        self.scene.addItem(self.root_item)
        self.get_annotations()

    def get_annotations(self):
        # Retrive image annotations and create tree item for every annotation
        image_id = self.scene.image_id

        r = requests.get(
            f"{config.api_server}/{self.prefix}areaannotations/image/{image_id}",
            headers=config.auth_header)
        if r.status_code == 200:
            for data in r.json():
                self.root_item.appendChild(
                    TreeGraphicsItem(data=data, type=self.prefix,
                                     is_panel=True))

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
            raise Exception("index is not valid")
            return QtCore.QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parentItem()

        if parentItem is None:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def flags(self, index: QtCore.QModelIndex()):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEditable | QAbstractItemModel.flags(self, index)

    # Provide support for editing and resizing

    def setData(self, index: QtCore.QModelIndex, value, role=None):
        if role == QtCore.Qt.EditRole:
            item = self.getItem(index)
            for k, v in {"current_color": value.color[1:],
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
