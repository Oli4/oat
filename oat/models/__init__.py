from PyQt5 import QtGui

from .patients import PatientsModel
from .registration_model import RegistrationModel


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