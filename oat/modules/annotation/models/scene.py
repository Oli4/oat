from collections import namedtuple
from typing import Tuple, Dict

from PySide6 import QtGui, QtCore, Qt, QtWidgets
from PySide6.QtCore import QRectF

from .scenetab import SceneTab
from oat.modules.annotation.tools import Inspection

from oat.utils import handle_exception_in_method

Line = namedtuple("Line", ["a", "b", "c"])
Point = namedtuple("Point", ["x", "y"])


class CustomGrahpicsScene(QtWidgets.QGraphicsScene):
    number = 0
    base_name = "Default"
    toolChanged = QtCore.Signal(object)

    def __init__(self, parent, image_id, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)
        self.image_id = image_id
        self._set_name()
        self._current_tool = None
        self.current_tool = Inspection()

        self.image = None
        self.image_meta = None
        self.shape = None

        self._widthForHeightFactor = 1

        self.background_on = True
        self.fake_cursor = self.addPixmap(
            QtGui.QPixmap(":/cursors/cursors/navigation_cursor.svg"))
        self.fake_cursor.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
        self.fake_cursor.hide()

        self.set_image()
        self.scene_tab = SceneTab(self)

        self.grabber_cache = None
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

    @property
    
    def current_tool(self):
        return self._current_tool

    @current_tool.setter
    def current_tool(self, tool):
        self.toolChanged.emit(tool)
        self._current_tool = tool

    def _set_name(self):
        if self.number == 0:
            self.name = self.base_name
            self.number += 1
        else:
            self.name = f"{self.base_name}_{self.number}"
            self.number += 1

    def _fetch_image(self, image_id) -> Tuple[QtWidgets.QGraphicsPixmapItem, Dict]:
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
        self.setBackgroundBrush(QtGui.QBrush(pixmap))

    def hide_background(self):
        if self.background_on:
            self.background_on = False
            self.invalidate(self.sceneRect(), QtWidgets.QGraphicsScene.BackgroundLayer)

    def show_background(self):
        if not self.background_on:
            self.background_on = True
            self.invalidate(self.sceneRect(), QtWidgets.QGraphicsScene.BackgroundLayer)

    
    def mouseMoveEvent(self, event):
        self.fake_cursor.hide()
        super().mouseMoveEvent(event)

    
    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        # Do not handle the event in ScrollHandDrag Mode to not interfere
        if self.views()[0].dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            return

        super().mousePressEvent(event)
        if not event.isAccepted():
            self.grabber_cache = self.mouseGrabberItem()
            if not self.grabber_cache is None:
                self.grabber_cache.ungrabMouse()
            super().mousePressEvent(event)

    
    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if self.views()[0].dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            return

        super().mouseReleaseEvent(event)
        if not self.grabber_cache is None:
            self.grabber_cache.grabMouse()

