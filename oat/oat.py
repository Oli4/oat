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

from oat.views import Ui_MainWindow, Ui_Toolbox, Ui_LayerEntry, Ui_Viewer3D, Ui_Viewer2D
from oat.models.layers import  OctLayer, NirLayer, layer_types_2d, layer_types_3d

class oat(QMainWindow, Ui_MainWindow):
    """Create the main window that stores all of the widgets necessary for the application."""

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super().__init__(parent)
        self.setupUi(self)

        self.layers_2d = {}
        self.layers_3d = {}

        self.subwindows = {}
        self.subwindows['viewer2d'] = self.mdiArea.addSubWindow(Viewer2D(self))
        self.subwindows['viewer3d'] = self.mdiArea.addSubWindow(Viewer3D(self))
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
        self.actionOpen_Project.triggered.connect(self.open_project)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_as.triggered.connect(self.save_as)

        self.actionToggle2D.triggered.connect(lambda: self.toggle_subwindow('viewer2d'))
        self.actionToggle3D.triggered.connect(lambda: self.toggle_subwindow('viewer3d'))
        self.actionToogleToolbox.triggered.connect(lambda: self.toggle_subwindow('toolbox'))

    @property
    def id_2d(self):
        self._id_2d += 1
        return self._id_2d -1

    @property
    def id_3d(self):
        self._id_3d += 1
        return self._id_3d - 1

    def reset_layer_ids(self):
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
                                           '/home', "HE OCT raw files (*.vol)")
        if fname:
            self.import_path = os.path.dirname(fname)
            self.delete_previous()

            self.layers_2d[self.id_2d] = NirLayer.import_vol(fname)
            self.layers_3d[self.id_3d] = OctLayer.import_vol(fname)

            self.update_toolbox_layer_entries()
            self.update_viewer2d()
            self.update_viewer3d()

            self.statusbar.showMessage(self.import_path)


        ''' 
            self.oct.import_vol_from(import_path)

            npimg = self.oct.get_scan()[:, :, self.currentScanNumber - 1]
            # slo = self.oct.get_slo()
            self.mainWindowUi.show_scan(npimg, self.oct.numSlices)
            # self.mainWindowUi.show_slo(slo)

            self.activaViewerSet.add('scanViewer')

            self.mainWindowUi.set_status_bar(self.lastImportPath)
            return 0
        else:
            return 1'''

    def update_toolbox_layer_entries(self):
        self.subwindows['toolbox'].widget().update_layer_entries(self.layers_2d, self.layers_3d)

    def update_viewer2d(self):
        self.subwindows['viewer2d'].widget().display_layers()

    def update_viewer3d(self):
        self.subwindows['viewer3d'].widget().display_layers()

    def delete_previous(self):
        self.layers_2d = {}
        self.layers_3d = {}

        self.reset_layer_ids()

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

        self.main_window = parent
        self.layers_3d = parent.layers_3d

        self.setupUi(self)

    def closeEvent(self, evnt):
        evnt.ignore()
        self.setWindowState(QtCore.Qt.WindowMinimized)

    def display_layers(self):
        pass


class Viewer2D(QWidget, Ui_Viewer2D):
    def __init__(self, parent=None):
        """Initialize the components of the Viewer2D subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.main_window = parent

        self.scene = QtWidgets.QGraphicsScene(self)
        self.graphicsView2D.setScene(self.scene)
        self.pixmapitem_dict = {}
        self.layers_2d = parent.layers_2d

    def closeEvent(self, evnt):
        evnt.ignore()
        self.setWindowState(QtCore.Qt.WindowMinimized)

    def display_layers(self):
        for key in self.main_window.layers_2d:
            q_img = qimage2ndarray.array2qimage(self.main_window.layers_2d[key].data)
            self.pixmapitem_dict[key] = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap().fromImage(q_img))
            self.scene.addItem(self.pixmapitem_dict[key])
            self.set_visibility(key)

    def set_visibility(self, key):
        if self.main_window.layers_2d[key].visible:
            self.show_layer(key)
        else:
            self.hide_layer(key)

    def hide_layer(self, key):
        self.pixmapitem_dict[key].hide()

    def show_layer(self, key):
        self.pixmapitem_dict[key].show()


class Toolbox(QWidget, Ui_Toolbox):
    def __init__(self, parent=None):
        """Initialize the components of the Toolbox subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.main_window = parent

        self.layers_2d = parent.layers_2d
        self.layers_3d = parent.layers_3d

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

        if self.layer_obj.dimension = 2:
            self.main_window.update_viewer2d()
        else:
            self.main_window.update_viewer3d()

    def show_layer(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/baseline-visibility-24px.svg"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.hideButton.setIcon(icon)

        self.layer_obj.visible = True

        if self.layer_obj.dimension = 2:
            self.main_window.update_viewer2d()
        else:
            self.main_window.update_viewer3d()






def main():
    application = QApplication(sys.argv)
    window = oat()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())


