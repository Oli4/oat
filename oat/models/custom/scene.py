from collections import namedtuple
from typing import Tuple, Dict

from PyQt5 import QtGui, QtCore, Qt
from PyQt5.Qt import QBrush, QGraphicsPixmapItem
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsScene

# from .treeitems import *

Line = namedtuple("Line", ["a", "b", "c"])
Point = namedtuple("Point", ["x", "y"])


class CustomGrahpicsScene(QGraphicsScene):
    number = 0
    base_name = "Default"

    def __init__(self, parent, image_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)
        self._set_name()

        self.image = None
        self.image_meta = None

        self._widthForHeightFactor = 1
        # Slice number for OCT Scenes, Enfaceimages are slice 0
        self.current_slice_number = 0

        self.area_annotations = []
        self.background_on = True
        self.fake_cursor = self.addPixmap(
            QtGui.QPixmap(":/cursors/cursors/navigation_cursor.svg"))
        self.fake_cursor.setFlag(Qt.QGraphicsItem.ItemIgnoresTransformations)
        self.fake_cursor.hide()

        # self.background_index = self.index(0, 0, QtCore.QModelIndex())
        # self.setData(self.background_index, self)

        self.image_id = None
        if image_id:
            self.set_image(image_id)

            # self.add_areaannotations(image_id)
            # self.add_shapeannotations(image_id)
            # self.add_overlays()

    def mouseMoveEvent(self, e):
        pass
        # print(self.activePanel())
        # if self.activePanel():
        #    painter = QtGui.QPainter(self.activePanel())
        #    painter.drawPoint(e.x(), e.y())
        #    painter.end()
        #    self.update()

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
        painter.translate(-0.5, -0.5)
        if self.background_on:
            painter.fillRect(self.sceneRect(), self.backgroundBrush())
        else:
            painter.fillRect(self.sceneRect(), QtCore.Qt.NoBrush)

    def set_image(self, image_id):
        self.image_id = image_id
        pixmap_item, meta = self._fetch_image(image_id)
        self.image_meta = meta
        self.shape = (
        pixmap_item.pixmap().height(), pixmap_item.pixmap().width())
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
