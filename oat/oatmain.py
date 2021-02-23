import logging
from functools import partial

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QMainWindow)

from oat.config import OAT_FOLDER
from oat.models import PatientsModel, CollectionsModel
from oat.models.config import DATA_ROLE
from oat.modules.annotation.views.annotation_view import AnnotationView
from oat.modules.navigation import NavigationView
from oat.modules.registration import RegistrationView
from oat.modules.registration.models.registration_model import RegistrationModel
from oat.modules.dialogs.login import LoginDialog
from oat.modules.dialogs.upload import ImportCfpDialog, ImportVolDialog, \
    ImportHexmlDialog, ImportFolderDialog
from oat.views.ui.ui_main_window import Ui_MainWindow


class oat(QMainWindow, Ui_MainWindow):
    """Create the main window that stores all of the widgets necessary for the application."""

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super().__init__(parent)
        self.setupUi(self)
        self.models = {"patients": PatientsModel(), "collections": CollectionsModel()}

        self.actionImportVol.triggered.connect(partial(self.upload, type="vol"))
        self.actionImportCfp.triggered.connect(partial(self.upload, type="cfp"))
        self.actionImportHEXML.triggered.connect(partial(self.upload, type="hexml"))
        self.actionImportBSFolder.triggered.connect(partial(self.upload, type="folder"))
        self.actionSave.triggered.connect(self.save)
        self.actionExport.triggered.connect(self.export)

        self.overview_view = NavigationView(model=self.models["collections"],
                                            parent=self)
        self.overview_view.annotateButton.clicked.connect(self.open_annotation_view)
        self.overview_view.registerButton.clicked.connect(self.open_registration_view)
        self.navigationDock.setWidget(self.overview_view)

    def open_annotation_view(self):
        overview = self.overview_view
        data = overview.model.data(overview.tableView.selectionModel().currentIndex(), role=DATA_ROLE)

        volume_ids = [v["id"] for v in data["volumeimages"]]
        volume_ids_with_localizer = [v["id"] for v in data["volumeimages"]
                                     if not v["localizer_image"] is None]
        volume_ids_without_localizer = list(set(volume_ids)-set(volume_ids_with_localizer))

        enface_ids = [e["id"] for e in data["enfaceimages"]]

        localizer_ids = [v["localizer_image"]["id"] for v in data["volumeimages"]
                         if not v["localizer_image"] is None]
        other_enface_ids = list(set(enface_ids) - set(localizer_ids))

        ao = AnnotationView(volume_ids_with_localizer, volume_ids_without_localizer,
                            other_enface_ids, parent=self)
        self.setCentralWidget(ao)

    def open_registration_view(self):
        overview = self.overview_view
        data = overview.model.data(overview.tableView.selectionModel().currentIndex(), role=DATA_ROLE)
        localizer_id = data["volumeimages"][0]["localizer_image"]["id"]
        cfp_id = data["enfaceimages"][0]["id"]

        model = RegistrationModel(localizer_id, cfp_id)
        rv = RegistrationView(model)
        self.setCentralWidget(rv)

    def upload(self, type):
        if type == "cfp":
            dialog = ImportCfpDialog(models=self.models)
        elif type == "vol":
            dialog = ImportVolDialog(models=self.models)
        elif type == "hexml":
            dialog = ImportHexmlDialog(models=self.models)
        elif type == "folder":
            dialog = ImportFolderDialog(models=self.models)
        else:
            raise ValueError("'type' has to be either 'cfp' or 'vol'")

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            pass

    def save(self):
        pass

    def export(self):
        pass


def main(log_level=logging.DEBUG):
    # create logger for "oat" application
    logger = logging.getLogger("oat")
    logger.setLevel(logging.DEBUG)
    # create file handler which logs debug messages
    fh = logging.FileHandler(OAT_FOLDER / 'oat.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    # create formatter and add it to the handlers
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    cmd_formatter = logging.Formatter(
        '%(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(file_formatter)
    ch.setFormatter(cmd_formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("Starting Application.")
    application = QApplication(sys.argv)
    login = LoginDialog()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = oat()
        desktop = QDesktopWidget().availableGeometry()
        width = (desktop.width() - window.width()) / 2
        height = (desktop.height() - window.height()) / 2
        window.show()
        window.move(width, height)

        sys.exit(application.exec_())

if __name__ == '__main__':
    main()

