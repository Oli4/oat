from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint

from oat.views.custom import CustomGraphicsView


class FeatureSelectionView(CustomGraphicsView):
    cursorPosChanged = QtCore.pyqtSignal(QtCore.QPointF)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.model = parent.model
        self._selectionModel = None

        self._mouse_pressed = False
        self._dragging = False

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    @property
    def selectionModel(self):
        return self._selectionModel

    @selectionModel.setter
    def selectionModel(self, value):
        self._selectionModel = value

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
                self.model.setData(self.selectionModel.currentIndex(), point)

    def mouseMoveEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
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

    def create_cursor_cross(self):
        line1 = QtCore.QLineF()
        line2 = QtCore.QLineF()
        line3 = QtCore.QLineF()
        line4 = QtCore.QLineF()

        self.line1 = self.scene().addLine(line1)
        self.line2 = self.scene().addLine(line2)
        self.line3 = self.scene().addLine(line3)
        self.line4 = self.scene().addLine(line4)
        [line.setZValue(10) for line in
         [self.line1, self.line2, self.line3, self.line4]]

    def set_cursor_cross(self, pos):
        pos = pos.toPoint()

        # Map viewport size to scene
        pos_end = self.mapToScene(self.viewport().rect().width(),
                                  self.viewport().rect().height()).toPoint()
        pos_start = self.mapToScene(0, 0).toPoint()

        # Create new line and set it.
        line1 = QtCore.QLineF(int(pos_start.x()), int(pos.y()) + 0.5,
                              int(pos.x()) - 1.5,
                              int(pos.y()) + 0.5)
        line2 = QtCore.QLineF(int(pos.x()) + 2.5, int(pos.y()) + 0.5,
                              int(pos_end.x()),
                              int(pos.y()) + 0.5)

        line3 = QtCore.QLineF(int(pos.x()) + 0.5, int(pos_start.y()),
                              int(pos.x()) + 0.5, int(pos.y()) - 1.5)
        line4 = QtCore.QLineF(int(pos.x()) + 0.5, int(pos.y()) + 2.5,
                              int(pos.x()) + 0.5, int(pos_end.y()))

        self.line1.setLine(line1)
        self.line2.setLine(line2)
        self.line3.setLine(line3)
        self.line4.setLine(line4)


