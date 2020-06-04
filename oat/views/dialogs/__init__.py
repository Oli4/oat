from pathlib import Path

import pandas as pd
import requests
from PyQt5 import QtWidgets, Qt, QtCore

from oat import config
from oat.core.security import get_local_patient_info, get_fernet
from oat.models.patients import PatientsModel
from oat.utils.api import upload_enface, upload_vol
from oat.views.ui import Ui_AddPatientDialog, Ui_LoginDialog, Ui_UploadDialog


class UploadDialog(QtWidgets.QDialog, Ui_UploadDialog):
    def __init__(self, parent=None, filefilter=None):
        super().__init__(parent)
        self.setupUi(self)

        self.filefilter = filefilter

        self.patientDropdown.setModel(PatientsModel())
        self.fileSelectButton.clicked.connect(self.select_file)
        self.buttonBox.accepted.connect(self.check_upload)

        self.fname = ''
        self.patient_id = None

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


class AddPatientDialog(QtWidgets.QDialog, Ui_AddPatientDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.add_patient)
        self.buttonBox.rejected.connect(self.close)

    def add_patient(self):
        pseudonym = {"pseudonym": self.pseudonymEdit.text()}

        # Only pseudonym is uploaded
        r = requests.post("{}/patients/".format(config.api_server),
                          headers=config.auth_header,
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
                config.local_patient_info_file,
                config.fernet)
        except Exception as e:
            raise e

        if patient_data["pseudonym"] not in patients_info.pseudonym:
            patients_info = patients_info.append(patient_data,
                                                 ignore_index=True)
            with open(config.local_patient_info_file, "wb") as myfile:
                myfile.write(config.fernet.encrypt(
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
            login_data = {
                "username": "admin@retina-annotation-tool.com",
                "password": "4dc86c90f921dfd3727c99893b17dcf36a84642a332da52d626fd3573e171d98",
            }

        r = requests.post(f"{api_server}/login/access-token", data=login_data)

        if r.status_code != 200:
            QtWidgets.QMessageBox.warning(self, 'Error',
                                          'Wrong username or password')
        else:
            response = r.json()
            auth_token = response["access_token"]
            config.auth_header = {
                "Authorization": f"Bearer {auth_token}"}
            config.api_server = api_server
            config.local_patient_info_file = \
                Path.home() / ".oat" / f"{login_data['username']}_patients.csv"
            config.fernet = get_fernet(login_data['password'])

            # Create local patients info if not existing
            if not config.local_patient_info_file.exists():
                columns = ["pseudonym"]
                patients_info = pd.DataFrame(columns=columns)
                with open(config.local_patient_info_file,
                          "wb") as myfile:
                    myfile.write(config.fernet.encrypt(
                        patients_info.to_csv(index=False).encode('utf8')))
            self.accept()
