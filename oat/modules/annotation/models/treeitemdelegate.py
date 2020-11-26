from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget

from oat.modules.annotation.models.layereditor import LayerEntry


class TreeItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self._visible = True

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionViewItem',
              index: QtCore.QModelIndex) -> None:
        super().paint(painter, option, index)
        self.parent().openPersistentEditor(index)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem',
                     index: QtCore.QModelIndex) -> QWidget:
        self.editor = LayerEntry(parent)
        self.editor.editorChanged.connect(self.update_model)
        return self.editor

    @QtCore.pyqtSlot()
    def update_model(self):
        editor = self.sender()
        self.commitData.emit(editor)

    def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
        data = index.model().data(index, QtCore.Qt.EditRole)
        editor.label.setText(str(data["name"]))
        editor.set_color(data["current_color"].upper())
        editor.set_visible(data["visible"])

    def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel,
                     index: QtCore.QModelIndex) -> None:
        model.setData(index, editor, QtCore.Qt.EditRole)

    def sizeHint(self, option: 'QStyleOptionViewItem',
                 index: QtCore.QModelIndex) -> QtCore.QSize:
        return LayerEntry(None).sizeHint()
