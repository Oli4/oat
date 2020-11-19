from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QPointF

from oat.views.custom.graphicsview import CustomGraphicsView


class BscanView(CustomGraphicsView):
    volumePosChanged = QtCore.pyqtSignal(QtCore.QPointF, CustomGraphicsView)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.current_slice=0

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def next_slice(self):
        self.current_slice +=1

    def last_slice(self):
        self.current_slice -=1

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

    def set_fake_cursor(self, pos, sender):
        if not sender == self:
            # Turn localizer position to x pos and slice number for OCT
            pos = self.map_from_localizer(pos)
            # set slice
            self.scene().set_slice(int(pos.y()))

            current_center = self.mapToScene(self.rect().center()).y()
            pos = QPointF(pos.x(), current_center)
            self.centerOn(pos)
            self.scene().fake_cursor.setPos(pos)
            self.scene().fake_cursor.show()
            self.viewport().update()

    def wheelEvent(self, event):
        if event.modifiers() == (QtCore.Qt.ControlModifier):
            if event.angleDelta().y() > 0:
                self.next_slice()
            else:
                self.last_slice()

            pos_on_localizer = self.map_to_localizer(
                QPointF(self.mapToScene(event.pos()).x(),
                        self.scene().current_slice_number))
            self.volumePosChanged.emit(pos_on_localizer, self)

            self.parent().wheelEvent(event)
            # Ask the parent to change the data -> change slice
            event.accept()
        else:
            super().wheelEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.scene().fake_cursor.hide()
        scene_pos = self.mapToScene(event.pos())
        localizer_pos = self.map_to_localizer(
            QtCore.QPointF(scene_pos.x(),
                           self.scene().current_slice_number))
        self.volumePosChanged.emit(localizer_pos, self)
