from functools import partial

import sys
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QMainWindow)

from oat.views import *
from oat.views.dialogs import LoginDialog, UploadCfpDialog, UploadVolDialog


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

        sys.exit(application.exec_())

if __name__ == '__main__':
    main()

