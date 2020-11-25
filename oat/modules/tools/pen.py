from PyQt5 import QtGui, QtWidgets, QtCore, Qt
from oat.views.ui.ui_pen_options import Ui_penOptions
import numpy as np

class PenWidget(QtWidgets.QWidget, Ui_penOptions):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.sizeSlider.valueChanged.connect(self.set_label)
        self.set_label()

    def set_label(self):
        self.sizeLabel.setText(f"Size: {self.sizeSlider.value()}")

class PaintPreview(Qt.QGraphicsEllipseItem):
    def __init__(self, settings_widget, parent=None):
        super().__init__(parent)
        self.settings_widget = settings_widget
        self.pen = self.get_pen()
        self.settings_widget.sizeSlider.valueChanged.connect(self.set_size)

    def set_size(self, size):
        self.set
        self.pen.setWidth(size)
        self.update()

    def get_pen(self):
        pen = Qt.QPen()
        pen.setWidth(self.settings_widget.sizeSlider.value())
        color = Qt.QColor()
        color.setNamedColor("#8833AA")
        brush = Qt.QBrush(color)
        brush.setStyle(QtCore.Qt.NoBrush)
        pen.setBrush(brush)
        return pen

    def paint(self, painter: QtGui.QPainter, QStyleOptionGraphicsItem, widget=None):
        painter.setPen(self.pen)
        painter.drawPoint()
        painter.drawPoints(self.pos)

class Pen(object):
    def __init__(self):
        """ """

        self.cursor = self.get_cursor()
        self.button = self.get_tool_button()
        self.hot_key = None
        self.options_widget = self.get_options_widget()
        self.paint_preview = self.get_paint_preview()
        self.paint_preview = None

        self._masks = {}



    @property
    def mask(self):
        radius = self.options_widget.sizeSlider.value()
        radius -= 1
        if radius not in self._masks:
            y, x = np.ogrid[-radius:radius + 1, -radius:radius + 1]
            self._masks[radius] = x ** 2 + y ** 2 <= radius ** 2

        return self._masks[radius]

    def get_paint_preview(self):
        return PaintPreview(self.options_widget)

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


    def mouse_move_handler(self, view: Qt.QGraphicsView, event):
        pos = view.mapToScene(event.pos())
        #view.scene().tool_preview.setPos(pos)
        layer = view.scene().focusItem()
        if layer:
            if event.buttons() & QtCore.Qt.LeftButton:
                layer.add_pixels(pos.toPoint(), self.mask)
            elif event.buttons() & QtCore.Qt.RightButton:
                layer.remove_pixel(pos.toPoint())

    def mouse_press_handler(self, view, event):
        scene_pos = view.mapToScene(event.pos())
        layer = view.scene().focusItem()
        if event.button() == QtCore.Qt.LeftButton:
            if layer:
                layer.add_pixels(scene_pos.toPoint(), self.mask)
        if event.button() == QtCore.Qt.RightButton:
            if layer:
                layer.remove_pixel(scene_pos.toPoint())

    @staticmethod
    def mouse_release_handler(view, event):
        pass

    @staticmethod
    def key_press_handler(view, event):
        pass

    @staticmethod
    def key_release_handler(view, event):
        pass