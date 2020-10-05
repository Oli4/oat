import qimage2ndarray
import sys
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QFileDialog,
                             QMainWindow, QWidget)

from oat.io import OCT
from oat.models import *
from oat.models.db import orm
from oat.models.layers import OctLayer, NirLayer, LineLayer3D, CfpLayer
# from oat.views import main_window, toolbox
from oat.views.dialogs.login import LoginDialog
from oat.views.toolbox import TreeItemDelegate, ModalityEntry, \
    SegmentationEntry, Toolbox


class RegistrationManual(QWidget, Ui_RegistrationManual):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.model: QtGui.QStandardItemModel = model
        # self.model.dataChanged.connect(self.refresh)

        self._root_index = QtCore.QModelIndex()
        print("test")


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
        self.data_2D_index = QtCore.QPersistentModelIndex(
            self.data_model.index(0, 0, parent=QtCore.QModelIndex()))
        self.data_3D_index = QtCore.QPersistentModelIndex(
            self.data_model.index(1, 0, parent=QtCore.QModelIndex()))

        # This is used to keep track which layers are registed with each other
        # If A registered to B and B registered to C than we also have a registration between A and C
        # self.registered_layers = DisjointSetForest()

        self.subwindows = {}
        self.subwindows['viewer2d'] = self.mdiArea.addSubWindow(
            Viewer2D(self.data_model, self))
        self.subwindows['viewer2d'].widget().setRootIndex(
            QtCore.QModelIndex(self.data_2D_index))
        self.subwindows['viewer3d'] = self.mdiArea.addSubWindow(
            Viewer3D(self.data_model, self))
        self.subwindows['viewer3d'].widget().setRootIndex(
            QtCore.QModelIndex(self.data_3D_index))
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

        self.actionToggle2D.triggered.connect(
            lambda: self.toggle_subwindow('viewer2d'))
        self.actionToggle3D.triggered.connect(
            lambda: self.toggle_subwindow('viewer3d'))
        self.actionToogleToolbox.triggered.connect(
            lambda: self.toggle_subwindow('toolbox'))

    def new_layer_id_2d(self):
        self._id_2d += 1
        return "2D_{}".format(self._id_2d - 1)

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

    def import_vol(self, filename=None):
        """ Imports HE OCT raw file (.vol ending)

        """
        if not filename:
            fname, _ = QFileDialog.getOpenFileName(self,
                                                   "Import Heidelberg Engineering OCT raw files (.vol ending)",
                                                   self.import_path,
                                                   "HE OCT raw files (*.vol)")
            print(fname)
        else:
            fname = filename

        if fname:
            self.import_path = os.path.dirname(fname)

            oct_data = OCT.read_vol(fname)

            # Add OCT
            oct_layer = OctLayer(oct_data.volume, oct_data.meta,
                                 oct_data.bscan_meta)

            # Store references to the Layers in data_model
            oct_TreeItem = ModalityTreeItem(oct_layer)

            for key in oct_data.layers:
                seg_layer = LineLayer3D(oct_data.layers[key], name=key)
                seg_TreeItem = SegmentationTreeItem(seg_layer)
                oct_TreeItem.appendRow(seg_TreeItem)
            self.data_model.itemFromIndex(
                QtCore.QModelIndex(self.data_3D_index)).appendRow(oct_TreeItem)

            # Add NIR
            nir_layer = NirLayer(oct_data.nir)
            nir_TreeItem = ModalityTreeItem(nir_layer)
            self.data_model.itemFromIndex(
                QtCore.QModelIndex(self.data_2D_index)).appendRow(nir_TreeItem)

            # Add 2D Slices Overlay
            overlay = OctOverlay(self.data_model,
                                 self.data_model.indexFromItem(oct_TreeItem))
            self.subwindows['viewer2d'].widget().add_overlay(overlay)

            self.update_viewer2d()
            self.update_viewer3d()
            self.statusbar.showMessage(self.import_path)

    def import_cfp(self, filename=None):
        """ Imports CFP

        :return:
        """
        if not filename:
            fname, _ = QFileDialog.getOpenFileName(self,
                                                   "Import Color Fundus Photography",
                                                   self.import_path,
                                                   "CFP files (*.bmp *.BMP *.tif *.TIF *.tiff *.TIFF)")
            print(fname)
        else:
            fname = filename
        if fname:
            self.import_path = os.path.dirname(fname)

            cfp_layer = CfpLayer.import_cfp(fname)

            cfp_TreeItem = ModalityTreeItem(cfp_layer)
            self.data_model.itemFromIndex(
                QtCore.QModelIndex(self.data_2D_index)).appendRow(cfp_TreeItem)

            self.statusbar.showMessage(self.import_path)

    def create_registration_view(self):
        self.subwindows['registration'] = self.mdiArea.addSubWindow(
            RegistrationManual(self.data_model, self))
        # self.subwindow_visibility['registration'] = True
        # self.toggle_subwindow('registration')
        self.subwindows['registration'].show()

    def update_toolbox_layer_entries(self):
        self.subwindows['toolbox'].widget().update_layer_entries(self.layers_2d,
                                                                 self.layers_3d)

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

    # def reset_viewer(self):
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
        self.spinBox.setRange(0, n_slices - 1)

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
            if (
            QtCore.QPersistentModelIndex(index), 0) not in self._pixmaps.keys():
                self.graphicsView3D._empty = False
                data = self.model.data(index, DATA_ROLE)
                for i in range(data.shape[-1]):
                    q_img = qimage2ndarray.array2qimage(data[..., i])
                    gp_item = QtWidgets.QGraphicsPixmapItem(
                        QtGui.QPixmap().fromImage(q_img))
                    self._pixmaps[
                        QtCore.QPersistentModelIndex(index), i] = gp_item
                    gp_item.hide()
                    self.graphicsView3D.scene.addItem(gp_item)

                self.active_modality = QtCore.QPersistentModelIndex(index)

            # Set last active slice hidden
            self._pixmaps[QtCore.QPersistentModelIndex(
                index), self._last_active_slice].hide()

            # Set modality visibility
            if self.model.data(index, VISIBILITY_ROLE):
                self._pixmaps[QtCore.QPersistentModelIndex(
                    index), self.active_slice].show()
            else:
                self._pixmaps[QtCore.QPersistentModelIndex(
                    index), self.active_slice].hide()


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


