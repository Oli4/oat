from collections import namedtuple
from typing import Tuple, Dict

import numpy as np
import skimage.transform as skitrans
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

from .utils import get_enface_by_id, get_bscan_by_id, get_volume_meta_by_id

Line = namedtuple("Line", ["a", "b", "c"])
Point = namedtuple("Point", ["x", "y"])


class CustomGrahpicsScene(QGraphicsScene):
    def __init__(self, parent, image_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)

        self.image = None
        self.image_meta = None

        self._widthForHeightFactor = 1
        if image_id:
            self.add_image(image_id)

    def _fetch_image(self, image_id) -> Tuple[QGraphicsPixmapItem, Dict]:
        raise NotImplementedError

    def add_image(self, image_id):
        # if image not in scene, fetch and add
        pixmap_item, meta = self._fetch_image(image_id)
        pixmap = pixmap_item.pixmap()
        if not pixmap_item in self.items():
            self.setSceneRect(QRectF(pixmap.rect()))
            self._widthForHeightFactor = \
                1.0 * pixmap.size().width() / pixmap.size().height()

            self.addItem(pixmap_item)


class BscanGraphicsScene(CustomGrahpicsScene):
    def __init__(self, parent, image_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)

        # Fetch Volume image
        self.volume_dict = get_volume_meta_by_id(image_id)
        # Make sure slices are correctly ordered
        self.slices = sorted(self.volume_dict["slices"],
                             key=lambda x: x["number"])

        # Set Scene to first B-Scan
        self.current_slice_number = 0
        self.add_image(self.slices[self.current_slice_number]["id"])

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
        return get_bscan_by_id(image_id)

    def set_slice(self, number):
        if 0 <= number < len(self.slices):
            previous_pixmap, _ = \
                self._fetch_image(self.slices[self.current_slice_number]["id"])
            self.current_slice_number = number
            pixmap, _ = \
                self._fetch_image(self.slices[self.current_slice_number]["id"])
            previous_pixmap.setZValue(0)
            pixmap.setZValue(1)
            if pixmap not in self.items():
                self.addItem(pixmap)

    def next_slice(self):
        self.set_slice(self.current_slice_number + 1)

    def last_slice(self):
        self.set_slice(self.current_slice_number - 1)


class EnfaceGraphicsScene(CustomGrahpicsScene):
    def __init__(self, parent, image_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent, image_id=image_id)

    def _fetch_image(self, image_id) -> Tuple[QGraphicsPixmapItem, Dict]:
        return get_enface_by_id(image_id)

    @property
    def tform(self):
        if self._tform is None:
            raise AttributeError("tform has not been set.")
        else:
            return self._tform

    @tform.setter
    def tform(self, value: skitrans.ProjectiveTransform):
        self._tform = value
