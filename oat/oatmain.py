import sys
import os
import qimage2ndarray
import numpy as np


import pkg_resources

#from oat.views import main_window, toolbox

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QDialog, QFileDialog,
                             QHBoxLayout, QLabel, QMainWindow, QToolBar, QVBoxLayout, QWidget, QMdiSubWindow)

from oat.views import Ui_MainWindow, Ui_Toolbox, Ui_ModalityEntry, Ui_SegmentationEntry, Ui_Viewer3D, Ui_Viewer2D
from oat.models.layers import OctLayer, NirLayer, LineLayer3D, layer_types_2d, layer_types_3d, CfpLayer
from oat.models import DataModel, ModalityTreeItem, SegmentationTreeItem, VISIBILITY_ROLE, DATA_ROLE, NAME_ROLE, SHAPE_ROLE
from oat.utils import DisjointSetForest
from oat.io import OCT


class oat(QMainWindow, Ui_MainWindow):
    """Create the main window that stores all of the widgets necessary for the application."""

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super().__init__(parent)
        self.setupUi(self)

        self.data_model = DataModel()
        # Add subtrees for 2D and 3D data
        self.data_model.appendRow(QtGui.QStandardItem())
        self.data_model.appendRow(QtGui.QStandardItem())
        self.data_2D_index = QtCore.QPersistentModelIndex(self.data_model.index(0, 0, parent=QtCore.QModelIndex()))
        self.data_3D_index = QtCore.QPersistentModelIndex(self.data_model.index(1, 0, parent=QtCore.QModelIndex()))


        # This is used to keep track which layers are registed with each other
        # If A registered to B and B registered to C than we also have a registration between A and C
        #self.registered_layers = DisjointSetForest()

        self.subwindows = {}
        self.subwindows['viewer2d'] = self.mdiArea.addSubWindow(Viewer2D(self.data_model, self))
        self.subwindows['viewer2d'].widget().setRootIndex(QtCore.QModelIndex(self.data_2D_index))
        self.subwindows['viewer3d'] = self.mdiArea.addSubWindow(Viewer3D(self.data_model, self))
        self.subwindows['viewer3d'].widget().setRootIndex(QtCore.QModelIndex(self.data_3D_index))
        self.subwindows['toolbox'] = self.mdiArea.addSubWindow(Toolbox(self))

        self.subwindow_visibility = {}
        self.subwindow_visibility['viewer2d'] = True
        self.subwindow_visibility['viewer3d'] = True
        self.subwindow_visibility['toolbox'] = True

        self.import_path = os.path.expanduser('~')
        self.save_path = os.path.expanduser('~')

        self._id_2d = 0
        self._id_3d = 0

        self.action_vol.triggered.connect(self.import_vol)
        self.action_cfp.triggered.connect(self.import_cfp)
        self.actionOpen_Project.triggered.connect(self.open_project)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_as.triggered.connect(self.save_as)

        self.actionToggle2D.triggered.connect(lambda: self.toggle_subwindow('viewer2d'))
        self.actionToggle3D.triggered.connect(lambda: self.toggle_subwindow('viewer3d'))
        self.actionToogleToolbox.triggered.connect(lambda: self.toggle_subwindow('toolbox'))


    def new_layer_id_2d(self):
        self._id_2d += 1
        return "2D_{}".format(self._id_2d -1)

    def new_layer_id_3d(self):
        self._id_3d += 1
        return "3D_{}".format(self._id_3d - 1)

    def _reset_layer_ids(self):
        self._id_2d = 0
        self._id_3d = 0

    def toggle_subwindow(self, name):
        if self.subwindow_visibility[name]:
            self.hide_subwindow(name)
            self.subwindow_visibility[name] = False
        else:
            self.show_subwindow(name)
            self.subwindow_visibility[name] = True

    def show_subwindow(self, name):
        self.subwindows[name].show()

    def hide_subwindow(self, name):
        self.subwindows[name].hide()

    def close_subwindow(self, name):
        self.subwindows[name].close()


    def import_vol(self):
        """ Imports HE OCT raw file (.vol ending)

        """
        fname, _ = QFileDialog.getOpenFileName(self, "Import Heidelberg Engineering OCT raw files (.vol ending)",
                                           self.import_path, "HE OCT raw files (*.vol)")
        if fname:
            self.import_path = os.path.dirname(fname)

            oct_data = OCT.read_vol(fname)

            #Add OCT
            oct_layer = OctLayer(oct_data.volume)

            # Store references to the Layers in data_model
            oct_TreeItem = ModalityTreeItem(oct_layer)

            for key in oct_data.segmentation:
                seg_layer = LineLayer3D(oct_data.segmentation[key], name=key)
                seg_TreeItem = SegmentationTreeItem(seg_layer)
                oct_TreeItem.appendRow(seg_TreeItem)
            self.data_model.itemFromIndex(QtCore.QModelIndex(self.data_3D_index)).appendRow(oct_TreeItem)

            # Add NIR
            nir_layer = NirLayer(oct_data.nir)
            nir_TreeItem = ModalityTreeItem(nir_layer)
            self.data_model.itemFromIndex(QtCore.QModelIndex(self.data_2D_index)).appendRow(nir_TreeItem)

            self.update_viewer2d()
            self.update_viewer3d()
            self.statusbar.showMessage(self.import_path)

    def import_cfp(self):
        """ Imports CFP

        :return:
        """
        fname, _ = QFileDialog.getOpenFileName(self, "Import Color Fundus Photography",
                                               self.import_path, "CFP files (*.bmp *.BMP *.tif *.TIF *.tiff *.TIFF)")
        if fname:
            self.import_path = os.path.dirname(fname)

            cfp_layer = CfpLayer.import_cfp(fname)

            cfp_TreeItem = ModalityTreeItem(cfp_layer)
            self.data_model.itemFromIndex(QtCore.QModelIndex(self.data_2D_index)).appendRow(cfp_TreeItem)

            self.statusbar.showMessage(self.import_path)

    def update_toolbox_layer_entries(self):
        self.subwindows['toolbox'].widget().update_layer_entries(self.layers_2d, self.layers_3d)

    def update_viewer2d(self):
        self.subwindows['viewer2d'].widget().refresh()

    def update_viewer3d(self):
        self.subwindows['viewer3d'].widget().refresh()

    def delete_previous(self):
        self.layers_2d = {}
        self.layers_3d = {}

        self._reset_layer_ids()

    def open_project(self):
        pass

    def save(self):
        pass

    def save_as(self):
        pass


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

            # Se modality visibility
            if self.model.data(index, VISIBILITY_ROLE):
                self._pixmaps[QtCore.QPersistentModelIndex(index), self.active_slice].show()
            else:
                self._pixmaps[QtCore.QPersistentModelIndex(index), self.active_slice].hide()




