from PyQt5 import QtGui, QtWidgets, QtCore, Qt
from oat.views.ui.ui_pen_options import Ui_penOptions
import numpy as np
import cv2
import skimage
from skimage import transform

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
        self.settings_widget.sizeSlider.valueChanged.connect(self.compute_preview)
        self.compute_preview()
        #self.set_size(self.settings_widget.sizeSlider.value())

    def compute_preview(self):
        diameter = float(self.settings_widget.sizeSlider.value())
        pixmap = Qt.QPixmap(diameter, diameter)
        #pixmap.fill(Qt.QColor(f"#{'FF000000'}"))

        painter = Qt.QPainter(pixmap)
        color = Qt.QColor(f"#{'FF0000'}")
        color.setAlpha(100)
        brush = Qt.QBrush()
        brush.setStyle(QtCore.Qt.SolidPattern)
        brush.setColor(color)
        painter.setPen(color)
        painter.setBrush(brush)

        painter.drawEllipse(Qt.QRectF(3,3,diameter, diameter))
        painter.end()
        self.setPixmap(pixmap)
        self.update()

    def get_pen(self):
        color = Qt.QColor()
        color.setNamedColor("#FFEE00")
        brush = Qt.QBrush()
        brush.setColor(color)
        brush.setStyle(QtCore.Qt.SolidPattern)

        pen = Qt.QPen()
        pen.setWidth(0)
        pen.setBrush(brush)
        pen.setStyle(QtCore.Qt.DashLine)
        return pen


class Pen(object):
    def __init__(self):
        """ """
        self._masks = {}
        self.cursor = self.get_cursor()
        self.button = self.get_tool_button()
        self.hot_key = None
        self.options_widget = self.get_options_widget()
        self.paint_preview = self.get_paint_preview()

    @property
    def mask(self):
        radius = self.options_widget.sizeSlider.value()
        radius -= 1
        if radius not in self._masks:
            y, x = np.ogrid[-radius:radius + 1, -radius:radius + 1]
            self._masks[radius] = x ** 2 + y ** 2 <= radius ** 2

        return self._masks[radius]

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
        painter.setCompositionMode(Qt.QPainter.CompositionMode_Source)
        painter.drawEllipse(pos, radius, radius)
        painter.end()

        gitem.update_pixmap()
        gitem.changed = True

    def erase(self, gitem, pos):
        radius = self.options_widget.sizeSlider.value() / 2
        painter = self.get_painter(gitem)
        painter.setCompositionMode(Qt.QPainter.CompositionMode_Clear)
        painter.drawEllipse(pos, radius, radius)
        painter.end()

        gitem.update_pixmap()
        gitem.changed = True

    def mouse_move_handler(self, gitem: "TreeGraphicsItem", event):
        pos = gitem.mapToScene(event.pos()).toPoint()
        pos = Qt.QPointF(pos.x() + 0.5, pos.y() + 0.5)
        if event.buttons() & QtCore.Qt.LeftButton:
            self.draw(gitem, pos)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.erase(gitem, pos)

    def mouse_press_handler(self, gitem, event):
        pos = gitem.mapToScene(event.pos()).toPoint()
        pos = Qt.QPointF(pos.x() + 0.5, pos.y() + 0.5)
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