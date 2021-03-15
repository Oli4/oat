from PyQt5 import QtGui, QtWidgets, QtCore, Qt

from oat.modules.annotation.models.treeview.lineitem import TreeLineItemDB

class PaintPreview(Qt.QGraphicsItem):
    def __init__(self, settings_widget, parent=None):
        super().__init__(parent)
        self.settings_widget = settings_widget
        self.init_preview()

    def init_preview(self):
        pass

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(0.0,0.0,0.0,0.0)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',
              widget) -> None:
        return None

class Spline(object):
    def __init__(self):
        """ """
        self.name = "spline"
        self.cursor = self.get_cursor()
        self.button = self.get_tool_button()
        self.hot_key = None
        self.options_widget = QtWidgets.QWidget()
        self.paint_preview = PaintPreview(self.options_widget)

    def get_tool_button(self):
        button = QtWidgets.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/path-tool.svg"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(24, 24))
        button.setCheckable(True)
        button.setObjectName("inspectionButton")
        return button

    def get_cursor(self):
        return QtGui.QCursor(
            QtGui.QPixmap(":/cursors/cursors/path_cursor.svg"), hotX=0, hotY=0)

    def mouse_move_handler(self, gitem, event):
        pass

    def mouse_press_handler(self, gitem, event):
        pass

    def mouse_doubleclick_handler(self, gitem, event):
        pos = gitem.mapToScene(event.pos())
        gitem.add_knot(pos)

    def mouse_release_handler(self, gitem, event):
        pass

    def mouse_release_handler(self, gitem, event):
        pass

    def key_press_handler(self, gitem, event):
        pass

    def key_release_handler(self, gitem, event):
        pass