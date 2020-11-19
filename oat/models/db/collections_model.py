import pandas as pd
import requests
from PyQt5 import QtCore

from oat import config
from oat.models.config import DATA_ROLE


class CollectionsModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()

        self._data = None
        self.reload_data()

    def reload_data(self):
        self.layoutAboutToBeChanged.emit()
        response = requests.get(
            f"{config.api_server}/collections/me",
            headers=config.auth_header)

        self._data = pd.DataFrame.from_records(response.json())

        if len(self._data) == 0:  # Produce empty collection model if no patients available
            self._data = pd.DataFrame(columns=["name", "id", "patient_id", "registered",
                                               "created_by", "enfaceimages", "volumeimages"])

        self._data.set_index("id", inplace=True)

        self.layoutChanged.emit()
        # self.dataChanged.emit(self.index(0,0), self.index(*self._data.shape))

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return str(self._data.iloc[index.row(), index.column()])
        elif role == DATA_ROLE:
            if len(self._data) > 0:
                row = self._data.iloc[index.row(), :]
                return {"enfaceimages": row["enfaceimages"],
                        "volumeimages": row["volumeimages"]}
            else:
                return {"enfaceimages": [],
                        "volumeimages": []}

    def indexByName(self, name):
        return self._data.columns.get_loc(name)

    def rowCount(self, index):
        # The length of the outer list.
        return self._data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self._data.shape[1]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        # section is the index of the column/row.
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self._data.columns[section])

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
