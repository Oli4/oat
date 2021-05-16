import pandas as pd
import requests
from PySide6 import QtCore

from oat import config
from oat.models.config import DATA_ROLE, ID_ROLE, EMPTY_ROLE

from oat.models.db.base_model import BaseModel
from datetime import datetime

class CollectionsModel(BaseModel):
    def __init__(self):
        super().__init__(db_endpoint="collections")

    @property
    def default_headers(self):
        return ["dropdown_text", "name", "patient_id", "patient_pseudonym", "registered", "created_by", "created_at",
                "enfaceimage_ids", "volumeimage_ids", "laterality", "id",]

    def record_processing(self, record_in):
        patient = record_in.pop("patient")
        record_in["patient_id"] = patient["id"]
        record_in["patient_pseudonym"] = patient["pseudonym"]

        record_in["dropdown_text"] = record_in["name"] + " (" + record_in["laterality"] + ")"
        record_in["created_at"] = datetime.fromisoformat(record_in["created_at"])
        if len(record_in["enfaceimage_ids"]) + len(record_in["volumeimage_ids"]) == 0:
            record_in["empty"] = True
        else:
            record_in["empty"] = False
        return record_in