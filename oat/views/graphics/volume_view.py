from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtCore import QPointF

from oat.views.custom.graphicsview import CustomGraphicsView
from oat.models.custom.bscanscene import BscanGraphicsScene
from oat.models.utils import get_volume_meta_by_id
from oat.models.custom.scene import Point, Line
import numpy as np

class VolumeView(CustomGraphicsView):
    volumePosChanged = QtCore.pyqtSignal(QtCore.QPointF, CustomGraphicsView)
    sceneChanged = QtCore.pyqtSignal(Qt.QGraphicsScene)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.volume_id = None
        self.current_slice = None
        self._bscan_scenes = {}
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def get_data(self, volume_id, name="OCT"):
        self.volume_id = volume_id
        self.name = name
        self.current_slice = 0

        self.volume_dict = get_volume_meta_by_id(volume_id)
        self.slices = sorted(self.volume_dict["slices"],
                             key=lambda x: x["number"])
        self.slice_lines = self._slice_lines()

        self.set_current_scene()
        self.zoomToFit()

    @property
    def bscan_scene(self):
        if not self.current_slice in self._bscan_scenes:
            self._bscan_scenes[self.current_slice] = BscanGraphicsScene(
                parent=self, data=self.slices[self.current_slice],
                base_name=self.name)
        return self._bscan_scenes[self.current_slice]


    def set_current_scene(self):
        self.setScene(self.bscan_scene)
        self.sceneChanged.emit(self.bscan_scene)

    def next_slice(self):
        if self.current_slice < len(self.slices) - 1:
            self.current_slice +=1
            self.set_current_scene()

    def last_slice(self):
        if self.current_slice > 0:
            self.current_slice -=1
            self.set_current_scene()

    def map_to_localizer(self, pos):
        # x = StartX + xpos
        # y = StartY + StartY-EndY/lenx * xpos
        slice_n = int(pos.y())
        lclzr_scale_x = self.volume_dict["localizer_image"]["scale_x"]
        lclzr_scale_y = self.volume_dict["localizer_image"]["scale_y"]
        start_y = self.slices[slice_n]["start_y"] / lclzr_scale_y
        end_y = self.slices[slice_n]["end_y"] / lclzr_scale_y
        size_x = self.volume_dict["size_x"]

        x = self.slices[slice_n]["start_x"] / lclzr_scale_x + pos.x()
        y = start_y + (start_y - end_y) / size_x * pos.x()

        return QPointF(x, y)

    def map_from_localizer(self, pos):
        lclzr_scale_x = self.volume_dict["localizer_image"]["scale_x"]
        x = pos.x() - self.slices[self.current_slice]["start_x"] / lclzr_scale_x
        y = self.closest_slice(pos)
        return QPointF(x, y)

    def set_fake_cursor(self, pos, sender):
        # Turn localizer position to x pos and slice number for OCT
        pos = self.map_from_localizer(pos)
        # set slice
        self.current_slice = int(pos.y())
        self.set_current_scene()

        current_center = self.mapToScene(self.rect().center()).y()
        pos = QPointF(pos.x(), current_center)
        self.centerOn(pos) # Todo: Make this optional
        self.scene().fake_cursor.setPos(pos)
        self.scene().fake_cursor.show()

        # ToDo: this is an overkill, update only cursor position
        self.viewport().update()

    def wheelEvent(self, event):
        if event.modifiers() == (QtCore.Qt.ControlModifier):
            if event.angleDelta().y() > 0:
                self.next_slice()
            else:
                self.last_slice()

            pos_on_localizer = self.map_to_localizer(
                QPointF(self.mapToScene(event.pos()).x(), self.current_slice))
            self.volumePosChanged.emit(pos_on_localizer, self)

            self.parent().wheelEvent(event)
            # Ask the parent to change the data -> change slice
            event.accept()
        else:
            super().wheelEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.scene().fake_cursor.hide()
        scene_pos = self.mapToScene(event.pos())
        localizer_pos = self.map_to_localizer(
            QtCore.QPointF(scene_pos.x(), self.current_slice))
        self.volumePosChanged.emit(localizer_pos, self)

    def _slice_lines(self):
        lines = []
        for sl in self.slices:
            lclzr_scale_x = self.volume_dict["localizer_image"]["scale_x"]
            lclzr_scale_y = self.volume_dict["localizer_image"]["scale_y"]
            start_x = sl["start_x"] / lclzr_scale_x
            start_y = sl["start_y"] / lclzr_scale_y
            end_x = sl["end_x"] / lclzr_scale_x
            end_y = sl["end_y"] / lclzr_scale_y

            p1 = Point(start_x, start_y)
            p2 = Point(end_x, end_y)
            a = p1.y - p2.y
            b = p2.x - p1.x
            c = a * p2.x + b * p2.y
            lines.append(Line(a, b, -c))
        return lines

    def closest_slice(self, pos):
        # Todo: Make this faster for smooth registered navigation
        point = Point(pos.x(), pos.y())

        smallest_dist = self.point_line_distance(point, self.slice_lines[0])
        for i, line in enumerate(self.slice_lines):
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
