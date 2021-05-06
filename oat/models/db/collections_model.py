import pandas as pd
import requests
from PySide6 import QtCore

from oat import config
from oat.models.config import DATA_ROLE, ID_ROLE, EMPTY_ROLE


class CollectionsModel(QtCore.QAbstractTableModel):
    def __init__(self, dataset_id=None):
        super().__init__()

        self.column_order = ["dropdown_text", "name", "patient_id",
                             "patient_pseudonym", "registered",
                             "created_by", "created_at", "enfaceimage_ids",
                             "volumeimage_ids", "laterality", "id",]
        self._dataset_id = dataset_id
        self._data = None
        self.reload_data()

    @property
    def dataset_id(self):
        return self._dataset_id

    @dataset_id.setter
    def dataset_id(self, value):
        self._dataset_id = value
        self.reload_data()

    def reload_data(self):
        self.layoutAboutToBeChanged.emit()
        if type(self.dataset_id) == int:
            response = requests.get(
                f"{config.api_server}/datasets/{self.dataset_id}",
                headers=config.auth_header)
            collections = response.json()["collections"]
        else:
            response = requests.get(
                f"{config.api_server}/collections/me",
                headers=config.auth_header)
            collections = response.json()

        clean_collections = []
        for c in collections:
            print(c)
            patient = c.pop("patient")
            c["patient_id"] = patient["id"]
            c["patient_pseudonym"] = patient["pseudonym"]
            clean_collections.append(c)

        if len(clean_collections) > 0:
            self._data = pd.DataFrame.from_records(clean_collections)
        else:
            self._data = pd.DataFrame(columns=self.column_order)
        self._data["dropdown_text"] = self._data["name"] + " (" + self._data["laterality"] + ")"
        self._data["created_at"] = pd.to_datetime(self._data["created_at"])

        self._data = self._data[self.column_order]

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
                return {"enfaceimage_ids": row["enfaceimage_ids"],
                        "volumeimage_ids": row["volumeimage_ids"]}
            else:
                return {"enfaceimage_ids": [],
                        "volumeimage_ids": []}

        elif role == ID_ROLE:
            if len(self._data) > 0:
                if index.row() == -1 or pd.isna(self._data.iloc[index.row()].name):
                    return None
                else:
                    return int(self._data.iloc[index.row()].name)

        elif role == EMPTY_ROLE:
            if len(self._data) > 0:
                row = self._data.iloc[index.row(), :]
                if len(row["enfaceimage_ids"]) + len(row["volumeimage_ids"]) == 0:
                    return True
                else:
                    return False


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
