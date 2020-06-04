from PyQt5.QtWidgets import QTableView


class FeatureTableView(QTableView):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def next(self):
        """ Select next item """
        index = self.currentIndex()
        if index.column() < self.model().columnCount() - 1:
            new_index = self.model().createIndex(index.row(),
                                                 index.column() + 1)
            self.setCurrentIndex(new_index)
        elif index.column() == self.model().columnCount() - 1:
            # Create new row if needed
            if index.row() + 1 == self.model().rowCount():
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
        index = self.currentIndex()
        if index.row() > 0:
            new_index = self.model().createIndex(index.row() - 1,
                                                 index.column())
            self.setCurrentIndex(new_index)

    def down(self):
        """ Select next feature on same image """
        index = self.currentIndex()
        if index.row() + 1 == self.model().rowCount():
            self.model().insertRow(self.model().rowCount())
        new_index = self.model().createIndex(index.row() + 1, index.column())
        self.setCurrentIndex(new_index)
