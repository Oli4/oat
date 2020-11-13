from pathlib import Path

import requests

from oat import config


def upload_vol(filepath, patient_id, collection_id=None):
    files = {'upl_file': (str(Path(filepath).name),
                          open(filepath, 'rb'),
                          "multipart/form-data"),
             "patient_id": (None, patient_id)}

    new_volume = requests.post(f"{config.api_server}/volumeimages/upload/vol",
                               files=files,
                               headers=config.auth_header)
    new_id = new_volume.json()["id"]

    # Add volume to collection if provided
    if collection_id:
        response = requests.get(f"{config.api_server}/collections/{collection_id}",
                                headers=config.auth_header)
        collection = response.json()
        volumeimage_ids = [x["id"] for x in collection["volumeimages"]]
        data = {"volumeimages": [new_id, ] + volumeimage_ids}

        requests.put(f"{config.api_server}/collections/{collection_id}",
                     headers=config.auth_header,
                     json=data)

    return new_volume


def upload_enface(filepath, patient_id, modality, collection_id=None):
    files = {'upl_file': (str(Path(filepath).name),
                          open(filepath, 'rb'),
                          "multipart/form-data"),
             "patient_id": (None, patient_id),
             "modality": (None, modality)}

    new_enface = requests.post(f"{config.api_server}/enfaceimages/upload/",
                               files=files,
                               headers=config.auth_header)

    new_id = new_enface.json()["id"]

    # Add enface to collection if provided
    if collection_id:
        response = requests.get(f"{config.api_server}/collections/{collection_id}",
                                headers=config.auth_header)
        collection = response.json()
        enfaceimage_ids = [x["id"] for x in collection["enfaceimages"]]
        data = {"enfaceimages": [new_id, ] + enfaceimage_ids}

        requests.put(f"{config.api_server}/collections/{collection_id}",
                     headers=config.auth_header,
                     json=data)

    return new_enface
