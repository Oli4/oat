from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint

from oat.views.custom import CustomGraphicsView


class LocalizerView(CustomGraphicsView):
    cursorPosChanged = QtCore.pyqtSignal(QtCore.QPointF)
    localizerPosChanged = QtCore.pyqtSignal(QtCore.QPointF)
    pixelClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._mouse_pressed = False
        self._dragging = False

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event):
        if event.modifiers() == (Qt.ControlModifier):
            self.parent().wheelEvent(event)
            # Ask the parent to change the data -> change slice
            event.accept()
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Control:
            self.setCursor(Qt.OpenHandCursor)

    def keyReleaseEvent(self, event):
        super().keyReleaseEvent(event)
        if not self._mouse_pressed:
            if event.key() == Qt.Key_Control:
                self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._mouse_pressed = True
            if event.modifiers() & Qt.ControlModifier:
                self.setCursor(Qt.ClosedHandCursor)
                self._dragging = True
                self._dragPos = event.pos()
                event.accept()
            else:
                point = self.mapToScene(event.pos())
                point = QPoint(int(point.x()), int(point.y()))
                self.pixelClicked.emit(point)

    def mouseMoveEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        self.cursorPosChanged.emit(scene_pos)
        self.localizerPosChanged.emit(scene_pos)

        super().mouseMoveEvent(event)
        if self._mouse_pressed and self._dragging:
            newPos = event.pos()
            diff = newPos - self._dragPos
            self._dragPos = newPos
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - diff.x())
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - diff.y())

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            if event.modifiers() & Qt.ControlModifier:
                self.setCursor(Qt.OpenHandCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
                self._dragging = False
            self._mouse_pressed = False

    def set_cursor(self, pos):
        super().set_cursor(pos)
        self.localizerPosChanged.emit(pos)
