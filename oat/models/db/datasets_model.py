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
        self.beginResetModel()
        if self.owned_only:
            response = requests.get(
                f"{config.api_server}/datasets/me",
                headers=config.auth_header)
            data = response.json()
        else:
            response = requests.get(
                f"{config.api_server}/datasets/",
                headers=config.auth_header)
            data = response.json()

        self._data = pd.DataFrame.from_records(data)
        if len(self._data) == 0:
            self._data = pd.DataFrame(columns=["id", "name", "info",
                                               "created_by", "collection_ids",
                                               "collaborator_ids"])
        self.endResetModel()

    @property
    def columns(self):
        return list(self._data.columns.values)



    def create(self, data):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        response = requests.post(
            f"{config.api_server}/datasets/",
            headers=config.auth_header,
            json=data)
        if response.status_code == 200:
            self._data.append(response.json(), ignore_index=True)
            self.endInsertRows()



    def update(self, id, data):
        response = requests.put(
            f"{config.api_server}/datasets/{id}",
            headers=config.auth_header,
            json=data)
    # Subclassing requires data, rowCount and columnCount methods

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data.iloc[index.row(), index.column()]
        elif role == ID_ROLE:
            if index.row() == -1 or pd.isna(self._data.iloc[index.row()].name):
                return None
            else:
                return int(self._data.iloc[index.row()]["id"])
        elif role == DATA_ROLE:
            if index.row() == -1 or pd.isna(self._data.iloc[index.row()].name):
                return None
            else:
                d = self._data.iloc[index.row()].to_dict()
                return d

    def rowCount(self, parent=QtCore.QModelIndex()):
        # The length of the outer list.
        return self._data.shape[0]

    def columnCount(self, parent=QtCore.QModelIndex()):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self._data.shape[1]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        # section is the index of the column/row.
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                data = self._data.columns[section]
                header = " ".join([p.capitalize() for p in data.split("_")])
                return header

            if orientation == QtCore.Qt.Vertical:
                return str(self._data.index[section])

    ## Make the model editable

    def setData(self, index: QtCore.QModelIndex, value: typing.Any,
                role: int = ...) -> bool:
        for keys in value:
            self._data.iloc[index.row(), index.column()] = value[keys]
        return True

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= QtCore.Qt.ItemIsEditable
        flags |= QtCore.Qt.ItemIsEnabled
        # flags |= QtCore.Qt.ItemIsSelectable
        # flags |= QtCore.Qt.ItemIsDragEnabled
        # flags |= QtCore.Qt.ItemIsDropEnabled
        return flags

    def removeRow(self, row:int, parent:QtCore.QModelIndex=...) -> bool:
        self.beginRemoveRows(parent, row, row)

        index = self.index(row, 0, parent)
        data = self.data(index, role=DATA_ROLE)
        id = data["id"]
        response = requests.delete(
            f"{config.api_server}/datasets/{id}",
            headers=config.auth_header)
        if response.status_code == 200:
            self._data.drop(index=index.row(), inplace=True)
            self._data.reset_index(inplace=True)
            success = True
            print(success)
        else:
            return False
        self.endRemoveRows()
        return True

    def removeRows(self, row:int, count:int, parent:QtCore.QModelIndex=...) -> bool:
        for i in range(row, row+count):
            success = self.removeRow(row, parent)
            if not success:
                return False
        return True
