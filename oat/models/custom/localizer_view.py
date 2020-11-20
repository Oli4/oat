from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt

from oat.views.custom.graphicsview import CustomGraphicsView
from .enfacescene import EnfaceGraphicsScene

class LocalizerView(CustomGraphicsView):
    cursorPosChanged = QtCore.pyqtSignal(QtCore.QPointF, CustomGraphicsView)

    def __init__(self, image_id, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.image_id = localizer_id
        self.scene = EnfaceGraphicsScene(image_id=self.localizer_id, )

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

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
        self.cursorPosChanged.emit(scene_pos, self)

    def set_fake_cursor(self, pos, sender):
        if not sender == self:
            pos = QtCore.QPointF(pos.x(), pos.y())
            self.scene().fake_cursor.setPos(pos)
            self.scene().fake_cursor.show()
            self.centerOn(pos)
            self.cursorPosChanged.emit(pos, sender)
            self.viewport().update()


