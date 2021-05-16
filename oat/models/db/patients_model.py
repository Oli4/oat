import pandas as pd
import requests
from PySide6 import QtCore

from oat import config
from oat.core.security import get_local_patient_info

from oat.models.db.base_model import BaseModel

class PatientsModel(BaseModel):
    def __init__(self):
        super().__init__(db_endpoint="patients")

    @property
    def default_headers(self):
        return ["pseudonym", "id", "gender", "birthday"]

    def record_processing(self, record_in):

        local_data = get_local_patient_info(
            config.local_patient_info_file,
            config.fernet)
        local_data.set_index("pseudonym", inplace=True)
        local_dict = local_data.to_dict(orient="records")

        if record_in["pseudonym"] in local_dict:
            for k, v in local_dict.items():
                record_in[k] = v
        else:
            record_in["gender"] = ""
            record_in["birthday"] = ""

        return record_in

