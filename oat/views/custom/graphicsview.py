import logging

import math
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QGraphicsView

logger = logging.getLogger(__name__)


class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._zoom = 0
        self._mouse_left_pressed = False
        self._mouse_right_pressed = False
        self._ctrl_pressed = False
        self._dragging = False

        # How to position the scene when transformed (eg zoom)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        # How to position the scene when resizing the widget
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        # Get Move events even if no button is pressed
        self.setMouseTracking(True)
        self.deactivate_scroll_bars()

        self._cursors = None
        self._active_tool = None

    @property
    def cursors(self):
        if self._cursors is None:
            bm = QtGui.QPixmap(":/cursors/cursors/navigation_cursor.svg")
            navigation_cursor = QtGui.QCursor(bm, hotX=0, hotY=0)
            bm = QtGui.QPixmap(":/cursors/cursors/pen_cursor.svg")
            pen_cursor = QtGui.QCursor(bm, hotX=0, hotY=0)

            self._cursors = {"navigation": navigation_cursor,
                             "pen": pen_cursor}
        return self._cursors

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

        # while self.mapToScene(self.rect()).boundingRect() / 4 > self.scene().width():

    def hasPhoto(self):
        if len(self.scene().items()) > 0:
            return True
        else:
            return False

    def zoom_in(self):
        self._zoom += 1
        self.scale(1.25, 1.25)

    def zoom_out(self):
        if self._zoom > 0:
            self._zoom -= 1
            self.scale(0.8, 0.8)

    def set_active_tool(self, tool=None):
        if tool is None:
            tool = self._active_tool
        if tool in self.cursors:
            self._active_tool = tool
            self.setCursor(self.cursors[tool])

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if self.hasPhoto():
            pos = self.mapToScene(event.pos())
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            self.centerOn(pos)
        else:
            super().wheelEvent(event)

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
        super().mousePressEvent(event)
        scene_pos = self.mapToScene(event.pos())
        if self._active_tool == "navigation":
            if event.button() == QtCore.Qt.LeftButton:
                self._mouse_left_pressed = True
                if event.modifiers() & QtCore.Qt.ControlModifier:
                    self.setCursor(QtCore.Qt.ClosedHandCursor)
                    self._dragging = True
                    self._dragPos = event.pos()
                    event.accept()
        elif self._active_tool == "pen":
            layer = self.scene().focusItem()
            if event.button() == QtCore.Qt.LeftButton:
                self._mouse_left_pressed = True
                if layer:
                    layer.add_pixel(scene_pos.toPoint())
            if event.button() == QtCore.Qt.RightButton:
                self._mouse_right_pressed = True
                if layer:
                    layer.remove_pixel(scene_pos.toPoint())
            event.accept()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self._dragging = False
        if event.button() == QtCore.Qt.LeftButton:
            self._mouse_left_pressed = False
        elif event.button() == QtCore.Qt.RightButton:
            self._mouse_right_pressed = False
        if not self._ctrl_pressed:
            self.set_active_tool()
            self.viewport().update()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Control:
            self.setCursor(QtCore.Qt.OpenHandCursor)
            self._ctrl_pressed = True

    def keyReleaseEvent(self, event):
        super().keyReleaseEvent(event)
        if event.key() == QtCore.Qt.Key_Control:
            self._ctrl_pressed = False
            if not self._mouse_left_pressed:
                self.set_active_tool()

    def mouseMoveEvent(self, event):
        if self._active_tool == "pen":
            layer = self.scene().focusItem()
            if layer:
                if self._mouse_left_pressed:
                    layer.add_pixel(self.mapToScene(event.pos()).toPoint())
                elif self._mouse_right_pressed:
                    layer.remove_pixel(self.mapToScene(event.pos()).toPoint())

        elif self._active_tool == "navigation":
            if self._mouse_left_pressed and self._dragging:
                newPos = event.pos()
                diff = newPos - self._dragPos
                self._dragPos = newPos
                self.horizontalScrollBar().setValue(
                    self.horizontalScrollBar().value() - diff.x())
                self.verticalScrollBar().setValue(
                    self.verticalScrollBar().value() - diff.y())