class Viewer2D(QWidget, Ui_Viewer2D):
    def __init__(self, model, parent=None):
        """Initialize the components of the Viewer2D subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.parent = parent
        self.model: QtGui.QStandardItemModel = model
        self.model.dataChanged.connect(self.refresh)

        #self.graphicsView2D.cursorChanged.connect(parent.)

        self._root_index = QtCore.QModelIndex()

        self._pixmaps = {}
        self._active_modality = None

    @property
    def active_modality(self):
        return self._active_modality

    @active_modality.setter
    def active_modality(self, value):
        self._active_modality = value

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
                gp_item = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap().fromImage(q_img))
                gp_item.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable |
                                QtWidgets.QGraphicsItem.ItemIsFocusable)
                self._pixmaps[QtCore.QPersistentModelIndex(index)] = gp_item
                self.graphicsView2D.scene.addItem(gp_item)
                self.active_modality = QtCore.QPersistentModelIndex(index)

            if self.model.data(index, VISIBILITY_ROLE):
                self._pixmaps[QtCore.QPersistentModelIndex(index)].show()
            else:
                self._pixmaps[QtCore.QPersistentModelIndex(index)].hide()

        self.graphicsView2D.scene.setFocusItem(
            self._pixmaps[self.active_modality])



class TreeItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self._visible = None

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        if isinstance(self.parent(), QtWidgets.QAbstractItemView) or \
                isinstance(self.parent(), ModalityTreeItem):
            self.parent().openPersistentEditor(index)
        super().paint(painter, option, index)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
        if not index.model().itemFromIndex(index).parent():
            editor = ModalityEntry(parent)
        else:
            editor = SegmentationEntry(parent)

        editor.hideButton.clicked.connect(self.visibilityChanged)

        return editor

    @QtCore.pyqtSlot()
    def visibilityChanged(self):
        self._visible = not self._visible
        editor = self.sender().parent().parent()
        self.commitData.emit(editor)

    def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
        editor.label.setText(index.model().data(index, Qt.UserRole+2))

        icon = QtGui.QIcon()
        if index.model().data(index, Qt.UserRole+1):
            icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-visibility-24px.svg"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            editor.hideButton.setIcon(icon)
            self._visible = True
        else:
            icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-visibility_off-24px.svg"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            editor.hideButton.setIcon(icon)
            self._visible = False

    def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
        model.setData(index, self._visible, Qt.UserRole+1)

    def sizeHint(self, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QtCore.QSize:
        if not index.model().itemFromIndex(index).parent():
            size = ModalityEntry(None).size()
        else:
            size = SegmentationEntry(None).size()

        return size


class ModalityEntry(QWidget, Ui_ModalityEntry):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)


class SegmentationEntry(QWidget, Ui_SegmentationEntry):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

class Toolbox(QWidget, Ui_Toolbox):
    def __init__(self, parent=None):
        """Initialize the components of the Toolbox subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.main_window = parent

        # Setting up the ModalityTreeView
        self.ModalityTreeView_2d.setModel(parent.data_model)
        self.ModalityTreeView_2d.setItemDelegate(TreeItemDelegate(self.ModalityTreeView_2d))
        self.ModalityTreeView_2d.setHeaderHidden(True)
        self.ModalityTreeView_2d.setRootIndex(QtCore.QModelIndex(parent.data_2D_index))
        self.ModalityTreeView_2d.setUniformRowHeights(False)

        self.ModalityTreeView_3d.setModel(parent.data_model)
        self.ModalityTreeView_3d.setItemDelegate(TreeItemDelegate(self.ModalityTreeView_3d))
        self.ModalityTreeView_3d.setHeaderHidden(True)
        self.ModalityTreeView_3d.setRootIndex(QtCore.QModelIndex(parent.data_3D_index))
        self.ModalityTreeView_3d.setUniformRowHeights(False)


        self.addButton_2d.clicked.connect(self.create_layer_2d)
        self.addButton_3d.clicked.connect(self.create_layer_3d)

    def closeEvent(self, evnt):
        evnt.ignore()
        self.setWindowState(QtCore.Qt.WindowMinimized)

    def add_modality(self):
        pass

    def add_segmentation(self):
        pass


    def add_layer(self, layer_obj):
        new_entry = LayerEntry(self, layer_obj)
        if layer_obj.dimension == 2:
            self.ScrollAreaLayout_2d.addWidget(new_entry)
        else:
            self.ScrollAreaLayout_3d.addWidget(new_entry)

    def create_layer_2d(self):
        #layer_type, layer_name = self.new_layer_dialog(dimension=2)
        layer_type, layer_name = 'Area Layer', 'Test'
        layer_obj = layer_types_2d[layer_type](data=None, name=layer_name)
        # Add Layer to mainwindow layer list
        self.add_layer(layer_obj)

    def create_layer_3d(self):
        #layer_type, layer_name = self.new_layer_dialog(dimension=3)
        layer_type, layer_name = 'Area Layer', 'Test'
        layer_obj = layer_types_3d[layer_type](data=None, name=layer_name)
        self.add_layer(layer_obj)

    def new_layer_dialog(self, dimenson):
        # return layer_type, layer_name
        pass

