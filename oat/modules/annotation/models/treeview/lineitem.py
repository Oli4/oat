import base64
import zlib
from typing import List, Dict, Optional

import numpy as np
import requests
import json

from PyQt5 import Qt, QtCore, QtWidgets, QtGui
import qimage2ndarray

from oat import config

import logging
logger = logging.getLogger(__name__)

class ControllPointGraphicsItem(Qt.QGraphicsRectItem):
    def __init__(self, parent, pos, **kwargs):
        super().__init__(parent=parent, **kwargs)

        self.setRect(Qt.QRectF(Qt.QPoint(-4, -4), Qt.QPoint(4, 4)))
        self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations, True)
        self.setPos(pos)

        pen = Qt.QPen(Qt.QColor("blue"))
        pen.setCosmetic(True)
        self.setPen(pen)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)

    @property
    def center(self):
        return self.mapToScene(Qt.QPointF(0,0))

    def as_tuple(self):
        center = self.center
        return np.round(center.x(), 2), np.round(center.y(), 2)

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


class KnotGraphicsItem(Qt.QGraphicsEllipseItem):
    def __init__(self, parent, pos, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations, True)
        self.setRect(Qt.QRectF(Qt.QPoint(-5, -5), Qt.QPoint(5, 5)))
        self.setPos(pos)

        pen = Qt.QPen(Qt.QColor("red"))
        pen.setCosmetic(True)
        self.setPen(pen)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemStacksBehindParent, True)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',
              widget: Optional[QtWidgets.QWidget] = ...) -> None:
        super().paint(painter, option, widget)

    @property
    def center(self):
        return self.mapToScene(Qt.QPointF(0,0))

    def as_tuple(self):
        center = self.center
        return np.round(center.x(), 2), np.round(center.y(), 2)

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
        if event.key() == QtCore.Qt.Key_Delete:
            self.parentItem().parentItem().delete_knot(self.parentItem())

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        logger.debug("mousePress on Knot")
        if event.buttons() & QtCore.Qt.RightButton:
            self.parentItem().parentItem().delete_knot(self.parentItem())
        self.ungrabMouse()



class CubicSplineKnotItem(Qt.QGraphicsItem):
    def __init__(self, parent, knot_pos: Qt.QPointF,
                 cp_in_pos: Optional[Qt.QPointF],
                 cp_out_pos: Optional[Qt.QPointF], **kwargs):
        """"""

        super().__init__(parent=parent, **kwargs)
        # Create knot
        self._knot = KnotGraphicsItem(self, self.mapFromScene(knot_pos))
        # Create control points
        pen = Qt.QPen(Qt.QColor("blue"))
        pen.setCosmetic(True)
        self.cps_visible = True

        if cp_in_pos is None:
            cp_in_pos = Qt.QPointF(knot_pos.x()-10, knot_pos.y())

        self._cp_in = ControllPointGraphicsItem(self, cp_in_pos)
        self._line_in = Qt.QGraphicsLineItem(
            Qt.QLineF(self.mapFromScene(self.knot.center),
                      self.mapFromScene(self.cp_in.center)),
            parent=self)
        self._line_in.setPen(pen)

        if cp_out_pos is None:
            cp_out_pos = Qt.QPointF(knot_pos.x() + 10, knot_pos.y())

        self._cp_out = ControllPointGraphicsItem(self, cp_out_pos)
        self._line_out = Qt.QGraphicsLineItem(
            Qt.QLineF(self.mapFromScene(self.knot.center),
                      self.mapFromScene(self.cp_out.center)),
            parent=self)
        self._line_out.setPen(pen)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemHasNoContents, True)

    def boundingRect(self) -> QtCore.QRectF:
        return self.childrenBoundingRect()

    def shape(self) -> QtGui.QPainterPath:
        d = Qt.QPointF(4, 4)
        r = Qt.QRectF(self.knot.center - d, self.knot.center + d)

        path = Qt.QPainterPath()
        path.addEllipse(r)
        return path

    @property
    def center(self):
        return self.knot.center

    @classmethod
    def from_dict(cls, data, parent=None):
        new = cls(parent, Qt.QPointF(*data["knot"]), Qt.QPointF(*data["cpin"]),
                  Qt.QPointF(*data["cpout"]))
        return new

    def as_dict(self):
        return {"knot": self.knot.as_tuple(),
                "cpin": self.cp_in.as_tuple(),
                "cpout": self.cp_out.as_tuple()}

    def hide_control_points(self):
        self.cps_visible = False
        self._cp_in.hide()
        self._cp_out.hide()
        self._line_in.hide()
        self._line_out.hide()

    def show_control_points(self):
        self.cps_visible = True
        self._cp_in.show()
        self._cp_out.show()
        self._line_in.show()
        self._line_out.show()

    @property
    def knot(self) -> KnotGraphicsItem:
        return self._knot

    @property
    def cp_in(self) -> ControllPointGraphicsItem:
        return self._cp_in

    @cp_in.setter
    def cp_in(self, cp):
        # Remove previous controllpoint
        self._cp_in.setPos(self.mapFromScene(cp))
        self._set_line_in()

    @property
    def cp_out(self) -> ControllPointGraphicsItem:
        return self._cp_out

    @cp_out.setter
    def cp_out(self, cp):
        self.cp_out.setPos(self.mapFromScene(cp))
        self._set_line_out()

    def set_lines(self):
        if self.cps_visible:
            self._set_line_out()
            self._set_line_in()

    def _set_line_in(self):
        self._line_in.setLine(Qt.QLineF(
            self.mapFromScene(self.center),
            self.mapFromScene(self.cp_in.center)))

    def _set_line_out(self):
        self._line_out.setLine(Qt.QLineF(
            self.mapFromScene(self.center),
            self.mapFromScene(self.cp_out.center)))

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        logger.debug("mousePress CubicSplineKnot")
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseMoveEvent(event)
        self.parentItem().update_line()


