from collections import defaultdict

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsView


class CustomGraphicsView(QGraphicsView):
    cursorPosChanged = QtCore.pyqtSignal(QtCore.QPointF)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._zoom = 0
        self._empty = True

        self._pressed_keys = defaultdict(lambda: False)
        self._mouse_pressed = False

        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setMouseTracking(True)

        self.create_cursor_cross()
        self.cursorPosChanged.connect(self.set_cursor_cross)
        self.setCursor(QtCore.Qt.BlankCursor)

    def hasPhoto(self):
        return not self._empty

    def zoom_in(self):
        self._zoom += 1
        self.scale(1.25, 1.25)

    def zoom_out(self):
        self._zoom -= 1
        self.scale(0.8, 0.8)


    def keyPressEvent(self, event):
        if not self._mouse_pressed:
            if int(event.key()) == int(QtCore.Qt.Key_Control):
                self.setCursor(QtCore.Qt.OpenHandCursor)
            event.accept()

    def keyReleaseEvent(self, event):
        if int(event.key()) == int(QtCore.Qt.Key_Control):
            self.setCursor(QtCore.Qt.ArrowCursor)
        else:
            super().keyReleaseEvent((event))

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.modifiers() == (QtCore.Qt.ControlModifier):
                self.parent().wheelEvent(event)
                # Ask the parent to change the data -> change slice
            else:
                if event.angleDelta().y() > 0:
                    self.zoom_in()
                else:
                    self.zoom_out()

        event.accept()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._mouse_pressed = True
            if event.modifiers() & QtCore.Qt.ControlModifier:
                self.setCursor(QtCore.Qt.ClosedHandCursor)
                self._dragPos = event.pos()
                event.accept()
            else:
                super().mousePressEvent(event)

    def create_cursor_cross(self):
        line1 = QtCore.QLineF()
        line2 = QtCore.QLineF()
        line3 = QtCore.QLineF()
        line4 = QtCore.QLineF()

        self.line1 = self.scene.addLine(line1)
        self.line2 = self.scene.addLine(line2)
        self.line3 = self.scene.addLine(line3)
        self.line4 = self.scene.addLine(line4)
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

    def mouseMoveEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        self.cursorPosChanged.emit(scene_pos)

        # Compute position on current item
        item = self.scene.itemAt(event.pos(), QtGui.QTransform())
        if item:
            # Item pos is currently always 0, 0 since items are only images which were never moved
            # The top left pixel has pos (0<1, 0<1)
            item_pos = scene_pos - item.pos()
            print(item_pos.x(), item_pos.y())


        if self._mouse_pressed and event.modifiers() and QtCore.Qt.ControlModifier:
            newPos = event.pos()
            diff = newPos - self._dragPos
            self._dragPos = newPos
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - diff.x())
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - diff.y())
            event.accept()
        else:
            super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if event.modifiers() & QtCore.Qt.ControlModifier:
                self.setCursor(QtCore.Qt.OpenHandCursor)
            else:
                self.setCursor(QtCore.Qt.BlankCursor)
            self._mouse_pressed = False
        else:
            super().mouseReleaseEvent(event)






