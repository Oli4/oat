import base64
import zlib
from typing import List, Dict

import numpy as np
import requests
import json

from PyQt5 import Qt, QtCore, QtWidgets, QtGui
import qimage2ndarray

from oat import config

class ControllPointGraphicsItem(Qt.QGraphicsRectItem):
    def __init__(self, parent, pos, **kwargs):
        super().__init__(parent=parent, **kwargs)

        self.setRect(Qt.QRectF(Qt.QPoint(0, 0), Qt.QPoint(5, 5)))
        # self.setTransformOriginPoint(self.boundingRect().center())
        self.setPos(pos - self.rect().center())

        pen = Qt.QPen(Qt.QColor("blue"))
        pen.setCosmetic(True)
        self.setPen(pen)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        #self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations, True)

    @property
    def center(self):
        return self.mapToScene(self.boundingRect().center())

    def as_tuple(self):
        center = self.center
        return center.x(), center.y()

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseMoveEvent(event)

        # Make sure control points move together to keep the curve smooth
        if self is self.parentItem().cp_in:
            line = Qt.QLineF(self.center, self.parentItem().center)
            line2 = Qt.QLineF(self.parentItem().center,
                              self.parentItem().cp_out.center)
            line.setLength(line.length()+line2.length())
            self.parentItem().cp_out = line.p2()
        elif self is self.parentItem().cp_out:
            line = Qt.QLineF(self.center, self.parentItem().center)
            line2 = Qt.QLineF(self.parentItem().center,
                              self.parentItem().cp_in.center)
            line.setLength(line.length() + line2.length())
            self.parentItem().cp_in = line.p2()

        self.parentItem().parentItem().update_line()
        self.parentItem().set_lines()


class PointGraphicsItem(Qt.QGraphicsEllipseItem):
    def __init__(self, parent, pos, **kwargs):
        super().__init__(parent=parent, **kwargs)

        self.setRect(Qt.QRectF(Qt.QPoint(0,0), Qt.QPoint(5,5)))
        self.setPos(pos-self.rect().center())

        pen = Qt.QPen(Qt.QColor("red"))
        pen.setCosmetic(True)
        self.setPen(pen)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        #self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations, True)

        self._cp_in = None
        self._cp_out = None
        self._line_in = None
        self._line_out = None

    def focusInEvent(self, event: QtGui.QFocusEvent) -> None:
        super().focusInEvent(event)
        pen = Qt.QPen(Qt.QColor("yellow"))
        pen.setCosmetic(True)
        self.setPen(pen)
        self.update()

    def focusOutEvent(self, event: QtGui.QFocusEvent) -> None:
        super().focusOutEvent(event)
        pen = Qt.QPen(Qt.QColor("red"))
        pen.setCosmetic(True)
        self.setPen(pen)
        self.update()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Delete:
            self.parentItem().delete_knot(self)

    @classmethod
    def from_dict(cls, data, parent=None):
        new = cls(parent, Qt.QPointF(*data["knot"]))
        if "cpin" in data:
            new.cp_in = Qt.QPointF(*data["cpin"])
        if "cpout" in data:
            new.cp_out = Qt.QPointF(*data["cpout"])
        return new

    def to_dict(self):
        return {"knot": self.as_tuple(),
                "cpin": self.cp_in.as_tuple(),
                "cpout": self.cp_out.as_tuple()}

    @property
    def center(self):
        return self.mapToScene(self.boundingRect().center())

    def as_tuple(self):
        center = self.center
        return center.x(), center.y()

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if self.scene().sceneRect().contains(self.mapToScene(event.pos())):
            super().mouseMoveEvent(event)
        self.parentItem().update_line()

    @property
    def cp_in(self) -> ControllPointGraphicsItem:
        return self._cp_in

    @cp_in.setter
    def cp_in(self, cp):
        if not self._cp_in is None:
            self._cp_in.setParentItem(None)
        self._cp_in = ControllPointGraphicsItem(self, self.mapFromScene(cp))
        self._set_line_in()

    def _set_line_in(self):
        if not self._cp_in is None:
            if self._line_in is None:
                self._line_in = Qt.QGraphicsLineItem(
                    Qt.QLineF(self.mapFromScene(self.center),
                              self.mapFromScene(self.cp_in.center)),
                    parent=self)
                pen = Qt.QPen(Qt.QColor("blue"))
                pen.setCosmetic(True)
                self._line_in.setPen(pen)
            else:
                self._line_in.setLine(Qt.QLineF(
                    self.mapFromScene(self.center),
                    self.mapFromScene(self.cp_in.center)))

    @property
    def cp_out(self) -> ControllPointGraphicsItem:
        return self._cp_out

    @cp_out.setter
    def cp_out(self, cp):
        if not self._cp_out is None:
            self._cp_out.setParentItem(None)
        self._cp_out = ControllPointGraphicsItem(self, self.mapFromScene(cp))
        self._set_line_out()

    def _set_line_out(self):
        if not self._cp_out is None:
            if self._line_out is None:
                self._line_out = Qt.QGraphicsLineItem(
                    Qt.QLineF(self.mapFromScene(self.center),
                              self.mapFromScene(self.cp_out.center)),
                    parent=self)
                pen = Qt.QPen(Qt.QColor("blue"))
                pen.setCosmetic(True)
                self._line_out.setPen(pen)
            else:
                self._line_out.setLine(Qt.QLineF(
                    self.mapFromScene(self.center),
                    self.mapFromScene(self.cp_out.center)))

    def set_lines(self):
        self._set_line_out()
        self._set_line_in()