class TreeLineItemBase(Qt.QGraphicsPathItem):
    _defaults = {"visible": True, "line_data": '{"points":[], "curves":[]}'}

    def __init__(self, *args, data, shape, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        self.shape = shape
        data["line_data"] = json.loads(data["line_data"])
        self._data = data
        [setattr(self, key, value) for key, value in self._data.items()]

        self.curve_knots = []
        self.set_data()
        self.changed = False
        self.hide_knots()

    def shape(self) -> QtGui.QPainterPath:
        # Create a path which closes without increasing its "area"
        # Only clicking exactly the line should activate this item
        path = self.path()
        path.connectPath(self.path().toReversed())
        return path

    def hide_knots(self):
        for knots in self.curve_knots:
            [k.hide() for k in knots]

    def show_knots(self):
        for knots in self.curve_knots:
            [k.show() for k in knots]

    def hide_control_points(self):
        for knots in self.curve_knots:
            [k.hide_control_points() for k in knots]

    def show_control_points(self):
        for knots in self.curve_knots:
            [k.show_control_points() for k in knots]

    def add_knot(self, pos, cpin_pos=None, cpout_pos=None):
        # if first knot, just add knot on the current path

        self.changed = True
        new_knot = CubicSplineKnotItem(self, pos, cpin_pos, cpout_pos)

        self.current_curve_knots.append(new_knot)

        if len(self.current_curve_knots) > 1:
            self.update_line()

    def delete_knot(self, knot):
        self.scene().removeItem(knot)
        for knots in self.curve_knots:
            if knot in knots:
                knots.remove(knot)
        self.update_line()


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
            knots = sorted(knots, key=lambda x: x.center.x())
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
            current = current_point.knot.center
            if p == 0:
                target = QtCore.QLineF(current, knots[p + 1].knot.center)
                source = QtCore.QLineF().fromPolar(
                    target.length(), 180+target.angle()).translated(current)
                source.setPoints(source.p2(), source.p1())
            elif p == len(knots) - 1:
                source = QtCore.QLineF(knots[p - 1].knot.center, current)
                target = QtCore.QLineF().fromPolar(
                    source.length(), source.angle()).translated(current)
            else:
                source = QtCore.QLineF(knots[p - 1].knot.center, current)
                target = QtCore.QLineF(current, knots[p + 1].knot.center)

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
                start_x = int(np.floor(knots[0].knot.as_tuple()[0]))
                end_x = int(np.ceil(knots[-1].knot.as_tuple()[0]))
                regions.append((start_x, end_x))
            else:
                self.curve_knots.remove(knots)
        return regions

    def set_data(self):
        if not self.line_data == {}:
            curves = self.line_data["curves"]

            # Remove current knots before setting new knots
            [[self.scene().removeItem(k) for k in c] for c in self.curve_knots]
            self.curve_knots = []

            # Add knots and controll points for every Curve
            for curve in curves:
                knots = [CubicSplineKnotItem.from_dict(p, parent=self)
                         for p in curve]
                knots = sorted(knots, key=lambda x: x.knot.as_tuple()[0])
                self.curve_knots.append(knots)

            self.update_line()

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
                curve_knots.append(knot.as_dict())
            all_curves.append(curve_knots)
        return {"points": points, "curves": all_curves}


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
        if column in self._data:
            return getattr(self, column)
        elif column == "name":
            return self.annotationtype["name"]

        raise Exception(f"column {column} not in data")


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
            layer = type(self)(data=item_data)
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


class TreeLineItemDB(TreeLineItemBase):
    def __init__(self, data, shape, parent=None, **kwargs):
        super().__init__(data=data, shape=shape, parent=parent, **kwargs)
        self.timer = QtCore.QTimer()
        self.timer.start(10000)
        self.timer.timeout.connect(self.save)

    @classmethod
    def create(cls, data, shape, parent=None):
        data = {**cls._defaults, **data}
        item_data = cls.post_annotation(data)
        return cls(data=item_data, parent=parent, shape=shape)

    @classmethod
    def from_annotation_id(cls, id, parent=None):
        item_data = cls.get_annotation(id, type="slice")
        return cls(data=item_data, parent=parent)

    @staticmethod
    def post_annotation(data):
        logger.debug("post annotation")
        response = requests.post(
            f"{config.api_server}/slicelineannotations/",
            headers=config.auth_header, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Status Code: {response.status_code}\n"
                             f"{response.json()}")

    @staticmethod
    def get_annotation(annotation_id):
        logger.debug("get annotation")
        response = requests.get(
            f"{config.api_server}/slicelineannotations/{annotation_id}",
            headers=config.auth_header)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Status Code: {response.status_code}\n"
                             f"{response.json()}")

    @staticmethod
    def put_annotation(annotation_id, data):
        logger.debug("put annotation")
        response = requests.put(
            f"{config.api_server}/slicelineannotations/{annotation_id}",
            json=data, headers=config.auth_header)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Status Code: {response.status_code}\n"
                             f"{response.json()}")

    @staticmethod
    def delete_annotation(annotation_id):
        logger.debug("delete annotation")
        response = requests.delete(
            f"{config.api_server}/slicelineannotations/{annotation_id}",
            headers=config.auth_header)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Status Code: {response.status_code}\n"
                             f"{response.json()}")

    def save(self):
        # Upload local changes if the layer is active
        if self.changed and not self.view._ctrl_pressed:
            logger.debug(f"Save {self.annotationtype['name']} annotation")
            self._data.update(line_data=json.dumps(self.as_dict()))
            data = self.put_annotation(annotation_id=self._data["id"],
                                       data=self._data)
            self._data = data
            data["line_data"] = json.loads(data["line_data"])
            [setattr(self, key, value) for key, value in self._data.items()]

            self.set_data()
            self.changed = False


class TreeLineItemOffline(TreeLineItemBase):
    def __init__(self, data, shape, parent=None, **kwargs):
        super().__init__(data=data, shape=shape, parent=parent, **kwargs)

        self.timer = QtCore.QTimer()
        self.timer.start(10000)
        self.timer.timeout.connect(self.save)

    @classmethod
    def create(cls, data, shape, parent=None):
        data = {**cls._defaults, **data}
        return cls(data=data, parent=parent, shape=shape)

    @staticmethod
    def delete_annotation(annotation_id):
        pass

    def save(self):
        if self.changed and not self.view._ctrl_pressed:
            self._data.update(line_data=json.dumps(self.as_dict()))
            # Todo Save to some folder
            self.changed=False

