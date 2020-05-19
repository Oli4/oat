import qimage2ndarray
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QtGui

from oat.models import DATA_ROLE, VISIBILITY_ROLE, SHAPE_ROLE
from oat.views import Ui_Viewer3D


class Viewer3D(QWidget, Ui_Viewer3D):
    def __init__(self, model, parent=None):
        """Initialize the components of the Viewer3D subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.main_window = parent
        self.model: QtGui.QStandardItemModel = model
        self.model.dataChanged.connect(self.refresh)

        self.spinBox.valueChanged.connect(self.spin_box_change_action)
        self._pixmaps = {}
        self._root_index = QtCore.QModelIndex()

        # Active slices for all modalities are saved independently
        # The key of this dict is the layer_id. Starts with 3D_*
        self._active_slice = 0
        self._last_active_slice = 0

        self._active_modality = None

    #def reset_viewer(self):
    #    self._active_slice = {}
    #    self.graphicsView3D._zoom = 0
    #    self.graphicsView3D.setTransform(QtGui.QTransform())

    def setRootIndex(self, index):
        self._root_index = index

    @property
    def active_slice(self):
        return self._active_slice

    @active_slice.setter
    def active_slice(self, value):
        # Remember last acitve slice
        self._last_active_slice = self.active_slice
        self._active_slice = value
        self.main_window.update_viewer3d()

    @property
    def active_modality(self):
        return self._active_modality

    @active_modality.setter
    def active_modality(self, value):
        self._active_modality = value
        n_slices = self.model.data(QtCore.QModelIndex(value), SHAPE_ROLE)[-1]
        self.spinBox.setRange(0, n_slices-1)


    def next_slice(self):
        self.set_slice(self.spinBox.value() + 1)

    def last_slice(self):
        self.set_slice(self.spinBox.value() - 1)

    def set_slice(self, slice_n):
        self.spinBox.setValue(slice_n)

    def spin_box_change_action(self):
        self.active_slice = self.spinBox.value()

    def wheelEvent(self, event):
        if not self.graphicsView3D._empty:
            if event.angleDelta().y() > 0:
                self.next_slice()
            else:
                self.last_slice()

            event.accept()

    # Scroll through modalities with Alt+Wheel
    # def next_modality(self):
    #     pass
    #
    # def last_modality(self):
    #     pass

    def closeEvent(self, evnt):
        evnt.ignore()
        self.setWindowState(QtCore.Qt.WindowMinimized)

    def refresh(self):
        # iterate over modalities
        for row in range(self.model.rowCount(parent=self._root_index)):
            index = self.model.index(row, 0, parent=self._root_index)
            if (QtCore.QPersistentModelIndex(index),0) not in self._pixmaps.keys():
                self.graphicsView3D._empty = False
                data = self.model.data(index, DATA_ROLE)
                for i in range(data.shape[-1]):
                    q_img = qimage2ndarray.array2qimage(data[..., i])
                    gp_item = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap().fromImage(q_img))
                    self._pixmaps[QtCore.QPersistentModelIndex(index), i] = gp_item
                    gp_item.hide()
                    self.graphicsView3D.scene.addItem(gp_item)

                self.active_modality = QtCore.QPersistentModelIndex(index)

            # Set last active slice hidden
            self._pixmaps[QtCore.QPersistentModelIndex(index), self._last_active_slice].hide()

            # Set modality visibility
            if self.model.data(index, VISIBILITY_ROLE):
                self._pixmaps[QtCore.QPersistentModelIndex(index), self.active_slice].show()
            else:
                self._pixmaps[QtCore.QPersistentModelIndex(index), self.active_slice].hide()
