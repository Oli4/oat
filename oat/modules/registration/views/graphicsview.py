import logging

import math
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QGraphicsView

logger = logging.getLogger(__name__)


class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._zoom = 0
        self._ctrl_pressed = False

        self.linked_navigation=False

        # How to position the scene when transformed (eg zoom)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        # How to position the scene when resizing the widget
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        # Get Move events even if no button is pressed
        self.setMouseTracking(True)
        self.deactivate_scroll_bars()

        self.tool = None

    def set_tool(self, tool):
        self.tool = tool
        self.setCursor(tool.cursor)

    def hasWidthForHeight(self):
        return True

    def widthForHeight(self, height):
        return math.ceil(height * self.scene()._widthForHeightFactor)

    def toggle_scroll_bars(self):
        if self._scroll_bars:
            self.deactivate_scroll_bars()
        else:
            self.activate_scroll_bars()

    def deactivate_scroll_bars(self):
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._scroll_bars = False

    def activate_scroll_bars(self):
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self._scroll_bars = True

    def zoomToFit(self):
        self.fitInView(self.scene().sceneRect(), QtCore.Qt.KeepAspectRatio)
        self._zoom = 0

    def zoomToFeature(self):
        # Zoom in as long as more than 1/3 of width of the image is
        # visible
        while self.mapToScene(self.rect()).boundingRect().width() \
                > self.scene().width() / 3:
            self.zoom_in()

    def zoom_in(self):
        self._zoom += 1
        self.scale(1.25, 1.25)

    def zoom_out(self):
        if self._zoom > 0:
            self._zoom -= 1
            self.scale(0.8, 0.8)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        pos = self.mapToScene(event.pos())
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()
        self.centerOn(pos)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        # self.zoomToFit()
        # height = event.size().height()
        # width = self.widthForHeight(height)
        # self.setBaseSize(width, height)
        # self.setMinimumSize(width, height)

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        self.zoomToFit()

    def mousePressEvent(self, event):
        if self._ctrl_pressed:
            super().mousePressEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        # Current tool action
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            super().keyPressEvent(event)
            self._ctrl_pressed = True
        event.accept()

    def keyReleaseEvent(self, event):
        super().keyReleaseEvent(event)
        if event.key() == QtCore.Qt.Key_Control:
            self.setDragMode(QGraphicsView.NoDrag)
            self._ctrl_pressed = False
            self.setCursor(self.tool.cursor)
        event.accept()

    def mouseMoveEvent(self, event):
        #self.scene().fake_cursor.hide()
        if self._ctrl_pressed:
            super().mouseMoveEvent(event)
        event.accept()