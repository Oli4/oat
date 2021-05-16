import typing
import requests
from PySide6 import QtCore

from oat import config
from oat.models.config import ID_ROLE, DATA_ROLE

class BaseModel(QtCore.QAbstractTableModel):
    def __init__(self, db_endpoint):
        super().__init__()
        self.endpoint = db_endpoint

        self._data = None
        self.reload_data()

    @property
    def default_headers(self):
        """
        This abstract method should return a list of default column headers in case the table contains no data
        :rtype: list
        """
        pass

    def record_processing(self, record_in):
        """
        Reimplement this method if you want to process the data retrieved from the DB
        """
        return record_in


    @property
    def columns(self):
        return self.default_headers

    def reload_data(self):
        self.beginResetModel()
        response = requests.get(
            f"{config.api_server}/{self.endpoint}/",
            headers=config.auth_header)

        if not response.status_code == 200:
            # Todo: Show warning, set default columns for empty table
            pass
        else:
            self._data = [self.record_processing(r) for r in response.json()]
        self.endResetModel()

    # Subclassing requires data, rowCount and columnCount methods
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return str(self._data[index.row()][self.columns[index.column()]])
        elif role == ID_ROLE:
            return int(self._data[index.row()]["id"])
        elif role == DATA_ROLE:
            return self._data[index.row()]

    def rowCount(self, parent=QtCore.QModelIndex()):
        # The length of the list.
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        # All rows (dicts in the list) needs to have the same number of elements
        return len(self.columns)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        # section is the index of the column/row.
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                data = self.columns[section]
                header = " ".join([p.capitalize() for p in data.split("_")])
                return header

            if orientation == QtCore.Qt.Vertical:
                return str(self._data[section]["id"])

    ## Make the model editable
    def insertRow(self, row:int, parent:QtCore.QModelIndex=...) -> bool:
        return self.insertRows(row, 1, parent)

    def insertRows(self, row:int, count:int, parent:QtCore.QModelIndex=...) -> bool:
        self.beginInsertRows(QtCore.QModelIndex(), row, row+count-1)
        for _ in range(count):
            self._data.insert(row, {k: "" for k in self.columns})
        self.endInsertRows()
        return True

    def removeRow(self, row:int, parent:QtCore.QModelIndex=...) -> bool:
        return self.removeRows(row, 1, parent)

    def removeRows(self, row:int, count:int, parent:QtCore.QModelIndex=...) -> bool:
        if count > 1:
            raise ValueError("This function is currently not safe for more than one row")
        self.beginRemoveRows(parent, row, row+count-1)
        success = True
        for i in range(row, row + count):
            id = self._data[i]["id"]
            response = requests.delete(
                f"{config.api_server}/{self.endpoint}/{id}",
                headers=config.auth_header)
            if response.status_code == 200:
                self._data.pop(i)
            else:
                success = False
        self.endRemoveRows()
        return success

    def setData(self, index: QtCore.QModelIndex, value: typing.Any,
                role: int = ...) -> bool:

        # if index > n_rows: create new row and insert data here.
        if index.row() == -1:
            response = requests.post(
                f"{config.api_server}/{self.endpoint}/",
                headers=config.auth_header,
                json=value)
            if response.status_code == 200:
                self.insertRows(self.rowCount(), 1)
                self._data[-1] = self.record_processing(response.json())
            else:
                return False

        # Otherwise update an existing row
        else:
            response = requests.put(
                f"{config.api_server}/{self.endpoint}/",
                headers=config.auth_header,
                json=value)
            if response.status_code == 200:
                self._data[index.row()] = self.record_processing(response.json())
                self.dataChanged.emit(self.index(self.rowCount() - 1, 0), self.index(self.rowCount() - 1, self.columnCount()))
            else:
                return False

    def flags(self, index):
        flags = super().flags(index)
        flags |= QtCore.Qt.ItemIsEditable
        flags |= QtCore.Qt.ItemIsEnabled
        # flags |= QtCore.Qt.ItemIsSelectable
        # flags |= QtCore.Qt.ItemIsDragEnabled
        # flags |= QtCore.Qt.ItemIsDropEnabled
        return flags
