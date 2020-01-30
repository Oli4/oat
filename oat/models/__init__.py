from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt

# custom data roles
VISIBILITY_ROLE = Qt.UserRole + 1
NAME_ROLE = Qt.UserRole + 2
DATA_ROLE = Qt.UserRole + 3
SHAPE_ROLE = Qt.UserRole + 4

role_mapping = {VISIBILITY_ROLE: "visible", NAME_ROLE: "name",
                DATA_ROLE: "data", None: "data", SHAPE_ROLE: "shape"}

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

class ModalityTreeItem(TreeItem):
    def __init__(self, data):
        super().__init__(data)

class SegmentationTreeItem(TreeItem):
    def __init__(self, data):
        super().__init__(data)

class DataModel(QtGui.QStandardItemModel):
    def __init__(self):
        super().__init__()