class Overlay(QtWidgets.QGraphicsItemGroup):
    def __init__(self, name, model, index):
        super().__init__()
        self.name = name
        self.model = model
        self.index = index


class OctOverlay(Overlay):
    def __init__(self, model, index):
        super().__init__(model=model, index=index, name="OCT")
        self.setZValue(5)

    def create_overlay(self):
        # Get Bscan Positions
        slice_positions = self.model.data(self.index, role=SLICEPOSITIONS_ROLE)
        x_scaling = self.model.data(self.index, role=XSCALING_ROLE)
        y_scaling = self.model.data(self.index, role=YSCALING_ROLE)
        active_slice = self.model.data(self.index, role=ACTIVESLICE_ROLE)

        # Add line for every Bscan position
        for slice_pos in slice_positions:
            start = QtCore.QPointF(slice_pos[0][0] * x_scaling,
                                   slice_pos[0][1] * y_scaling)
            end = QtCore.QPointF(slice_pos[1][0] * x_scaling,
                                 slice_pos[1][1] * y_scaling)
            line_item = QtWidgets.QGraphicsLineItem(QtCore.QLineF(start, end))
            line_item.setPen(QtGui.QPen().setColor("lawngreen"))
            self.addToGroup(line_item)


class TreeItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self._visible = None

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionViewItem',
              index: QtCore.QModelIndex) -> None:
        if isinstance(self.parent(), QtWidgets.QAbstractItemView) or \
                isinstance(self.parent(), ModalityTreeItem):
            self.parent().openPersistentEditor(index)
        super().paint(painter, option, index)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem',
                     index: QtCore.QModelIndex) -> QWidget:
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
        editor.label.setText(index.model().data(index, Qt.UserRole + 2))

        icon = QtGui.QIcon()
        if index.model().data(index, Qt.UserRole + 1):
            icon.addPixmap(
                QtGui.QPixmap(":/icons/icons/baseline-visibility-24px.svg"),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off)
            editor.hideButton.setIcon(icon)
            self._visible = True
        else:
            icon.addPixmap(
                QtGui.QPixmap(":/icons/icons/baseline-visibility_off-24px.svg"),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off)
            editor.hideButton.setIcon(icon)
            self._visible = False

    def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel,
                     index: QtCore.QModelIndex) -> None:
        model.setData(index, self._visible, Qt.UserRole + 1)

    def sizeHint(self, option: 'QStyleOptionViewItem',
                 index: QtCore.QModelIndex) -> QtCore.QSize:
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
        self.ModalityTreeView_2d.setItemDelegate(
            TreeItemDelegate(self.ModalityTreeView_2d))
        self.ModalityTreeView_2d.setHeaderHidden(True)
        self.ModalityTreeView_2d.setRootIndex(
            QtCore.QModelIndex(parent.data_2D_index))
        self.ModalityTreeView_2d.setUniformRowHeights(False)

        self.ModalityTreeView_3d.setModel(parent.data_model)
        self.ModalityTreeView_3d.setItemDelegate(
            TreeItemDelegate(self.ModalityTreeView_3d))
        self.ModalityTreeView_3d.setHeaderHidden(True)
        self.ModalityTreeView_3d.setRootIndex(
            QtCore.QModelIndex(parent.data_3D_index))
        self.ModalityTreeView_3d.setUniformRowHeights(False)

        # self.addButton_2d.clicked.connect(self.create_layer_2d)
        # self.addButton_3d.clicked.connect(self.create_layer_3d)

        self.registerButton_2d.clicked.connect(
            self.main_window.create_registration_view)

    def closeEvent(self, evnt):
        evnt.ignore()
        self.setWindowState(QtCore.Qt.WindowMinimized)


