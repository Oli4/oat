import pandas as pd
import requests
from PyQt5 import QtCore

from oat import config
from oat.core.security import get_local_patient_info


class PatientsModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()

        self.data = None
        self.reload_data()

    def reload_data(self):
        response = requests.get(
            f"{config.api_server}/patients/",
            headers=config.auth_header)

        data = pd.DataFrame.from_records(response.json())
        local_data = get_local_patient_info(
            config.local_patient_info_file,
            config.fernet)

        try:
            self.data = data.merge(local_data, on="pseudonym", how="left")
        except KeyError:  # Produce empty patient model if no patients available
            self.data = pd.DataFrame(columns=["pseudonym", "id", "gender",
                                              "birthday"])

        self.data.set_index("id", inplace=True)

        self.layoutChanged.emit()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self.data.iloc[index.row(), index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return self.data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self.data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self.data.columns[section])

            if orientation == QtCore.Qt.Vertical:
                return str(self.data.index[section])

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
            self.data = self.data.sort_values(self.data.columns[Ncol],
                                              ascending=not order)
            self.layoutChanged.emit()
        except Exception as e:
            print(e)
