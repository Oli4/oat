from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt

from oat.views.custom.graphicsview import CustomGraphicsView


class LocalizerView(CustomGraphicsView):
    localizerPosChanged = QtCore.pyqtSignal(QtCore.QPointF, CustomGraphicsView)
    pixelClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

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
        self.localizerPosChanged.emit(scene_pos, self)

    def set_fake_cursor(self, pos, sender):
        if not sender == self:
            pos = QtCore.QPointF(pos.x(), pos.y())
            self.scene().fake_cursor.setPos(pos)
            self.scene().fake_cursor.show()
            self.centerOn(pos)
            self.localizerPosChanged.emit(pos, sender)
            self.viewport().update()
