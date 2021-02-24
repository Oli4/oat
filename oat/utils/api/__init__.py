from pathlib import Path

import requests

from oat import config
import eyepy as ep

from io import BytesIO
import imageio
import numpy as np
import json

def upload_hexml(filepath, patient_id, collection_id):
    data = ep.Oct.from_heyex_xml(filepath)
    upload_eyepy_Oct(data, patient_id, collection_id)

def upload_vol(filepath, patient_id, collection_id):
    data = ep.Oct.from_heyex_vol(filepath)
    upload_eyepy_Oct(data, patient_id, collection_id)

def upload_folder(filepath, patient_id, collection_id):
    data = ep.Oct.from_folder(filepath)
    upload_eyepy_Oct(data, patient_id, collection_id)

def upload_eyepy_Oct(data, patient_id, collection_id):
    # create volume
    has_meta = True
    try:
        data.meta
    except AttributeError:
        has_meta = False

    if has_meta:
        volumeimage_data = dict(patient_id=patient_id,
                                visit_data=str(data.VisitDate),
                                modality="OCT", scale_x=data.ScaleX,
                                scale_z=data.ScaleZ, distance=data.Distance,
                                size_x=data.SizeX, num_bscans=data.NumBScans,
                                size_z=data.SizeZ, scan_focus=data.ScanFocus,
                                scan_position=data.ScanPosition,
                                collection_ids=[collection_id])
    else:
        volumeimage_data = dict(patient_id=patient_id,
                                modality="OCT",
                                size_x=data.shape[1], num_bscans=len(data),
                                size_z=data.shape[0],
                                scan_position="Unknown",
                                collection_ids=[collection_id])
    volumeimage = requests.post(
        f"{config.api_server}/volumeimages/", json=volumeimage_data,
        headers=config.auth_header)

    has_localizer=True
    try:
        data.localizer
    except AttributeError:
        has_localizer=False
    if has_localizer:
        localizer_kwargs = dict(scale_x=data.ScaleXSlo,
                                scale_y=data.ScaleYSlo,
                                visit_date=str(data.VisitDate),
                                field_size=data.FieldSizeSlo,
                                registered_volume_id=volumeimage.json()["id"])

        with BytesIO() as fileobj:
            imageio.imwrite(fileobj, data.localizer, format="png")
            file_obj = fileobj.getvalue()
        localizer = upload_enface(file_obj, "png", patient_id=patient_id,
                                  collection_id=collection_id, modality="NIR",
                                  **localizer_kwargs)

    linetypes = requests.get(f"{config.api_server}/linetypes/me",
                             headers=config.auth_header).json()
    for i, slice in enumerate(data):
        if has_meta:
            slice_kwargs = dict(volumeimage_id=volumeimage.json()["id"],
                                start_x=slice.StartX,
                                start_y=slice.StartY,
                                end_x=slice.EndX,
                                end_y=slice.EndY,
                                quality=slice.Quality,
                                number=i, )
        else:
            slice_kwargs = dict(volumeimage_id=volumeimage.json()["id"],
                                number=i, )
        with BytesIO() as fileobj:
            imageio.imwrite(fileobj, slice.scan, format="png")
            file_obj = fileobj.getvalue()
        slice_response = upload_slice(file_obj, "png", **slice_kwargs)

        # upload line annotations
        for l_name in slice.layers:
            try:
                heights = slice.layers[l_name]
            except KeyError:
                continue
            points = {"points": [(x, np.round(float(y), 1))
                                 for x, y in enumerate(heights)]}

            if l_name not in [l["name"] for l in linetypes]:
                new_type = requests.post(
                    f"{config.api_server}/linetypes/",
                    json={"description": "","name": l_name,"public": True},
                    headers=config.auth_header).json()
                linetypes.append(new_type)

            type_id, color = [(l["id"], l["default_color"])
                       for l in linetypes if l["name"]==l_name][0]

            lineannotation_data = {
                "line_data": json.dumps(points),
                "image_id": slice_response.json()["id"],
                "current_color": color,
                "annotationtype_id": type_id}
            requests.post(
                f"{config.api_server}/slicelineannotations/",
                json=lineannotation_data,
                headers=config.auth_header)


def upload_slice_file(filepath, volumeimage_id, number, type="standard"):
    return upload_slice(file_object=open(filepath, 'rb'),
                        filetype=str(Path(filepath).suffix),
                        volumeimage_id=volumeimage_id,
                        number=number,
                        type=type)

def upload_slice(file_object, filetype, **kwargs):
    files = {'upl_file': (f"dummy.{filetype.strip('.')}",
                          file_object, "multipart/form-data")}
    #files = {**files, **kwargs}

    return requests.post(f"{config.api_server}/slices/upload/",
                         files=files, data=kwargs,
                         headers=config.auth_header)

def upload_enface_file(filepath, patient_id, collection_id, modality):
    return upload_enface(file_object=open(filepath, 'rb'),
                         filetype=str(Path(filepath).suffix),
                         patient_id=patient_id,
                         modality=modality,
                         collection_id=collection_id)

def upload_enface(file_object, filetype, patient_id, collection_id, modality, **kwargs):
    files = {'upl_file': (f"dummy.{filetype.strip('.')}",
                          file_object, "multipart/form-data")}
    kwargs = {**{"patient_id": patient_id, "collection_ids":[collection_id],
                 "modality":modality}, **kwargs}
    new_enface = requests.post(f"{config.api_server}/enfaceimages/upload/",
                               files=files, data=kwargs,
                               headers=config.auth_header)

    new_id = new_enface.json()["id"]

    # Add enface to collection if provided
    if collection_id:
        response = requests.get(
            f"{config.api_server}/collections/{collection_id}",
            headers=config.auth_header)
        collection = response.json()
        enfaceimage_ids = [x["id"] for x in collection["enfaceimages"]]
        data = {"enfaceimages": [new_id, ] + enfaceimage_ids}

        requests.put(f"{config.api_server}/collections/{collection_id}",
                     headers=config.auth_header,
                     json=data)

    return new_enface
