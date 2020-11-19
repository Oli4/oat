from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPointF

from oat.views.custom.graphicsview import CustomGraphicsView


class EnfaceView(CustomGraphicsView):
    enfacePosChanged = QtCore.pyqtSignal(QtCore.QPointF, CustomGraphicsView)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def map_to_localizer(self, pos):
        result = self.scene().tform((pos.x(), pos.y()))[0]
        return QPointF(*result)

    def map_from_localizer(self, pos):
        result = self.scene().tform.inverse((pos.x(), pos.y()))[0]
        return QPointF(*result)

    def set_fake_cursor(self, pos, sender):
        if not sender == self:
            pos = QPointF(pos.x(), pos.y())
            pos = self.map_from_localizer(pos)
            self.centerOn(pos)
            self.scene().fake_cursor.setPos(pos)
            self.scene().fake_cursor.show()
            self.viewport().update()

    def wheelEvent(self, event):
        if event.modifiers() == (Qt.ControlModifier):
            self.parent().wheelEvent(event)
            # Ask the parent to change the data -> change slice
            event.accept()
        else:
            super().wheelEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.scene().fake_cursor.hide()
        scene_pos = self.mapToScene(event.pos())
        localizer_pos = self.map_to_localizer(scene_pos)
        self.enfacePosChanged.emit(localizer_pos, self)
