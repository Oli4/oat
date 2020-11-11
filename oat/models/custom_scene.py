from collections import namedtuple
from typing import Tuple, Dict, List

import numpy as np
import skimage.transform as skitrans
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.Qt import QBrush, QGraphicsPixmapItem
from PyQt5.QtCore import QRectF, QAbstractItemModel
from PyQt5.QtWidgets import QGraphicsScene

from .utils import get_enface_by_id, get_bscan_by_id, get_volume_meta_by_id, array2qgraphicspixmapitem

# from .treeitems import *

Line = namedtuple("Line", ["a", "b", "c"])
Point = namedtuple("Point", ["x", "y"])


class CustomAbstractItemModel(QAbstractItemModel):
    def __init__(self, scene, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)
        self.root_item = scene

    # required methods to make this scene work as a treemodel

    def headerData(self, p_int, Qt_Orientation, role=None):
        pass

    def data(self, index: QtCore.QModelIndex(), role=None):
        # Return ItemGroup
        if role == QtCore.Qt.DisplayRole:
            return self.getItem(index)

    def getItem(self, index: QtCore.QModelIndex):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self.rootitem

    def index(self, row, column, parent=QtCore.QModelIndex(), *args, **kwargs):
        if parent.isValid() and parent.column() != 0:
            parentItem = self.getItem(parent);
            if not parentItem:
                raise Exception("No parent Item")
                # return QtCore.QModelIndex()

            childItem = parentItem.child(row);
            if childItem:
                return self.createIndex(row, column, childItem);
            raise Exception("No child Item")
        return QtCore.QModelIndex();

    def parent(self, index: QtCore.QModelIndex):
        if not index.isValid():
            return QtCore.QModelIndex();

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if (parentItem == self.rootitem or not parentItem):
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def rowCount(self, parent: QtCore.QModelIndex, *args, **kwargs):
        parent_item = self.getItem(parent)
        return parent_item.childCount()

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def flags(self, index: QtCore.QModelIndex()):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEditable | QAbstractItemModel.flags(index)

    # Provide support for editing and resizing

    def setData(self, QModelIndex, Any, role=None):
        pass

    def setHeaderData(self, p_int, Qt_Orientation, Any, role=None):
        pass

    def insertColumns(self, p_int, p_int_1, parent=None, *args, **kwargs):
        pass

    def removeColumns(self, p_int, p_int_1, parent=None, *args, **kwargs):
        pass

    def insertRows(self, p_int, p_int_1, parent=None, *args, **kwargs):
        pass

    def removeRows(self, p_int, p_int_1, parent=None, *args, **kwargs):
        pass


class TreeGraphicsItemGroup(Qt.QGraphicsItemGroup):
    def __init__(self, *args, parent=None, data=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        if data is None:
            self._data = {"name": None, "type": None, "status": 0,
                          "color": None, "hidden": False, "opacity": 1}
        else:
            self._data = data

    # Functions to make the QGraphicsItemGroup work as a item in a model tree
    def parent(self):
        return self.parentItem()

    def childNumber(self):
        if self.parent():
            return self.parent().childItems().index(self)
        return 0

    def childCount(self):
        return len(self.childItems())

    def child(self, number: int):
        if number < 0 or number >= self.childCount():
            raise Exception("Number not valid")
            # return None
        return self.childItems()[number]

    def columnCount(self):
        return len(self._data)

    def data(self, column: str):
        if column not in self._data:
            raise Exception("column key not in data")
        return self._data[column]

    def setData(self, column: str, value):
        if column not in self._data or type(self._data[column]) != type(value):
            return False
        self._data[column] = value
        return True

    def insertChildren(self, position: int, count: int, data: List[Dict]):
        if position < 0 or position > self.childCount():
            return False

        for row in range(0, count):
            group = TreeGraphicsItemGroup(parent=self, data=data[row])
            self.addItem(group)

    def removeChildren(self, position: int, count: int):
        pass


class CustomGrahpicsScene(QGraphicsScene):
    number = 0
    base_name = "Default"

    def __init__(self, parent, image_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)
        self._set_name()

        self.image = None
        self.image_meta = None

        self._widthForHeightFactor = 1

        self.area_annotations = []
        self.background_on = True
        self.background_index = self.index(0, 0, QtCore.QModelIndex())
        self.setData(self.background_index, self)

        if image_id:
            self.set_image(image_id)

            # self.add_areaannotations(image_id)
            # self.add_shapeannotations(image_id)
            # self.add_overlays()

    def _set_name(self):
        if self.number == 0:
            self.name = self.base_name
            self.number += 1
        else:
            self.name = f"{self.base_name}_{self.number}"
            self.number += 1

    def _fetch_image(self, image_id) -> Tuple[QGraphicsPixmapItem, Dict]:
        raise NotImplementedError

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF):
        if self.background_on:
            painter.fillRect(self.sceneRect(), self.backgroundBrush())
        else:
            painter.fillRect(self.sceneRect(), QtCore.Qt.NoBrush)

    def set_image(self, image_id):
        print("Set image: ", image_id)
        pixmap_item, meta = self._fetch_image(image_id)
        pixmap = pixmap_item.pixmap()

        self.setSceneRect(QRectF(pixmap.rect()))
        self._widthForHeightFactor = \
            1.0 * pixmap.size().width() / pixmap.size().height()
        brush = QBrush(pixmap)
        self.setBackgroundBrush(brush)

    def hide_background(self):
        if self.background_on:
            self.background_on = False
            self.invalidate(self.sceneRect(), Qt.QGraphicsScene.BackgroundLayer)

    def show_background(self):
        if not self.background_on:
            self.background_on = True
            self.invalidate(self.sceneRect(), Qt.QGraphicsScene.BackgroundLayer)

    def add_areaannotations(self, image_id):
        pass


