from PyQt5 import QtCore, QtGui

class TreeItem(QtGui.QStandardItem):
    def __init__(self, *args, **kwargs):
        super().__init__()

        #self._parent = parent
        #self._child_items = []
        #self._item_data = data

    def column_count(self):
        # We have only a single column currently because I plan to store the complete modality/segmentation in column 1
        return 1

    """
    def add_child(self, treeitem):
        self._child_items.append(treeitem)

    def child_count(self):
        return len(self._child_items)

    def column_count(self):
        # We have only a single column currently because I plan to store the complete modality/segmentation in column 1
        return len(self._item_data)

    def row(self):
        pass

    def parent(self):
        return self._parent

    def child(self, number):
        if number < 0 or number >= self.child_count():
            return None
        return self._child_items[number]

    def child_number(self):
        # Return index of this item in parents list of childs
        if self._parent:
            self.parent()._childItems.index(self)

        # Return 0 for the root and other elements without a parent
        return 0

    def data(self, column):
        if column < 0 or column >= self.column_count():
            return False

        return self._item_data[column]

    def set_item_data(self, column, data):
        if column < 0 or column >= self.column_count():
            return False

        self._item_data[column] = data
        return True

    def insert_children(self, position, count):
        if position < 0 or position > self.child_count():
            return False

        for _ in range(0, count-1):
            data = []
            new_item = TreeItem(data, self)
            self._child_items.insert(position, new_item)

    def remove_children(self, position, count):
        if position < 0 or position > self.child_count():
            return False

        for _ in range(0, count-1):
            del self._child_items[position]

        return True
    
    """


class ModalityTreeItem(TreeItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SegmentationTreeItem(TreeItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class DataModel(QtGui.QStandardItemModel):
    def __init__(self):
        super().__init__()


        root_data = []
        self.root_item = TreeItem(root_data)


    def get_item(self, qm_index):
        if qm_index.isValid():
            item = qm_index.internalPointer()
            if item:
                return item

        return self.root_item

    def flags(self, qm_index):
        if not qm_index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, QModelIndex, role=None):
        pass

    def setData(self, QModelIndex, Any, role=None):
        print("whyhere")
        pass

    def headerData(self, p_int, Qt_Orientation, role=None):
        pass

    def setHeaderData(self, p_int, Qt_Orientation, Any, role=None):
        pass

    def columnCount(self, parent=None, *args, **kwargs):
        return self.root_item.column_count()

    def rowCount(self, parent=None, *args, **kwargs):
        parent_item = self.get_item(parent)
        return parent_item.rowCount()

    def beginInsertRows(self, QModelIndex, p_int, p_int_1):
        pass

    def removeRows(self, p_int, p_int_1, parent=None, *args, **kwargs):
        pass

    def index(self, row, column, parent=QtCore.QModelIndex(), *args, **kwargs):
        if parent.isValid() and parent.column() != 0:
            return QtCore.QModelIndex()

        parent_item = self.get_item(parent)
        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()


    def parent(self, qm_index=None):
        if not qm_index.isValid():
            return QtCore.QModelIndex()

        child_item = self.get_item(qm_index)
        parent_item = child_item.parent()

        if parent_item == self.root_item:
            return QtCore.QModelIndex()

        return self.createIndex(parent_item.childNumber(), 0, parent_item)