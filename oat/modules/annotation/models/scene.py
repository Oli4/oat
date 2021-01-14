from collections import namedtuple
from typing import Tuple, Dict

from PyQt5 import QtGui, QtCore, Qt
from PyQt5.Qt import QBrush, QGraphicsPixmapItem
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsScene

from .scenetab import SceneTab

Line = namedtuple("Line", ["a", "b", "c"])
Point = namedtuple("Point", ["x", "y"])


class CustomGrahpicsScene(QGraphicsScene):
    number = 0
    base_name = "Default"

    def __init__(self, parent, image_id, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)
        self.image_id = image_id
        self._set_name()
        self.tool = None

        self.image = None
        self.image_meta = None
        self.shape = None

        self._widthForHeightFactor = 1

        self.area_annotations = []
        self.background_on = True
        self.fake_cursor = self.addPixmap(
            QtGui.QPixmap(":/cursors/cursors/navigation_cursor.svg"))
        self.fake_cursor.setFlag(Qt.QGraphicsItem.ItemIgnoresTransformations)
        self.fake_cursor.hide()

        self.set_image()
        self.scene_tab = SceneTab(self)

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

    def set_image(self):
        pixmap_item, meta = self._fetch_image(self.image_id)
        self.image_meta = meta
        pixmap = pixmap_item.pixmap()
        self.shape = (pixmap.height(), pixmap.width())

        self.setSceneRect(QRectF(pixmap.rect()))
        self._widthForHeightFactor = \
            1.0 * pixmap.size().width() / pixmap.size().height()
        self.setBackgroundBrush(QBrush(pixmap))

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

    def mouseMoveEvent(self, event):
        self.fake_cursor.hide()
        # Set tool preview
        super().mouseMoveEvent(event)

