import qimage2ndarray
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QtGui
from PyQt5.QtWidgets import QWidget

from oat.models import DATA_ROLE, VISIBILITY_ROLE
from oat.views import Ui_Viewer2D


class Viewer2D(QWidget, Ui_Viewer2D):
    def __init__(self, model, parent=None):
        """Initialize the components of the Viewer2D subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.parent = parent
        self.model: QtGui.QStandardItemModel = model
        self.model.dataChanged.connect(self.refresh)

        # self.graphicsView2D.cursorChanged.connect(parent.)

        self._root_index = QtCore.QModelIndex()
        self._overlays = []

        self._pixmaps = {}
        self._active_modality = None

    @property
    def active_modality(self):
        return self._active_modality

    @active_modality.setter
    def active_modality(self, value):
        self._active_modality = value

    def add_overlay(self, overlay):
        self._overlays.append(overlay)

    def closeEvent(self, evnt):
        evnt.ignore()
        self.setWindowState(QtCore.Qt.WindowMinimized)

    def setRootIndex(self, index):
        self._root_index = index

    def refresh(self):
        for row in range(self.model.rowCount(parent=self._root_index)):
            index = self.model.index(row, 0, parent=self._root_index)
            if QtCore.QPersistentModelIndex(index) not in self._pixmaps.keys():
                self.graphicsView2D._empty = False
                data = self.model.data(index, DATA_ROLE)
                q_img = qimage2ndarray.array2qimage(data)
                gp_item = QtWidgets.QGraphicsPixmapItem(
                    QtGui.QPixmap().fromImage(q_img))
                gp_item.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable)
                self._pixmaps[QtCore.QPersistentModelIndex(index)] = gp_item
                self.graphicsView2D.scene.addItem(gp_item)
                self.active_modality = QtCore.QPersistentModelIndex(index)

            if self.model.data(index, VISIBILITY_ROLE):
                self._pixmaps[QtCore.QPersistentModelIndex(index)].show()
            else:
                self._pixmaps[QtCore.QPersistentModelIndex(index)].hide()

        # for overlay_key in self._overlays:
        #    if overlay_key
        #    if overlay.visible:
        #        overlay.show()
        #    else:
        #        overlay.hide()
