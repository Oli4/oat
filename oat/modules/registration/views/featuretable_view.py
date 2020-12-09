from PyQt5 import QtWidgets

from oat.models.config import DELETE_ROLE


class FeatureTableView(QtWidgets.QTableView):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)

    def delete_current_cell(self):
        index = self.currentIndex()
        self.model().setData(index, None, role=DELETE_ROLE)

    def delete_current_row(self):
        index = self.currentIndex()
        self.model().removeRow(index.row())

    def next(self):
        """ Select next item """
        index = self.currentIndex()
        if index.column() < self.model().columnCount() - 1:
            new_index = self.model().createIndex(index.row(),
                                                 index.column() + 1)
        elif index.column() == self.model().columnCount() - 1:
            # Create new row if needed
            if index.row() + 1 == self.model().rowCount():
                if self.model().match_is_empty(index.row()):
                    return False
                self.model().insertRow(self.model().rowCount())
            # Set the new index
            new_index = self.model().createIndex(index.row() + 1, 0)
        self.setCurrentIndex(new_index)

    def last(self):
        """ Select last item """
        index = self.currentIndex()
        if index.column() > 0:
            new_index = self.model().createIndex(index.row(),
                                                 index.column() - 1)
            self.setCurrentIndex(new_index)
        else:
            if not index.row() == 0:
                new_index = self.model().createIndex(
                    index.row() - 1, self.model().columnCount() - 1)
                self.setCurrentIndex(new_index)

    def up(self):
        """ Select last feature on same image """
        print("test")
        index = self.currentIndex()
        if index.row() > 0:
            new_index = self.model().createIndex(index.row() - 1,
                                                 index.column())
            self.setCurrentIndex(new_index)

    def down(self):
        """ Select next feature on same image """
        print("test down")
        index = self.currentIndex()
        if index.row() + 1 == self.model().rowCount():
            if self.model().match_is_empty(index.row()):
                return False
            self.model().insertRow(self.model().rowCount())
        new_index = self.model().createIndex(index.row() + 1, index.column())
        self.setCurrentIndex(new_index)
