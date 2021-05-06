import typing
import pandas as pd
import requests
from PySide6 import QtCore

from oat import config
from oat.models.config import ID_ROLE, DATA_ROLE


class DatasetsModel(QtCore.QAbstractTableModel):
    def __init__(self, owned_only=False):
        super().__init__()

        self._data = None
        self.owned_only = owned_only
        self.reload_data()


    def reload_data(self):
        self.layoutAboutToBeChanged.emit()
        if self.owned_only:
            response = requests.get(
                f"{config.api_server}/datasets/me",
                headers=config.auth_header)
            data = response.json()
        else:
            response = requests.get(
                f"{config.api_server}/datasets/",
                headers=config.auth_header)
            no_dataset = [{"id": None, "name": 'All Collections', "info":''}]
            data = no_dataset + response.json()

        self._data = pd.DataFrame.from_records(data)
        if len(self._data) == 0:
            self._data = pd.DataFrame(columns=["id", "name", "info",
                                               "created_by", "collection_ids",
                                               "collaborator_ids"])

        self._data.set_index("id", inplace=True)
        self.layoutChanged.emit()

    @property
    def columns(self):
        return list(self._data.columns.values)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data.iloc[index.row(), index.column()]
        elif role == ID_ROLE:
            if index.row() == -1 or pd.isna(self.data.iloc[index.row()].name):
                return None
            else:
                return int(self._data.iloc[index.row()].name)
        elif role == DATA_ROLE:
            if index.row() == -1 or pd.isna(self._data.iloc[index.row()].name):
                return None
            else:
                d = self._data.iloc[index.row()].to_dict()
                d["id"] = int(self._data.iloc[index.row()].name)
                return d

    def setData(self, index: QtCore.QModelIndex, value: typing.Any,
                role: int = ...) -> bool:
        for keys in value:
            self._data.iloc[index.row(), self.columns.index(keys)] = value[keys]

    def create(self, data):
        response = requests.post(
            f"{config.api_server}/datasets/",
            headers=config.auth_header,
            json=data)
        self.reload_data()

    def delete(self, id):
        response = requests.delete(
            f"{config.api_server}/datasets/{id}",
            headers=config.auth_header)
        self.reload_data()

    def rowCount(self, index):
        # The length of the outer list.
        return self._data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                data = self._data.columns[section]
                header = " ".join([p.capitalize() for p in data.split("_")])
                return header

            if orientation == QtCore.Qt.Vertical:
                return str(self._data.index[section])

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        # flags |= QtCore.Qt.ItemIsEditable
        # flags |= QtCore.Qt.ItemIsSelectable
        flags |= QtCore.Qt.ItemIsEnabled
        # flags |= QtCore.Qt.ItemIsDragEnabled
        # flags |= QtCore.Qt.ItemIsDropEnabled
        return flags

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        try:
            self.layoutAboutToBeChanged.emit()
            self._data = self._data.sort_values(self._data.columns[Ncol],
                                              ascending=not order)
            self.layoutChanged.emit()
        except Exception as e:
            print(e)
