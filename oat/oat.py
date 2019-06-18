import sys
import os

import pkg_resources

#from oat.views import main_window, toolbox

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QDialog, QFileDialog,
                             QHBoxLayout, QLabel, QMainWindow, QToolBar, QVBoxLayout, QWidget, QMdiSubWindow)

from oat.views.ui_main_window import Ui_MainWindow
from oat.views.ui_toolbox import Ui_Toolbox
from oat.models.layers import  OctLayer, NirLayer

class oat(QMainWindow, Ui_MainWindow):
    """Create the main window that stores all of the widgets necessary for the application."""

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super().__init__(parent)
        self.setupUi(self)

        toolbox = Toolbox(self)
        self.mdiArea.addSubWindow(toolbox)



        self.viewer_2d = None
        self.viewer_3d = None

        self.import_path = os.path.expanduser('~')
        self.save_path = os.path.expanduser('~')

        self.layers_2d = {}
        self.layers_3d = {}
        self._id_2d = 0
        self._id_3d = 0

        self.action_vol.triggered.connect(self.import_vol)
        self.actionOpen_Project.triggered.connect(self.open_project)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_as.triggered.connect(self.save_as)


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

            self.show_2d()
            self.show_3d()
            self.show_toolbox()


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

class Toolbox(QWidget, Ui_Toolbox):
    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super().__init__(parent)
        self.setupUi(self)





def main():
    application = QApplication(sys.argv)
    window = oat()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())


