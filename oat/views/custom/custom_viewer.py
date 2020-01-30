from PyQt5.QtWidgets import QGraphicsView, QAction
from PyQt5 import QtWidgets, QtCore, QtGui

from collections import defaultdict

class CustomGraphicsView(QGraphicsView):

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

        self.line1 = self.scene.addLine(QtCore.QLineF(0, 0, self.width(), 0))
        self.line2 = self.scene.addLine(QtCore.QLineF(0, 0, 0, self.height()))
        self.line1.setZValue(10)
        self.line2.setZValue(10)



        #self.setCursor(QtCore.Qt.CrossCursor)

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


    def move_cross_cursor(self, pos):
        pos = self.mapToScene(pos)
        line1 = QtCore.QLineF(0, pos.y(), self.rect().width(), pos.y())
        line2 = QtCore.QLineF(pos.x(), 0, pos.x(), self.rect().height())
        self.line1.setLine(line1)
        self.line2.setLine(line2)

    def mouseMoveEvent(self, event):
        self.move_cross_cursor(event.pos())

        if self._mouse_pressed and event.modifiers() and QtCore.Qt.ControlModifier:
            newPos = event.pos()
            diff = newPos - self._dragPos
            self._dragPos = newPos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
            event.accept()
        else:
            super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if event.modifiers() & QtCore.Qt.ControlModifier:
                self.setCursor(QtCore.Qt.OpenHandCursor)
            else:
                self.setCursor(QtCore.Qt.ArrowCursor)
            self._mouse_pressed = False
        else:
            super().mouseReleaseEvent(event)






