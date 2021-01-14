from PyQt5 import QtGui, QtWidgets, QtCore, Qt
from oat.views.ui.ui_pen_options import Ui_penOptions

class PenWidget(QtWidgets.QWidget, Ui_penOptions):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.sizeSlider.valueChanged.connect(self.set_label)
        self.set_label()

    def set_label(self):
        self.sizeLabel.setText(f"Size: {self.sizeSlider.value()}")


class PaintPreview(Qt.QGraphicsPixmapItem):
    def __init__(self, tool, parent=None):
        super().__init__(parent)
        self.tool = tool
        self.settings_widget = tool.options_widget
        self.settings_widget.sizeSlider.valueChanged.connect(self.set_preview)
        self.set_preview()

    def set_preview(self):
        diameter = self.settings_widget.sizeSlider.value()
        pm = Qt.QPixmap(diameter+1, diameter+1)
        pm.fill(QtCore.Qt.transparent)
        painter = Qt.QPainter(pm)
        pen = Qt.QPen(QtCore.Qt.red)
        painter.setPen(pen)
        painter.setBackgroundMode(QtCore.Qt.TransparentMode)
        painter.drawPixmap(0, 0, self.tool.mask)
        painter.end()

        self.setPixmap(pm)
        offset = self.settings_widget.sizeSlider.value() // 2
        self.setOffset(-offset, -offset)
        self.setOpacity(0.25)


class Pen(object):
    def __init__(self):
        """ """
        self.name = "pen"
        self._masks = {}
        self.cursor = self.get_cursor()
        self.button = self.get_tool_button()
        self.hot_key = None
        self.options_widget = self.get_options_widget()
        self.paint_preview = self.get_paint_preview()

    @property
    def mask(self):
        diameter = self.options_widget.sizeSlider.value()
        if diameter not in self._masks:
            bm = Qt.QBitmap(diameter+1, diameter+1)
            bm.fill(QtCore.Qt.color0)
            painter = Qt.QPainter(bm)
            brush = Qt.QBrush()
            brush.setStyle(QtCore.Qt.SolidPattern)
            painter.setBrush(brush)
            painter.drawEllipse(0,0, diameter, diameter)
            painter.end()
            self._masks[diameter] = bm

        return self._masks[diameter]

    def get_paint_preview(self):
        return PaintPreview(self)

    def get_options_widget(self):
        widget = PenWidget()
        return widget

    def get_tool_button(self):
        button = QtWidgets.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-edit-24px.svg"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(24, 24))
        button.setCheckable(True)
        button.setObjectName("penButton")
        return button

    def get_cursor(self):
        return QtGui.QCursor(
            QtGui.QPixmap(":/cursors/cursors/pen_cursor.svg"), hotX=0, hotY=0)

    def get_painter(self, gitem):
        painter = Qt.QPainter(gitem.qimage)
        color = Qt.QColor(f"#{gitem.current_color}")
        brush = Qt.QBrush()
        brush.setStyle(QtCore.Qt.SolidPattern)
        brush.setColor(color)
        painter.setPen(color)
        painter.setBrush(brush)
        return painter

    def draw(self, gitem, pos):
        radius = self.options_widget.sizeSlider.value() / 2
        painter = self.get_painter(gitem)
        painter.setBackgroundMode(QtCore.Qt.TransparentMode)
        pos = Qt.QPointF(pos.x()-radius, pos.y()-radius)
        painter.drawPixmap(pos, self.mask)
        painter.end()

        gitem.update_pixmap()
        gitem.changed = True

    def erase(self, gitem, pos):
        radius = self.options_widget.sizeSlider.value() / 2
        painter = self.get_painter(gitem)
        painter.setCompositionMode(Qt.QPainter.CompositionMode_Clear)
        pos = Qt.QPointF(pos.x() - radius, pos.y() - radius)
        painter.drawPixmap(pos, self.mask)
        painter.end()

        gitem.update_pixmap()
        gitem.changed = True

    def mouse_move_handler(self, gitem: "TreeAreaItem", event):
        pos = gitem.mapToScene(event.pos()).toPoint()
        if event.buttons() & QtCore.Qt.LeftButton:
            self.draw(gitem, pos)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.erase(gitem, pos)

    def mouse_press_handler(self, gitem, event):
        pos = gitem.mapToScene(event.pos()).toPoint()
        if event.buttons() & QtCore.Qt.LeftButton:
            self.draw(gitem, pos)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.erase(gitem, pos)

    @staticmethod
    def mouse_release_handler(gitem, event):
        pass

    @staticmethod
    def key_press_handler(gitem, event):
        pass

    @staticmethod
    def key_release_handler(gitem, event):
        pass