from PyQt5 import QtGui, QtWidgets, QtCore

class Pen(object):
    def __init__(self):

        self.cursor = self.get_cursor()
        self.button = self.get_tool_button()
        self.hot_key = None
        self.settings_widget = None

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

    @staticmethod
    def mouse_move_handler(view, event):
        layer = view.scene().focusItem()
        if layer:
            if view._mouse_left_pressed:
                layer.add_pixel(view.mapToScene(event.pos()).toPoint())
            elif view._mouse_right_pressed:
                layer.remove_pixel(view.mapToScene(event.pos()).toPoint())

    @staticmethod
    def mouse_press_handler(view, event):
        scene_pos = view.mapToScene(event.pos())
        layer = view.scene().focusItem()
        if event.button() == QtCore.Qt.LeftButton:
            view._mouse_left_pressed = True
            if layer:
                layer.add_pixel(scene_pos.toPoint())
        if event.button() == QtCore.Qt.RightButton:
            view._mouse_right_pressed = True
            if layer:
                layer.remove_pixel(scene_pos.toPoint())

    @staticmethod
    def mouse_release_handler(view, event):
        pass