class BscanGraphicsScene(CustomGrahpicsScene):
    def __init__(self, parent, image_id=None, base_name="OCT", *args, **kwargs):
        self.base_name = base_name
        super().__init__(*args, **kwargs, parent=parent)

        # Fetch Volume image
        self.volume_dict = get_volume_meta_by_id(image_id)
        # Make sure slices are correctly ordered
        self.slices = sorted(self.volume_dict["slices"],
                             key=lambda x: x["number"])

        # Set Scene to first B-Scan
        self.current_slice_number = 0
        self.set_image(self.slices[self.current_slice_number]["id"])

        # Asynchronously load remaining B-Scans

        self.slice_params = [self._line_for_slice(i)
                             for i in range(len(self.slices))]

    @property
    def current_slice(self):
        return self.slices[self.current_slice_number]

    def _line_for_slice(self, number):
        lclzr_scale_x = self.volume_dict["localizer_image"]["scale_x"]
        lclzr_scale_y = self.volume_dict["localizer_image"]["scale_y"]
        start_x = self.slices[number]["start_x"] / lclzr_scale_x
        start_y = self.slices[number]["start_y"] / lclzr_scale_y
        end_x = self.slices[number]["end_x"] / lclzr_scale_x
        end_y = self.slices[number]["end_y"] / lclzr_scale_y

        p1 = Point(start_x, start_y)
        p2 = Point(end_x, end_y)
        a = p1.y - p2.y
        b = p2.x - p1.x
        c = a * (p2.x) + b * (p2.y)

        return Line(a, b, -c)

    def closest_slice(self, pos):
        # Todo: Make this faster for smooth registered navigation
        point = Point(pos.x(), pos.y())

        smallest_dist = self.point_line_distance(point, self.slice_params[0])
        for i, line in enumerate(self.slice_params):

            dist = self.point_line_distance(point, line)
            if dist <= smallest_dist:
                smallest_dist = dist
            else:
                return i - 1
        return i

    @staticmethod
    def point_line_distance(point, line):
        return np.abs(line.a * point.x + line.b * point.y + line.c) / \
               np.sqrt(line.a ** 2 + line.b ** 2)

    def _fetch_image(self, image_id) -> Tuple[QGraphicsPixmapItem, Dict]:
        img, meta = get_bscan_by_id(image_id)
        return array2qgraphicspixmapitem(img), meta

    def set_slice(self, number):
        if 0 <= number < len(self.slices):
            self.current_slice_number = number
            image_id = self.slices[self.current_slice_number]["id"]
            self.set_image(image_id)

    def next_slice(self):
        self.set_slice(self.current_slice_number + 1)

    def last_slice(self):
        self.set_slice(self.current_slice_number - 1)


class EnfaceGraphicsScene(CustomGrahpicsScene):
    def __init__(self, parent, image_id=None, base_name="Enface", *args, **kwargs):
        self.base_name=base_name
        super().__init__(*args, **kwargs, parent=parent, image_id=image_id)

    def _fetch_image(self, image_id) -> Tuple[QGraphicsPixmapItem, Dict]:
        img, meta = get_enface_by_id(image_id)
        return array2qgraphicspixmapitem(img), meta

    @property
    def tform(self):
        if self._tform is None:
            raise AttributeError("tform has not been set.")
        else:
            return self._tform

    @tform.setter
    def tform(self, value: skitrans.ProjectiveTransform):
        self._tform = value
