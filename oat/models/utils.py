import functools
import io

import imageio
import qimage2ndarray
import requests
from PyQt5 import QtWidgets, QtGui

from oat import config


@functools.lru_cache(maxsize=4, typed=False)
def get_enface_by_id(img_id, format="jpeg"):
    return get_img_by_id(img_id, type="enface", format=format)


@functools.lru_cache(maxsize=300, typed=False)
def get_bscan_by_id(img_id, format="jpeg"):
    return get_img_by_id(img_id, type="bscan", format=format)


def get_registration_from_enface_ids(id1, id2):
    response = requests.get(
        f"{config.api_server}/registrations/"
        f"?enfaceimage1_id={id1}"
        f"&enfaceimage2_id={id2}",
        headers=config.auth_header)
    if response.status_code == 200:
        return response.json()
    else:
        msg = f"Status {response.status_code}: {response.json()['detail']}"
        raise ValueError(msg)


def get_img_by_id(img_id, type, format):
    if type == "enface":
        path = "enfaceimages"
    elif type == "bscan":
        path = "slices"
    else:
        msg = f"Parameter type has to be (enface|bscan) not {type}"
        raise ValueError(msg)

    response = requests.get(
        f"{config.api_server}/{path}/data/{format}/{img_id}",
        headers=config.auth_header)
    if response.status_code == 200:
        meta = {k.lower(): v for k, v in response.headers.items()}
        img = imageio.imread(io.BytesIO(response.content), format=format)
        return img, meta
    else:
        raise ValueError(f"Status Code: {response.status_code}")


def get_volume_meta_by_id(volume_id):
    response = requests.get(
        f"{config.api_server}/volumeimages/{volume_id}",
        headers=config.auth_header)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Status Code: {response.status_code}")


def array2qgraphicspixmapitem(image):
    return QtWidgets.QGraphicsPixmapItem(
        QtGui.QPixmap().fromImage(qimage2ndarray.array2qimage(image)))


def qgraphicspixmapitem2array(pixmapitem):
    return qimage2ndarray.rgb_view(pixmapitem.pixmap().toImage())


def qgraphicspixmap2array(pixmap):
    return qimage2ndarray.rgb_view(pixmap.toImage())


def get_collection_by_id(id):
    response = requests.get(
        f"{config.api_server}/collections/{id}",
        headers=config.auth_header)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Status Code: {response.status_code}")
