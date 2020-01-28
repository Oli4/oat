import sys
import os
import qimage2ndarray

import pkg_resources

#from oat.views import main_window, toolbox

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QDialog, QFileDialog,
                             QHBoxLayout, QLabel, QMainWindow, QToolBar, QVBoxLayout, QWidget, QMdiSubWindow)

from oat.views import Ui_MainWindow, Ui_Toolbox, Ui_ModalityEntry, Ui_SegmentationEntry, Ui_Viewer3D, Ui_Viewer2D
from oat.models.layers import  OctLayer, NirLayer, layer_types_2d, layer_types_3d, CfpLayer
from oat.models import DataModel, ModalityTreeItem, SegmentationTreeItem
from oat.utils import DisjointSetForest
from oat.io import OCT

class oat(QMainWindow, Ui_MainWindow):
    """Create the main window that stores all of the widgets necessary for the application."""

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super().__init__(parent)
        self.setupUi(self)

        self.data_model = DataModel()
        self.data_model = QtGui.QStandardItemModel()

        # This is used to keep track which layers are registed with each other
        # If A registered to B and B registered to C than we also have a registration between A and C
        #self.registered_layers = DisjointSetForest()

        self.subwindows = {}
        #self.subwindows['viewer2d'] = self.mdiArea.addSubWindow(Viewer2D(self))
        #self.subwindows['viewer3d'] = self.mdiArea.addSubWindow(Viewer3D(self))
        self.subwindows['toolbox'] = self.mdiArea.addSubWindow(Toolbox(self))

        self.subwindow_visibility = {}
        #self.subwindow_visibility['viewer2d'] = True
        #self.subwindow_visibility['viewer3d'] = True
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

        #self.actionToggle2D.triggered.connect(lambda: self.toggle_subwindow('viewer2d'))
        #self.actionToggle3D.triggered.connect(lambda: self.toggle_subwindow('viewer3d'))
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
            oct_layer = OctLayer(oct_data.volume)
            # Create OCT Layer with Segmentations
            #oct = OctLayer.import_vol(fname)

            # Create NIR Layer
            #nir = NirLayer.import_vol(fname)

            # Store references to the Layers in data_model
            oct_TreeItem = ModalityTreeItem()
            visibilityRole = Qt.UserRole+1
            nameRole = Qt.UserRole+2

            oct_TreeItem.setData(oct_layer.visible, visibilityRole)
            oct_TreeItem.setData(oct_layer.name, nameRole)
            #oct_TreeItem.appendRow(ModalityTreeItem().setData(oct_layer))

            #oct_TreeItem = QtGui.QStandardItem().setData(oct_layer)
            #oct_TreeItem.appendRow(QtGui.QStandardItem().setData(oct_layer))
            #[oct_TreeItem.add_child(SegmentationTreeItem(s)) for s in oct.segmentations]
            self.data_model.appendRow(oct_TreeItem)
            self.subwindows["toolbox"].widget().ModalityTreeView_3d.openPersistentEditor(self.data_model.index(0,0,self.data_model.invisibleRootItem().index()))

            #nir_TreeItem = ModalityTreeItem(nir)
            #[nir_TreeItem.add_child(SegmentationTreeItem(s)) for s in nir.segmentations]
            #self.data_model.appendRow(nir_TreeItem)

            # We assume that NIR and OCT from .vol are registered
            #self.registered_layers.make_set(nir_id)
            #self.registered_layers.make_set(oct_id)
            #self.registered_layers.union(nir_id, oct_id)

            #self.update_toolbox_layer_entries()
            #self.update_viewer2d()
            #self.update_viewer3d()

            self.statusbar.showMessage(self.import_path)

    def import_cfp(self):
        """ Imports CFP

        :return:
        """
        fname, _ = QFileDialog.getOpenFileName(self, "Import Color Fundus Photography",
                                               self.import_path, "CFP files (*.bmp *.BMP *.tif *.TIF *.tiff *.TIFF)")
        if fname:
            self.import_path = os.path.dirname(fname)

            cfp = CfpLayer.import_cfp(fname)

            cfp_TreeItem = ModalityTreeItem(cfp)
            [cfp_TreeItem.add_child(SegmentationTreeItem(s)) for s in cfp.segmentations]
            self.data_model.appendRow(cfp_TreeItem)

            # We assume that added CFP is not registered with any existing modality
            #self.registered_layers.make_set(cfp_id)

            #self.update_toolbox_layer_entries()
            #self.update_viewer2d()

            self.statusbar.showMessage(self.import_path)

    def update_toolbox_layer_entries(self):
        self.subwindows['toolbox'].widget().update_layer_entries(self.layers_2d, self.layers_3d)

    def update_viewer2d(self):
        self.subwindows['viewer2d'].widget().display_layers()

    def update_viewer3d(self):
        self.subwindows['viewer3d'].widget().display_layers()

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
    def __init__(self, parent=None):
        """Initialize the components of the Viewer3D subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.main_window = parent

        self.scene = QtWidgets.QGraphicsScene(self)
        self.graphicsView3D.setScene(self.scene)

        self.spinBox.valueChanged.connect(self.spin_box_change_action)
        self.pixmapitem_dict = {}
        self.layers_3d = parent.layers_3d

        # Active slices for all modalities are saved independently
        # The key of this dict is the layer_id. Starts with 3D_*
        self._active_slice = {}
        # The active modality refers to a layer_id of the form 3D_*
        self._active_modality = ""

    @property
    def active_modality(self):
        if self._active_modality == "":
            self.active_modality = self.main_window.layers_3d.keys().__iter__().__next__()
        return self._active_modality

    @active_modality.setter
    def active_modality(self, new_active):
        if new_active in self.main_window.layers_3d.keys():
            self._active_modality = new_active
            self.spinBox.setRange(0, self.main_window.layers_3d[self.active_modality].data.shape[-1]-1)
        else:
            raise ValueError("{} is not an available Layer.".format(new_active))

    @property
    def active_slice(self):
        if self._active_slice == {}:
            self._active_slice = {"{}".format(self.active_modality):0}
        return self._active_slice

    #def reset_viewer(self):
    #    self._active_slice = {}
    #    self.graphicsView3D._zoom = 0
    #    self.graphicsView3D.setTransform(QtGui.QTransform())

    def next_slice(self):
        self.set_slice(self._active_slice[self._active_modality] + 1)

        #if (self._active_slice[self.active_modality] + 2
        #        <= self.main_window.layers_3d[self.active_modality].data.shape[-1]):
        #    for modality in self.main_window.layers_3d.keys():
        #        if self.main_window.registered_layers.connected(modality, self.active_modality):
        #            self._active_slice[modality] += 1
        #    self.main_window.update_viewer3d()

    def last_slice(self):
        self.set_slice(self._active_slice[self._active_modality]-1)

        #if (self._active_slice[self._active_modality] >= 0):
        #    for modality in self.main_window.layers_3d.keys():
        #        if self.main_window.registered_layers.connected(modality, self.active_modality):
        #            self._active_slice[modality] -= 1
        #    self.main_window.update_viewer3d()

    def set_slice(self, slice_n):
        # Make sure slice_n is within possible range
        slice_n = max(0, slice_n)
        slice_n = min(self.main_window.layers_3d[self.active_modality].data.shape[-1]-1, slice_n)

        # Set slice for active modality and all connected/registered modalities
        for modality in self.main_window.layers_3d.keys():
            if self.main_window.registered_layers.connected(modality, self.active_modality):
                self._active_slice[modality] = slice_n

        self.main_window.update_viewer3d()

    def spin_box_change_action(self):
        self.set_slice(self.spinBox.value())

    def wheelEvent(self, event):
        if self.main_window.layers_3d:
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

    def display_layers(self):
        if self.main_window.layers_3d:
            self.graphicsView3D._empty = False

            active_component = self.main_window.registered_layers.find(self.active_modality)
            # Currently we have only 1 volume but at some point there might be multiple registered volumes
            for key in self.main_window.layers_3d:
                # Only display the modality "key" if it is registered to the current active modality
                if self.main_window.registered_layers.find(key) == active_component:
                    # Add active slice as pixmaps to the scene
                    slice = self.active_slice[self.active_modality]
                    q_img = qimage2ndarray.array2qimage(self.main_window.layers_3d[key].data[..., slice])

                    self.pixmapitem_dict[key, slice] = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap().fromImage(q_img))
                    self.scene.addItem(self.pixmapitem_dict[key, slice])
                    self.set_visibility(key)
        else:
            self.graphicsView3D._empty = True

        self.spinBox.setValue(self._active_slice[self._active_modality])

    def set_visibility(self, key):
        if self.main_window.layers_3d[key].visible:
            self.show_layer(key)
        else:
            self.hide_layer(key)

    def hide_layer(self, key):
        self.pixmapitem_dict[key, self.active_slice[self.active_modality]].setOpacity(0)

    def show_layer(self, key):
        opacity = self.main_window.layers_3d[key].opacity
        self.pixmapitem_dict[key, self.active_slice[self.active_modality]].setOpacity(opacity*0.01)


class Viewer2D(QWidget, Ui_Viewer2D):
    def __init__(self, parent=None):
        """Initialize the components of the Viewer2D subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.main_window = parent

        self.scene = QtWidgets.QGraphicsScene(self)
        self.graphicsView2D.setScene(self.scene)
        self.pixmapitem_dict = {}

        self._active_modality = ""

    def closeEvent(self, evnt):
        evnt.ignore()
        self.setWindowState(QtCore.Qt.WindowMinimized)

    def display_layers(self):
        if self.main_window.layers_2d:
            self.graphicsView2D._empty = False
            for key in self.main_window.layers_2d:
                q_img = qimage2ndarray.array2qimage(self.main_window.layers_2d[key].data)
                self.pixmapitem_dict[key] = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap().fromImage(q_img))
                self.scene.addItem(self.pixmapitem_dict[key])
                self.set_visibility(key)
        else:
            self.graphicsView2D._empty=True

    def set_visibility(self, key):
        if self.main_window.layers_2d[key].visible:
            self.show_layer(key)
        else:
            self.hide_layer(key)

    def hide_layer(self, key):
        self.pixmapitem_dict[key].hide()

    def show_layer(self, key):
        self.pixmapitem_dict[key].show()


class TreeItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self.visible = None

    def createEditor(self, parent, option, index):
        editor = ModalityEntry(parent)
        editor.hideButton.clicked.connect(self.visibilityChanged)
        return editor

    @QtCore.pyqtSlot()
    def visibilityChanged(self):
        self.visible = not self.visible
        self.commitData.emit(self.sender())

    def setEditorData(self, editor, index):
        if index.isValid():
            editor.label.setText(index.model().data(index, Qt.UserRole+2))

            icon = QtGui.QIcon()
            if index.model().data(index, Qt.UserRole+1):
                icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-visibility-24px.svg"), QtGui.QIcon.Normal,
                               QtGui.QIcon.Off)
                editor.hideButton.setIcon(icon)
                self.visible = True
            else:
                icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-visibility_off-24px.svg"), QtGui.QIcon.Normal,
                               QtGui.QIcon.Off)
                editor.hideButton.setIcon(icon)
                self.visible = False

    def setModelData(self, editor, model, index):
        print("here")
        model.setData(index, self.visible, Qt.UserRole+1)


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
        root = parent.data_model.index(0, 0)
        self.ModalityTreeView_2d.setCurrentIndex(root)
        self.ModalityTreeView_2d.setItemDelegate(TreeItemDelegate(self.ModalityTreeView_2d))
        self.ModalityTreeView_2d.setHeaderHidden(True)


        self.ModalityTreeView_3d.setModel(parent.data_model)
        root = parent.data_model.index(0, 0)
        self.ModalityTreeView_3d.setCurrentIndex(root)
        self.ModalityTreeView_3d.setItemDelegate(TreeItemDelegate(self.ModalityTreeView_3d))
        self.ModalityTreeView_3d.setHeaderHidden(True)

        self.addButton_2d.clicked.connect(self.create_layer_2d)
        self.addButton_3d.clicked.connect(self.create_layer_3d)

    def closeEvent(self, evnt):
        evnt.ignore()
        self.setWindowState(QtCore.Qt.WindowMinimized)

    def update_layer_entries(self, layers_2d, layers_3d):
        for key in layers_2d:
            self.add_layer(layers_2d[key])

        for key in layers_3d:
            self.add_layer(layers_3d[key])

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


