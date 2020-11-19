import logging

from PyQt5 import QtWidgets

from oat.models.config import DATA_ROLE
from oat.models.db import AreaTypeModel
from oat.modules.annotation.models import TreeItemModel, TreeGraphicsItem
from oat.views.ui.ui_add_areaannotation_dialog import Ui_AreaAnnotationDialog

logger = logging.getLogger(__name__)


class AddAnnotationDialog(QtWidgets.QDialog, Ui_AreaAnnotationDialog):
    def __init__(self, layer_model: TreeItemModel, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.layer_model = layer_model

        model = AreaTypeModel(self)
        self.typeDropdown.setModel(model)
        self.typeDropdown.update()
        self.buttonBox.accepted.connect(self.add_areaannotation)
        self.buttonBox.rejected.connect(self.close)

    def add_areaannotation(self):
        # Create AreaAnnotation of selected Type
        area_type_data = self.typeDropdown.currentData(role=DATA_ROLE)
        area_annotation = {"annotationtype_id": area_type_data["id"],
                           "current_color": area_type_data["default_color"],
                           "image_id": self.layer_model.scene.image_id,
                           "z_value": self.layer_model.rowCount()
                           }
        if self.layer_model.scene.base_name in ["CFP", "NIR", "Enface"]:
            t = "enface"
        elif self.layer_model.scene.base_name in ["OCT"]:
            t = "slice"
        new_item = TreeGraphicsItem.create(area_annotation, type=t)
        self.layer_model.appendRow(new_item)
