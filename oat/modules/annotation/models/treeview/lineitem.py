import base64
import zlib
from typing import List, Dict

import numpy as np
import requests
import json

from PyQt5 import Qt, QtCore

from oat import config


class TreeLineItem(Qt.QGraphicsPathItem):
    _defaults = {"visible": True, "heights": ""}

    def __init__(self, *args, parent=None, data=None, is_panel=True,
                 type="slice", shape, **kwargs):
        """ Provide data to create a new annotation or the id of an existing
        annotation.
        """
        super().__init__(*args, parent=parent, **kwargs)
        if not data is None:
            at = data.pop("annotationtype")
            data = {**at, **data}
        self._data = data
        self.type = type
        self.shape = shape
        [setattr(self, key, value) for key, value in self._data.items()]

        self.points = None
        self.set_data()


        # self.toSubpathPolygons() for saving




        """
        self.paintable = False
        if is_panel:
            self.paintable=True
            self.set_data()

            self.changed = False
            self.setFlag(Qt.QGraphicsItem.ItemIsFocusable)
            self.timer = QtCore.QTimer()
            self.timer.start(2500)
            self.timer.timeout.connect(self.sync)

        """

    def update_line(self):
        path = Qt.QPainterPath()
        for p in self.polygons:
            path.addPolygon(p)
        self.setPath(path)
        self.update()

    def set_data(self):
        if self.line_data == "":
            polygons = [Qt.QPolygonF([Qt.QPointF(i, self.shape[0]/2)
                      for i in [0, self.shape[1]]])]
        else:
            points = json.loads(self.line_data)["points"]
            polygons = []
            path = []
            # Add a polygon for every subpath (not interupted by nan)
            for point in points:
                if not np.isnan(point[1]):
                    path.append(Qt.QPointF(point[0]+0.5, point[1]))
                else:
                    if not path == []:
                        polygons.append(Qt.QPolygonF(path))
                        path = []
            if not path == []:
                polygons.append(Qt.QPolygonF(path))

        self.polygons = polygons
        self.update_line()

    @classmethod
    def create(cls, data, shape, parent=None, type="slice"):
        data = {**cls._defaults, **data}
        item_data = cls.post_annotation(data, type=type)
        return cls(data=item_data, parent=parent, is_panel=True, type=type,
                   shape=shape)

    @classmethod
    def from_annotation_id(cls, id, parent=None, type="slice"):
        item_data = cls.get_annotation(id, type=type)
        return cls(data=item_data, parent=parent, is_panel=True, type=type)

    @staticmethod
    def post_annotation(data, type="slice"):
        response = requests.post(
            f"{config.api_server}/{type}lineannotations/",
            headers=config.auth_header, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Status Code: {response.status_code}\n"
                             f"{response.json()}")

    @staticmethod
    def get_annotation(annotation_id, type="slice"):
        if type not in ["enface", "slice"]:
            msg = f"Parameter type has to be (enface|slice) not {type}"
            raise ValueError(msg)

        response = requests.get(
            f"{config.api_server}/{type}lineannotations/{annotation_id}",
            headers=config.auth_header)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Status Code: {response.status_code}\n"
                             f"{response.json()}")

    @staticmethod
    def put_annotation(annotation_id, data, type="slice"):
        response = requests.put(
            f"{config.api_server}/{type}lineannotations/{annotation_id}",
            json=data, headers=config.auth_header)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Status Code: {response.status_code}\n"
                             f"{response.json()}")

    @staticmethod
    def delete_annotation(annotation_id, type="slice"):
        response = requests.delete(
            f"{config.api_server}/{type}lineannotations/{annotation_id}",
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
        pen = Qt.QPen(color)
        pen.setWidth(2)
        pen.setCosmetic(True)
        self.setPen(pen)
        self.update()

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
        if (column not in self._data) or type(self._data[column]) != type(value):
            return False

        setattr(self, column, value)
        if column == "visible" and value == True:
            if self.scene().mouseGrabberItem() is None:
                self.grabMouse()

        self.scene().update(self.scene().sceneRect())
        return True

    def appendChild(self, data: "TreeLineItem"):
        items = self.childItems()

        if items:
            z_value = float(items[-1].zValue() + 1)
        else:
            z_value = 0.0

        data.z_value = z_value
        data.setParentItem(self)

    def insertChildren(self, row: int, count: int, data: List[Dict] = None):
        if row < 0:
            return False

        items = self.childItems()

        if items:
            z = float(items[-1].zValue() + 1)
        else:
            z = 0.0
        z_values = [float(x) for x in range(z, z + count)]

        for i, z_value in enumerate(z_values):
            if data:
                item_data = data[i]
            else:
                item_data = {}
            item_data.update(z_value=z_value)
            layer = TreeLineItem(data=item_data)
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