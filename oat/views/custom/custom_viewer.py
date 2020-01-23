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

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

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
            self._pressed_keys[int(event.key())] = True
            event.accept()
            if self._pressed_keys[int(QtCore.Qt.Key_Control)]:
                self.setCursor(QtCore.Qt.OpenHandCursor)

    def keyReleaseEvent(self, event):
        self._pressed_keys[int(event.key())] = False
        event.accept()

        if not self._pressed_keys[int(QtCore.Qt.Key_Control)]:
            self.setCursor(QtCore.Qt.ArrowCursor)

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


    def mouseMoveEvent(self, event):
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
        super().mouseReleaseEvent(event)

"""

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._mouse_pressed = True
            if event.modifiers() & QtCore.Qt.ControlModifier:
                self.setCursor(QtCore.Qt.ClosedHandCursor)
                self._dragPos = event.pos()
                event.accept()
            else:
                super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
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
                self._ctrl_pressed = False
                self.setCursor(QtCore.Qt.ArrowCursor)
            self._mouse_pressed = False
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        pass

    def keyPressEvent(self, event):
        if not self._mouse_pressed QtCore.Qt.:
            if event.key() == QtCore.Qt.Key_Control:
                self._ctrl_pressed = True

            elif self._ctrl_alt_combined(event):
                self._ctrl_pressed = True
                self._alt_pressed = True
                self.setCursor(QtCore.Qt.OpenHandCursor)
            else:
                super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            self._ctrl_pressed = False
            self.setCursor(QtCore.Qt.ArrowCursor)
        elif event.key() == QtCore.Qt.Key_Alt:
            self._alt_pressed = False
            self.setCursor(QtCore.Qt.ArrowCursor)
        else:
            super().keyPressEvent(event)

    def wheelEvent(self, event):
        if self.hasPhoto():
            if self._ctrl_pressed and self._alt_pressed:
                # Ask the parent to change the data -> change slice
                super().wheelEvent(event)
            else:
                if event.angleDelta().y() > 0:
                    self.zoom_in()
                else:
                    self.zoom_out()

            event.accept()

    def _ctrl_alt_combined(self, event):
        if event.key == QtCore.Qt.Key_Control and event.modifiers() & QtCore.Qt.AltModifier:
            return True
        elif event.key == QtCore.Qt.Key_Alt and event.modifiers() & QtCore.Qt.ControlModifier:
            return True
        else:
            return False





"""









