from pathlib import Path

import requests

from oat import config


def upload_vol(filepath, patient_id):
    files = {'upl_file': (str(Path(filepath).name),
                          open(filepath, 'rb'),
                          "multipart/form-data"),
             "patient_id": (None, patient_id)}

    return requests.post(f"{config.api_server}/volumeimages/upload/vol",
                         files=files,
                         headers=config.auth_header)


def upload_enface(filepath, patient_id, modality):
    files = {'upl_file': (str(Path(filepath).name),
                          open(filepath, 'rb'),
                          "multipart/form-data"),
             "patient_id": (None, patient_id),
             "modality": (None, modality)}

    return requests.post(f"{config.api_server}/enfaceimages/upload/",
                         files=files,
                         headers=config.auth_header)
