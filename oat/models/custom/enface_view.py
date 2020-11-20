from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPointF

from oat.views.custom.graphicsview import CustomGraphicsView
from oat.models.utils import get_transformation


class EnfaceView(CustomGraphicsView):
    cursorPosChanged = QtCore.pyqtSignal(QtCore.QPointF, CustomGraphicsView)

    def __init__(self, image_id, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.image_id = image_id
        self._tforms = {}

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def map_from_sender(self, pos, sender):
        tform = self.get_tform(sender)
        result = tform.inverse((pos.x(), pos.y()))[0]
        return QPointF(*result)

    def map_to_sender(self, pos, sender):
        tform = self.get_tform(sender)
        result = tform((pos.x(), pos.y()))[0]
        return QPointF(*result)

    def set_fake_cursor(self, pos, sender):
        if not sender == self:
            pos = QPointF(pos.x(), pos.y())
            pos = self.map_from_sender(pos, sender)
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
        self.enfacePosChanged.emit(scene_pos, self)

    def get_tform(self, other_view):
        id_pair = (self.image_id, other_view.scene().image_id)
        if not id_pair in self._tforms:
            tmodel = "similarity"
            self._tforms[id_pair] = get_transformation(*id_pair, tmodel)
        return self._tforms[id_pair]
