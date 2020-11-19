from typing import Tuple, Dict

import numpy as np
from PyQt5 import QtGui, Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem

from oat.models.custom import CustomGrahpicsScene
from oat.models.custom.scene import Point, Line
from oat.models.utils import get_volume_meta_by_id, get_bscan_by_id, \
    array2qgraphicspixmapitem


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
        self.set_image(self.slices[self.current_slice_number]["id"])

        # Asynchronously load remaining B-Scans

        self.slice_params = [self._line_for_slice(i)
                             for i in range(len(self.slices))]
        self.fake_cursor = self.addPixmap(
            QtGui.QPixmap(":/cursors/cursors/navigation_cursor.svg"))
        self.fake_cursor.setFlag(Qt.QGraphicsItem.ItemIgnoresTransformations)
        self.fake_cursor.hide()

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