class LayerTreeView(QtWidgets.QTreeView):
    def __init__(self, model, parent):
        super().__init__(parent)
        self.setModel(model)
        model.setView(self)
        root = model.index(0, 0)
        self.setCurrentIndex(root)
        self.setHeaderHidden(True)


import hashlib, binascii, os
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class LoginDialog(QtWidgets.QDialog, Ui_LoginDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        _translate = QtCore.QCoreApplication.translate

        self.db_dict = {"Local SQLite": "/home/morelle/DBs/test.db",
                        "UKB Patients": "path"}

        self.setupUi(self)

        for i, key in enumerate(self.db_dict.keys()):
            self.dbDropdown.addItem(key)

        self.buttonBox.accepted.connect(self.handleLogin)
        self.buttonBox.rejected.connect(self.close)

    def handleLogin(self):
        # query selected DB for user:
        db_key = self.dbDropdown.currentText()

        if db_key == "Add new DB":
            return
            # self.create_new_db()
        else:
            engine = create_engine("sqlite:///" + self.db_dict[db_key])
            Session = sessionmaker(bind=engine)
            session = Session()
            query = session.query(orm.User).filter(
                orm.User.username == self.username.text())

            try:
                stored_hash = query.one().password_hash
                # Compare hash of password field to password_hash in DB
                if self.verify_password(stored_hash, self.password.text()):
                    self.accept()
                else:
                    QtWidgets.QMessageBox.warning(self, 'Error',
                                                  'Wrong password')
            except NoResultFound:
                QtWidgets.QMessageBox.warning(self, 'Error',
                                              'Username not found')

    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                      salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password


class DataTableView(QWidget, Ui_DataTableView):
    def __init__(self, model, parent=None):
        """Initialize the components of the Toolbox subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.PatientView.setModel(model)


def main():
    application = QApplication(sys.argv)
    login = LoginDialog()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = oat()
        desktop = QDesktopWidget().availableGeometry()
        width = (desktop.width() - window.width()) / 2
        height = (desktop.height() - window.height()) / 2
        window.show()
        window.move(width, height)

        debug = False

        if debug:
            window.import_vol("/run/user/1000/doc/5575ed92/67007_20190515.vol")
            window.import_cfp("/run/user/1000/doc/b1a09644/HS00+0EZ.003.BMP")

        sys.exit(application.exec_())


if __name__ == '__main__':
    main()