class TreeLineItem(Qt.QGraphicsPathItem):
    _defaults = {"visible": True, "line_data": {"points":[], "curves":[]}}

    def __init__(self, *args, parent=None, data=None, is_panel=True,
                 type="slice", shape, **kwargs):
        """ Provide data to create a new annotation or the id of an existing
        annotation.
        """
        super().__init__(*args, parent=parent, **kwargs)
        if not data is None:
            at = data.pop("annotationtype")
            data = {**at, **data}
        if "heights" in data:
            data.pop("heights")
            data["line_data"] = json.dumps({"curves": [], "points": []})
        if data["line_data"] == '':
            data["line_data"] = json.dumps({"curves": [], "points": []})
        self._data = data
        self.type = type
        self.shape = shape
        [setattr(self, key, value) for key, value in self._data.items()]
        self.line_data = json.loads(self.line_data)

        self.points = None
        self.curve_knots = []
        self.set_data()
        self.changed = False
        self.hide_controlls()

        self.setFlag(Qt.QGraphicsItem.ItemIsFocusable, True)

        self.timer = QtCore.QTimer()
        self.timer.start(5000)
        self.timer.timeout.connect(self.sync)


    def hide_controlls(self):
        for knots in self.curve_knots:
            [k.hide() for k in knots]

    def show_controlls(self):
        for knots in self.curve_knots:
            [k.show() for k in knots]

    def add_knot(self, pos, cpin_pos=None, cpout_pos=None):
        # if first knot, just add knot on the current path
        if not self.view._ctrl_pressed:
            self.changed = True
            new_knot = PointGraphicsItem(self, pos)
            if not cpin_pos is None:
                new_knot.cp_in = cpin_pos
            if not cpout_pos is None:
                new_knot.cp_out = cpout_pos

            self.current_curve_knots.append(new_knot)
            self.current_curve_knots = sorted(
                self.current_curve_knots, key=lambda x: x.center.x())

            if len(self.current_curve_knots) > 1:
                self.update_line()

    def delete_knot(self, knot):
        self.scene().removeItem(knot)
        for knots in self.curve_knots:
            if knot in knots:
                knots.remove(knot)
        self.update_line()

        self.as_array()


    def as_array(self):
        """ Return the annotated path as an array of shape (image width)

        The array has the same shape as the annotated image width. Regions
        which are not annoted become np.nan

        The array is build by painting the annotated path on a pixmap,
        converting it to a numpy array and computing the column-wise center of
        mass for the first channel.
        """

        height, width = self.scene().shape
        qimage = Qt.QImage(width, height, Qt.QImage.Format_RGB32)
        pixmap = QtGui.QPixmap().fromImage(qimage)
        pixmap.convertFromImage(qimage)
        pixmap.fill(QtCore.Qt.black)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor("white")))
        painter.drawPath(self.path())
        painter.end()

        qimage = pixmap.toImage()
        array = qimage2ndarray.rgb_view(qimage)
        indices = np.ones(array.shape[:-1]) * np.arange(height)[..., np.newaxis]

        # Without annotation, set the array to nan
        annotated_region = array[...,0].sum(axis=0) != 0
        heights = np.full(width, np.nan)
        heights[annotated_region] = np.average(
            indices[:,annotated_region], axis=0,
            weights=array[:, annotated_region, 0])
        return heights

    @property
    def as_points(self):
        """Return the annotated path as discrete points

        There is one point returned for every image column even if there is no
        annotation for this column. In this case a point with a y-value of
        np.nan is returned """
        width = self.scene().shape[1]
        return [(x, self.as_array()[x]) for x in range(width)]

    @property
    def current_curve_knots(self):
        # This is enough as long as we support only a single curve per layer
        # We might want to support multiple curves to support ungraded regions
        if len(self.curve_knots) == 0:
            self.curve_knots.append([])
        return self.curve_knots[0]

    @current_curve_knots.setter
    def current_curve_knots(self, value):
        self.curve_knots[0] = value

    @property
    def curve_paths(self):
        paths = []
        for knots in self.curve_knots:
            if len(knots) > 1:
                paths.append(self.build_path(knots, factor=0.25))
        return paths

    @property
    def line_paths(self):
        # Create polygons for annotated non curve regions
        paths = []
        if not self.line_data == {}:
            points = self.line_data["points"]

            # Remove curve regions from points
            points = np.array(points)
            for start, end in self.curve_regions:
                #points = [p for p in points if p[0]>=start and p[0]<=end]
                points[start: end + 1] = np.nan

            # Create QPainterPaths for every point collection.

            line = []
            for point in points:
                point_x, point_y = point
                if not (np.isnan(point_x) | np.isnan(point_y)):
                    line.append(Qt.QPointF(point[0] + 0.5, point[1] + 0.5))
                else:
                    if not line == []:
                        new_line = Qt.QPainterPath(line[0])
                        new_line.addPolygon(Qt.QPolygonF(line[1:]))
                        paths.append(new_line)
                        line = []

            if not line == []:
                new_line = Qt.QPainterPath(line[0])
                new_line.addPolygon(Qt.QPolygonF(line[1:]))
                paths.append(new_line)

        return paths


    def build_path(self, knots, factor=0.25):
        for p, current_point in enumerate(knots):
            current = current_point.center

            if p == 0:
                target = QtCore.QLineF(current, knots[p + 1].center)
                source = QtCore.QLineF().fromPolar(
                    target.length(), 180+target.angle()).translated(current)
                source.setPoints(source.p2(), source.p1())
            elif p == len(knots) - 1:
                source = QtCore.QLineF(knots[p - 1].center, current)
                target = QtCore.QLineF().fromPolar(
                    source.length(), source.angle()).translated(current)
            else:
                source = QtCore.QLineF(knots[p - 1].center, current)
                target = QtCore.QLineF(current, knots[p + 1].center)

            targetAngle = target.angleTo(source)
            if targetAngle > 180:
                angle = (source.angle() + source.angleTo(target) / 2) % 360
            else:
                angle = (target.angle() + target.angleTo(source) / 2) % 360

            if current_point.cp_in is None:
                revTarget = QtCore.QLineF.fromPolar(source.length() * factor,
                                                    angle + 180).translated(current)
                cp2 = revTarget.p2()
                current_point.cp_in = cp2

            if current_point.cp_out is None:
                revSource = QtCore.QLineF.fromPolar(target.length() * factor,
                                                    angle).translated(current)
                cp1 = revSource.p2()
                current_point.cp_out = cp1

            if p == 0:
                path = Qt.QPainterPath(current)
                last_point = current_point
            else:
                path.cubicTo(last_point.cp_out.center,
                             current_point.cp_in.center, current)
                last_point = current_point

        return path

    def update_line(self):
        self.changed=True
        paths = self.line_paths + self.curve_paths
        paths = sorted(paths, key=lambda x: x.elementAt(0).x)
        if len(paths) > 0:
            path = paths[0]
            if len(paths) > 1:
                for i in range(len(paths)-1):
                    path.connectPath(paths[i+1])
            self.setPath(path)
            self.update()

    @property
    def curve_regions(self):
        regions = []
        for knots in self.curve_knots:
            if len(knots) > 0:
                start_x = int(np.floor(knots[0].as_tuple()[0]))
                end_x = int(np.ceil(knots[-1].as_tuple()[0]))
                regions.append((start_x, end_x))
            else:
                self.curve_knots.remove(knots)
        return regions

    def set_data(self):
        if not self.line_data == {}:
            if not "curves" in self.line_data:
                self.line_data["curves"] = []
            curves = self.line_data["curves"]

            # Remove current knots before setting new knots
            [[self.scene().removeItem(k) for k in c] for c in self.curve_knots]
            self.curve_knots = []

            # Add knots and controll points for every Curve
            for curve in curves:
                knots = [PointGraphicsItem.from_dict(p, parent=self)
                         for p in curve]
                knots = sorted(knots, key=lambda x: x.as_tuple()[0])
                self.curve_knots.append(knots)

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
        super().mousePressEvent(event)
        self.view.tool.mouse_press_handler(self, event)
        event.accept()

    def mouseDoubleClickEvent(self, event):
        self.view.tool.mouse_doubleclick_handler(self, event)
        event.accept()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.view.tool.mouse_release_handler(self, event)
        event.accept()

    def keyPressEvent(self, event):
        self.view.tool.key_press_handler(self, event)
        event.accept()

    def keyReleaseEvent(self, event):
        self.view.tool.key_release_handler(self, event)
        event.accept()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.view.tool.mouse_move_handler(self, event)
        event.accept()

    def as_dict(self):
        points = self.line_data["points"]

        all_curves = []
        for knots in self.curve_knots:
            curve_knots = []
            for knot in knots:
                knot_dict = {"knot": knot.as_tuple()}
                if not knot.cp_in is None:
                    knot_dict["cpin"] = knot.cp_in.as_tuple()
                if not knot.cp_out is None:
                    knot_dict["cpout"] = knot.cp_out.as_tuple()
                curve_knots.append(knot_dict)
            all_curves.append(curve_knots)
        return {"points": points, "curves": all_curves}

    def sync(self):
        # Upload local changes if the layer is active
        if self.changed and not self.view._ctrl_pressed:
            self._data.update(line_data=json.dumps(self.as_dict()))
            data = self.put_annotation(annotation_id=self._data["id"],
                                             data=self._data, type=self.type)
            at = data.pop("annotationtype")
            data = {**at, **data}
            self._data = data
            [setattr(self, key, value) for key, value in self._data.items()]
            self.line_data = json.loads(self.line_data)

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
        return 0
    #    return len(self.childItems())

    #def child(self, number: int):
    #    if number < 0 or number >= self.childCount():
    #        return False
    #    return self.childItems()[number]

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