class LayerTreeView(QtWidgets.QTreeView):
    def  __init__(self, model, parent):
        super().__init__(parent)
        self.setModel(model)
        model.setView(self)
        root = model.index(0, 0)
        self.setCurrentIndex(root)
        self.setHeaderHidden(True)

        #self.setIndexWidget(root, root_widget)



'''
class LayerEntry(QWidget, Ui_LayerEntry):
    def __init__(self, parent, layer_obj):
        """Initialize the components of an LayerEntry."""
        super().__init__(parent)
        self.setupUi(self)

        self.main_window = parent.main_window

        self.layer_obj = layer_obj
        self.LayerName.setText(self.layer_obj.name)
        self.set_layer_visibility(self.layer_obj.visible)

        self.hideButton.clicked.connect(self.toogle_visibility)

    def set_layer_visibility(self, visible):
        if visible:
            self.show_layer()
        else:
            self.hide_layer()

    def toogle_visibility(self):
        if self.layer_obj.visible:
            self.hide_layer()
        else:
            self.show_layer()

    def hide_layer(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-visibility_off-24px.svg"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.hideButton.setIcon(icon)
        self.layer_obj.visible = False

        if self.layer_obj.dimension == 2:
            self.main_window.update_viewer2d()
        else:
            self.main_window.update_viewer3d()

    def show_layer(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-visibility-24px.svg"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.hideButton.setIcon(icon)

        self.layer_obj.visible = True

        if self.layer_obj.dimension == 2:
            self.main_window.update_viewer2d()
        else:
            self.main_window.update_viewer3d()

'''




def main():
    application = QApplication(sys.argv)
    window = oat()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()

