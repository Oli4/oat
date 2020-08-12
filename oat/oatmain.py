import logging
from functools import partial

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QMainWindow)

from oat.config import OAT_FOLDER
from oat.models.registration_model import RegistrationModel
from oat.views.annotation.annotation_view import AnnotationView
from oat.views.dialogs.login import LoginDialog
from oat.views.dialogs.upload import UploadCfpDialog, UploadVolDialog
from oat.views.registration.registration_view import RegistrationView
from oat.views.ui.ui_main_window import Ui_MainWindow


class oat(QMainWindow, Ui_MainWindow):
    """Create the main window that stores all of the widgets necessary for the application."""

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super().__init__(parent)
        self.setupUi(self)

        self.actionUploadVol.triggered.connect(partial(self.upload, type="vol"))
        self.actionUploadCfp.triggered.connect(partial(self.upload, type="cfp"))
        self.actionSave.triggered.connect(self.save)
        self.actionExport.triggered.connect(self.export)

        #registration_view = RegistrationView(model=RegistrationModel(2, 3),
        #                                     parent=self)
        #self.mdiArea.addSubWindow(registration_view)

        annotation_view = AnnotationView(0, parent=self)
        self.mdiArea.addSubWindow(annotation_view)



    def upload(self, type):
        if type == "cfp":
            dialog = UploadCfpDialog()
        elif type == "vol":
            dialog = UploadVolDialog()
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

