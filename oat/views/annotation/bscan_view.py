from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF

from oat.views.custom import CustomGraphicsView


class BscanView(CustomGraphicsView):
    pixelClicked = QtCore.pyqtSignal(QtCore.QPoint)
    localizerPosChanged = QtCore.pyqtSignal(QtCore.QPointF, CustomGraphicsView)

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

            localizer_pos = self.map_to_localizer(
                QPointF(event.pos().x(), self.scene().current_slice_number))
            self.localizerPosChanged.emit(localizer_pos, self)

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
        # x = StartX + xpos
        # y = StartY + StartY-EndY/lenx * xpos
        slice_n = int(pos.y())
        lclzr_scale_x = self.scene().volume_dict["localizer_image"]["scale_x"]
        lclzr_scale_y = self.scene().volume_dict["localizer_image"]["scale_y"]
        start_y = self.scene().slices[slice_n]["start_y"] / lclzr_scale_y
        end_y = self.scene().slices[slice_n]["end_y"] / lclzr_scale_y
        size_x = self.scene().volume_dict["size_x"]

        x = self.scene().current_slice["start_x"] / lclzr_scale_x + pos.x()
        y = start_y + (start_y - end_y) / size_x * pos.x()

        return QPointF(x, y)

    def map_from_localizer(self, pos):
        lclzr_scale_x = self.scene().volume_dict["localizer_image"]["scale_x"]
        x = pos.x() - self.scene().current_slice["start_x"] / lclzr_scale_x
        y = self.scene().closest_slice(pos)

        return QPointF(x, y)

    def set_cursor_from_localizer(self, pos, sender):
        if sender is not self:
            # Turn localizer position to x pos and slice number for OCT
            pos = self.map_from_localizer(pos)
            # set slice
            self.scene().set_slice(int(pos.y()))
            # set cursor x position
            # hide vertical line
            self._line1.hide()
            self._line2.hide()
            pos = QPointF(pos.x(), 5)
            self.set_cursor(pos)
            self.centerOn(pos)

            self.viewport().update()

    def mouseMoveEvent(self, event):
        # Show vertical line
        self._line1.show()
        self._line2.show()
        super().mouseMoveEvent(event)

        scene_pos = self.mapToScene(event.pos())
        localizer_pos = self.map_to_localizer(
            QPointF(scene_pos.x(), self.scene().current_slice_number))
        self.localizerPosChanged.emit(localizer_pos, self)
        self.cursorPosChanged.emit(scene_pos)

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
            self.viewport().update()
