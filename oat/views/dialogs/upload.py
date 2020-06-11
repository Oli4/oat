import logging
from pathlib import Path

from PyQt5 import QtWidgets, QtCore

from oat import config
from oat.models import PatientsModel
from oat.utils.api import upload_vol, upload_enface
from oat.views.dialogs import AddPatientDialog
from oat.views.ui.ui_upload_dialog import Ui_UploadDialog

logger = logging.getLogger(__name__)


class UploadDialog(QtWidgets.QDialog, Ui_UploadDialog):
    def __init__(self, parent=None, filefilter=None):
        super().__init__(parent)
        self.setupUi(self)

        self.filefilter = filefilter

        self.model = PatientsModel()
        self.patientDropdown.setModel(self.model)
        self.addPatientButton.clicked.connect(self.add_patient)
        self.fileSelectButton.clicked.connect(self.select_file)
        self.buttonBox.accepted.connect(self.check_upload)

        self.fname = ''
        self.patient_id = None

    def add_patient(self):
        dialog = AddPatientDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.model.reload_data()

    def select_file(self):
        self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                              "Select Upload File",
                                                              config.import_path,
                                                              self.filefilter)
        if self.fname != '':
            self.fileName.setText(str(Path(self.fname).name))

    def check_upload(self):
        patient_index = self.patientDropdown.currentIndex()
        self.patient_id = self.patientDropdown.model().headerData(
            patient_index, QtCore.Qt.Vertical, QtCore.Qt.DisplayRole)
        if self.fname == '':
            QtWidgets.QMessageBox.warning(self, 'Error',
                                          'No file selected for upload.')
        elif self.patientDropdown.currentText() == '':
            QtWidgets.QMessageBox.warning(self, 'Error',
                                          'No patient selected.')
        else:
            self.upload()

    def upload(self):
        pass


class UploadCfpDialog(UploadDialog):
    def __init__(self, parent=None):
        super().__init__(parent, filefilter="CFP (*.bmp *.BMP *.tif *.TIF"
                                            " *.tiff *.TIFF)")

    def upload(self):
        return upload_enface(self.fname, self.patient_id, 'CFP')


class UploadVolDialog(UploadDialog):
    def __init__(self, parent=None):
        super().__init__(parent, filefilter="Heyex Raw (*.vol)")

    def upload(self):
        return upload_vol(self.fname, self.patient_id)
