from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget

from oat import AddPatientDialog
from oat.views import Ui_DataTableView


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
