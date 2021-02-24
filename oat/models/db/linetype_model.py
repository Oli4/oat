import typing

import requests
from PyQt5 import Qt, QtWidgets, QtCore

from oat import config
from oat.models.config import DATA_ROLE


class LineTypeModel(Qt.QAbstractTableModel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._data = self.get_line_types()
        self.columns = ["name", "description", "default_color", "public", "id"]

    def get_line_types(self):
        r = requests.get("{}/linetypes/public".format(config.api_server),
                         headers=config.auth_header)
        if r.status_code != 200:
            QtWidgets.QMessageBox.warning(
                self, 'Error while retrieving annotation line types',
                r.json()["detail"])

        return r.json()

    def columnCount(self, parent=QtCore.QModelIndex()) -> int:
        return len(self.columns)

    def rowCount(self, parent=QtCore.QModelIndex()) -> int:
        return len(self._data)

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self.columns[section])

            if orientation == QtCore.Qt.Vertical:
                return str(self._data[section]["id"])

    def flags(self, index: QtCore.QModelIndex()):
        flags = super(self.__class__, self).flags(index)
        # flags |= QtCore.Qt.ItemIsEditable
        # flags |= QtCore.Qt.ItemIsSelectable
        flags |= QtCore.Qt.ItemIsEnabled
        # flags |= QtCore.Qt.ItemIsDragEnabled
        # flags |= QtCore.Qt.ItemIsDropEnabled
        return flags

    def data(self, index: QtCore.QModelIndex, role: int) -> typing.Any:
        if role == QtCore.Qt.DisplayRole:
            return str(self._data[index.row()]["name"])
        if role == DATA_ROLE:
            return self._data[index.row()]
