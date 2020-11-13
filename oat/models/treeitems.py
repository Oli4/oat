from PyQt5 import QtGui, Qt

from .config import role_mapping
from .custom_scene import CustomGrahpicsScene


class TreeItem(QtGui.QStandardItem):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, role=None, *args, **kwargs):
        if role in role_mapping.keys():
            return getattr(self._data, role_mapping[role])
        else:
            super().data(role, *args, **kwargs)

    def setData(self, value, role=None, *args, **kwargs):
        if role in role_mapping.keys():
            setattr(self._data, role_mapping[role], value)
            self.emitDataChanged()
        else:
            super().setData(value, role, *args, **kwargs)

    def columnCount(self):
        return 1


class ImageTreeItem(TreeItem):
    def __init__(self, data: CustomGrahpicsScene):
        super().__init__(data)

    def rowCount(self):
        return 0

    def hide(self):
        self._data.show_background()

    def show(self):
        self._data.hide_background()


class AreaAnnotationsTreeItem(TreeItem):
    def __init__(self, data: Qt.QGraphicsItemGroup):
        super().__init__(data)

    def rowCount(self):
        return len(self._data.childItems())


class LayerAnnotationsTreeItem(TreeItem):
    def __init__(self, data: Qt.QGraphicsItemGroup):
        super().__init__(data)

    def rowCount(self):
        return len(self._data.childItems())


class AnnotationTreeItem(TreeItem):
    def __init__(self, data: Qt.QGraphicsItemGroup):
        super().__init__(data)

    def rowCount(self):
        return 0


class DataModel(QtGui.QStandardItemModel):
    def __init__(self):
        super().__init__()
