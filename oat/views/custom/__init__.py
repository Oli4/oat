import logging

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsView, QGraphicsItemGroup

logger = logging.getLogger(__name__)


class CustomGraphicsView(QGraphicsView):
    cursorPosChanged = QtCore.pyqtSignal(QtCore.QPointF)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._zoom = 0

        # How to position the scene when transformed (eg zoom)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        # How to position the scene when resizing the widget
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        # Get Move events even if no button is pressed
        self.setMouseTracking(True)

        self._cursor_cross = False
        self.cursorPosChanged.connect(self.set_cursor)

    def toggle_cursor_cross(self):
        if self._cursor_cross:
            # Disable cursor cross
            self.scene().removeItem(self._item_group_cursor_cross)
            self.setCursor(Qt.ArrowCursor)
            self._cursor_cross = False
        else:
            # Enable cursor cross
            self.scene().addItem(self._create_cursor_cross())
            self._cursor_cross = True

    def _create_cursor_cross(self):
        line1 = QtCore.QLineF()
        line2 = QtCore.QLineF()
        line3 = QtCore.QLineF()
        line4 = QtCore.QLineF()

        self._line1 = self.scene().addLine(line1)
        self._line2 = self.scene().addLine(line2)
        self._line3 = self.scene().addLine(line3)
        self._line4 = self.scene().addLine(line4)
        lines = [self._line1, self._line2, self._line3, self._line4]

        self._item_group_cursor_cross = QGraphicsItemGroup()
        [self._item_group_cursor_cross.addToGroup(line) for line in lines]
        return self._item_group_cursor_cross

    def set_cursor(self, pos):
        if self._cursor_cross:
            self.setCursor(Qt.BlankCursor)
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

            self._line1.setLine(line1)
            self._line2.setLine(line2)
            self._line3.setLine(line3)
            self._line4.setLine(line4)

            self._item_group_cursor_cross.setZValue(10)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
        else:
            super().wheelEvent(event)

    def zoomToFit(self):
        rect = self.scene().sceneRect()
        self.fitInView(rect, Qt.KeepAspectRatio)
        # self.fitInView(self.scene().itemsBoundingRect(), Qt.KeepAspectRatio)

    def zoomToFeature(self):
        # Zoom in as long as more than 1/3 of width of the image is
        # visible
        while self.mapToScene(self.rect()).boundingRect().width() \
                > self.scene().width() / 3:
            self.zoom_in()

        # while self.mapToScene(self.rect()).boundingRect() / 4 > self.scene().width():

    def hasPhoto(self):
        if len(self.scene().items()) > 0:
            return True
        else:
            return False

    def zoom_in(self):
        self._zoom += 1
        self.scale(1.25, 1.25)

    def zoom_out(self):
        self._zoom -= 1
        self.scale(0.8, 0.8)
