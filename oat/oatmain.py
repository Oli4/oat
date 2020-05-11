import pandas as pd
import qimage2ndarray
import requests
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QFileDialog,
                             QMainWindow, QWidget)

from oat.config import *
from oat.core.security import get_fernet, get_local_patient_info
from oat.io import OCT
from oat.models import *
from oat.models.layers import OctLayer, NirLayer, LineLayer3D, CfpLayer
from oat.views import *


# from oat.views import main_window, toolbox


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

        self.import_path = os.path.expanduser('~')
        self.save_path = os.path.expanduser('~')

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
        self.subwindows["patientviewer"] = self.mdiArea \
            .addSubWindow(DataTableView(PatientsModel(), self))
        # self.subwindows['viewer2d'] = self.mdiArea.addSubWindow(Viewer2D(self.data_model, self))
        # self.subwindows['viewer2d'].widget().setRootIndex(QtCore.QModelIndex(self.data_2D_index))
        # self.subwindows['viewer3d'] = self.mdiArea.addSubWindow(Viewer3D(self.data_model, self))
        # self.subwindows['viewer3d'].widget().setRootIndex(QtCore.QModelIndex(self.data_3D_index))
        # self.subwindows['toolbox'] = self.mdiArea.addSubWindow(Toolbox(self))

        # self._id_2d = 0
        # self._id_3d = 0

        self.action_vol.triggered.connect(self.import_vol)
        self.action_cfp.triggered.connect(self.import_cfp)
        self.actionOpen_Project.triggered.connect(self.open_project)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_as.triggered.connect(self.save_as)

        # self.actionToggle2D.triggered.connect(lambda: self.toggle_subwindow('viewer2d'))
        # self.actionToggle3D.triggered.connect(lambda: self.toggle_subwindow('viewer3d'))
        #self.actionToogleToolbox.triggered.connect(lambda: self.toggle_subwindow('toolbox'))

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
        if self.subwindows[name].isVisible():
            self.subwindows[name].hide()
        else:
            self.subwindows[name].show()

    def close_subwindow(self, name):
        self.subwindows[name].close()


    def import_vol(self, filename=None):
        """ Imports HE OCT raw file (.vol ending)

        """
        if not filename:
            fname, _ = QFileDialog.getOpenFileName(self, "Import Heidelberg Engineering OCT raw files (.vol ending)",
                                               self.import_path, "HE OCT raw files (*.vol)")
            print(fname)
        else:
            fname = filename


        if fname:
            self.import_path = os.path.dirname(fname)

            oct_data = OCT.read_vol(fname)

            #Add OCT
            oct_layer = OctLayer(oct_data.volume, oct_data.meta,
                                 oct_data.bscan_meta)

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
            fname, _ = QFileDialog.getOpenFileName(self, "Import Color Fundus Photography",
                                                 self.import_path, "CFP files (*.bmp *.BMP *.tif *.TIF *.tiff *.TIFF)")
            print(fname)
        else:
            fname = filename
        if fname:
            self.import_path = os.path.dirname(fname)

            cfp_layer = CfpLayer.import_cfp(fname)

            cfp_TreeItem = ModalityTreeItem(cfp_layer)
            self.data_model.itemFromIndex(QtCore.QModelIndex(self.data_2D_index)).appendRow(cfp_TreeItem)

            self.statusbar.showMessage(self.import_path)

    def create_registration_view(self):
        self.subwindows['registration'] = self.mdiArea.addSubWindow(RegistrationManual(self.data_model, self))
        #self.subwindow_visibility['registration'] = True
        #self.toggle_subwindow('registration')
        self.subwindows['registration'].show()

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


class DataTableView(QWidget, Ui_DataTableView):
    def __init__(self, model, parent=None):
        """Initialize the components of the Toolbox subwindow."""
        super().__init__(parent)
        self.setupUi(self)
        self.model = model
        self.PatientView.setModel(model)

        self.AddButton.clicked.connect(self.add_patient)

    def add_patient(self):
        dialog = AddPatientDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.model.reload_data()


class PatientsModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()

        self.data = None
        self.reload_data()

    def reload_data(self):
        response = requests.get(
            "{}/patients/all".format(oat_config['api_server']),
            headers=oat_config["auth_header"])

        data = pd.DataFrame.from_records(response.json())
        local_data = get_local_patient_info(
            oat_config["local_patient_info_file"],
            oat_config["fernet"])

        self.data = data.merge(local_data, on="pseudonym", how="left")
        self.data.set_index("id", inplace=True)

        self.layoutChanged.emit()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self.data.iloc[index.row(), index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return self.data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self.data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.data.columns[section])

            if orientation == Qt.Vertical:
                return str(self.data.index[section])

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        # flags |= QtCore.Qt.ItemIsEditable
        # flags |= QtCore.Qt.ItemIsSelectable
        flags |= QtCore.Qt.ItemIsEnabled
        # flags |= QtCore.Qt.ItemIsDragEnabled
        # flags |= QtCore.Qt.ItemIsDropEnabled
        return flags

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        try:
            self.layoutAboutToBeChanged.emit()
            self.data = self.data.sort_values(self.data.columns[Ncol],
                                              ascending=not order)
            self.layoutChanged.emit()
        except Exception as e:
            print(e)


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
                gp_item = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap().fromImage(q_img))
                gp_item.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable)
                self._pixmaps[QtCore.QPersistentModelIndex(index)] = gp_item
                self.graphicsView2D.scene.addItem(gp_item)
                self.active_modality = QtCore.QPersistentModelIndex(index)

            if self.model.data(index, VISIBILITY_ROLE):
                self._pixmaps[QtCore.QPersistentModelIndex(index)].show()
            else:
                self._pixmaps[QtCore.QPersistentModelIndex(index)].hide()

        #for overlay_key in self._overlays:
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
            start = QtCore.QPointF(slice_pos[0][0]*x_scaling, slice_pos[0][1]*y_scaling)
            end = QtCore.QPointF(slice_pos[1][0] * x_scaling,
                                   slice_pos[1][1] * y_scaling)
            line_item = QtWidgets.QGraphicsLineItem(QtCore.QLineF(start, end))
            line_item.setPen(QtGui.QPen().setColor("lawngreen"))
            self.addToGroup(line_item)

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


        #self.addButton_2d.clicked.connect(self.create_layer_2d)
        #self.addButton_3d.clicked.connect(self.create_layer_3d)

        self.registerButton_2d.clicked.connect(self.main_window.create_registration_view)

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


class AddPatientDialog(QtWidgets.QDialog, Ui_AddPatientDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.add_patient)
        self.buttonBox.rejected.connect(self.close)

    def add_patient(self):
        pseudonym = {"pseudonym": self.pseudonymEdit.text()}

        # Only pseudonym is uploaded
        r = requests.post("{}/patients/".format(oat_config["api_server"]),
                          headers=oat_config["auth_header"],
                          json=pseudonym)

        if r.status_code != 200:
            print(r.json())
            try:
                QtWidgets.QMessageBox.warning(self, 'Error', r.json()["detail"])
            except:
                QtWidgets.QMessageBox.warning(self, 'Error',
                                              "Patient could not be added to the database")
        else:
            # Save additional information to local patients file
            pd = {"pseudonym": self.pseudonymEdit.text(),
                  "gender": self.genderBox.currentText().lower(),
                  "birthday": self.birthdayEdit.date().toString(Qt.ISODate)}
            patient_data = {key: pd[key] for key in pd if pd[key]}

            self.add_local_patient_info(patient_data)
            self.accept()

    def add_local_patient_info(self, patient_data: dict):
        try:
            patients_info = get_local_patient_info(
                oat_config["local_patient_info_file"],
                oat_config["fernet"])
        except Exception as e:
            raise e

        if patient_data["pseudonym"] not in patients_info.pseudonym:
            patients_info = patients_info.append(patient_data,
                                                 ignore_index=True)
            with open(oat_config["local_patient_info_file"], "wb") as myfile:
                myfile.write(oat_config["fernet"].encrypt(
                    patients_info.to_csv(index=False).encode('utf8')))


class LoginDialog(QtWidgets.QDialog, Ui_LoginDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        _translate = QtCore.QCoreApplication.translate

        self.db_dict = {"Default DB": "http://localhost/api/v1"}

        self.setupUi(self)

        for i, key in enumerate(self.db_dict.keys()):
            self.dbDropdown.addItem(key)

        self.buttonBox.accepted.connect(self.handleLogin)
        self.buttonBox.rejected.connect(self.close)

    def handleLogin(self):
        # query selected DB for user:
        db_key = self.dbDropdown.currentText()
        api_server = self.db_dict[db_key]

        login_data = {
            "username": self.username.text(),
            "password": self.password.text(),
        }
        if True:
            pass
            login_data = {
                "username": "oli4morelle@gmail.com",
                "password": "testpw",
            }

        r = requests.post(f"{api_server}/login/access-token", data=login_data)

        if r.status_code != 200:
            print(r.status_code)
            QtWidgets.QMessageBox.warning(self, 'Error',
                                          'Wrong username or password')
        else:
            response = r.json()
            auth_token = response["access_token"]
            oat_config["auth_header"] = {
                "Authorization": f"Bearer {auth_token}"}
            oat_config["api_server"] = api_server
            oat_config["local_patient_info_file"] = \
                Path.home() / ".oat" / f"{login_data['username']}_patients.csv"
            oat_config["fernet"] = get_fernet(login_data['password'])

            # Create local patients info if not existing
            if not oat_config["local_patient_info_file"].exists():
                columns = ["pseudonym"]
                patients_info = pd.DataFrame(columns=columns)
                with open(oat_config["local_patient_info_file"],
                          "wb") as myfile:
                    myfile.write(oat_config["fernet"].encrypt(
                        patients_info.to_csv(index=False).encode('utf8')))
            self.accept()


def main():
    application = QApplication(sys.argv)
    global oat_config
    oat_config = {}
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

