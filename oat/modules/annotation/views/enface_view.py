from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPointF

from oat.modules.annotation.views.graphicsview import CustomGraphicsView
from oat.models.utils import get_transformation
from oat.modules.annotation.models import EnfaceGraphicsScene
from oat.models.utils import get_enface_meta_by_id


class EnfaceView(CustomGraphicsView):
    cursorPosChanged = QtCore.pyqtSignal(QtCore.QPointF, CustomGraphicsView)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.image_id = None
        self._tforms = {}

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    @property
    def scene_tab(self):
        return self.scene.scene_tab

    def get_data(self, image_id, name):
        self.image_id = image_id
        data = get_enface_meta_by_id(self.image_id)
        self.setScene(EnfaceGraphicsScene(parent=self, data=data,
                                          base_name=name))
        self.zoomToFit()

    def map_from_sender(self, pos, sender):
        tform = self.get_tform(sender)
        result = tform((pos.x(), pos.y()))[0]
        return QPointF(*result)

    def map_to_sender(self, pos, sender):
        tform = self.get_tform(sender)
        result = tform.inverse((pos.x(), pos.y()))[0]
        return QPointF(*result)

    def set_fake_cursor(self, pos, sender=None):
        pos = QPointF(pos.x(), pos.y())
        if not sender is None and sender != self:
            pos = self.map_from_sender(pos, sender)
        if self.linked_navigation:
            self.centerOn(pos)
        self.scene().fake_cursor.setPos(pos)
        self.scene().fake_cursor.show()
        self.viewport().update()

    def wheelEvent(self, event):
        if event.modifiers() == (Qt.ControlModifier):
            event.accept()
        else:
            super().wheelEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        scene_pos = self.mapToScene(event.pos())
        if self.tool.paint_preview.scene() == self.scene():
            self.tool.paint_preview.setPos(scene_pos.toPoint())
        self.cursorPosChanged.emit(scene_pos, self)

    def get_tform(self, other_view):
        id_pair = (self.image_id, other_view.scene().image_id)
        if not id_pair in self._tforms:
            tmodel = "similarity"
            self._tforms[id_pair] = get_transformation(*id_pair, tmodel)
        return self._tforms[id_pair]
