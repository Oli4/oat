from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF

from oat.views.custom import CustomGraphicsView


class BscanView(CustomGraphicsView):
    pixelClicked = QtCore.pyqtSignal(QtCore.QPoint)
    localizerPosChanged = QtCore.pyqtSignal(QtCore.QPointF)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._mouse_pressed = False
        self._dragging = False

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event):
        if event.modifiers() == (Qt.ControlModifier):
            if event.angleDelta().y() > 0:
                self.next_slice()
            else:
                self.last_slice()
            self.parent().wheelEvent(event)
            # Ask the parent to change the data -> change slice
            event.accept()
        else:
            super().wheelEvent(event)

    def next_slice(self):
        self.scene().next_slice()

    def last_slice(self):
        self.scene().last_slice()

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

    def map_to_localizer(self, pos):
        return QPointF(pos.x() * 1.5, pos.y() * 30)

    def map_from_localizer(self, pos):
        return QPointF(pos.x() / 1.5, pos.y() / 30)

    def set_cursor_from_localizer(self, pos):
        pos = self.map_from_localizer(pos)
        # set slice
        self.scene().set_slice(int(pos.y() - 0.5))
        # set cursor x position
        self.set_cursor(QPointF(pos.x(), -100))

    def mouseMoveEvent(self, event):
        scene_pos = self.mapToScene(event.pos())

        localizer_pos = self.map_to_localizer(
            QPointF(scene_pos.x(), self.scene().current_slice + 0.5))
        self.localizerPosChanged.emit(localizer_pos)
        self.cursorPosChanged.emit(scene_pos)

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
