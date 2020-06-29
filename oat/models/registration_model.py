import io
from collections import defaultdict
from datetime import datetime
from typing import Optional

import imageio
import numpy as np
import qimage2ndarray
import requests
import skimage.segmentation as skiseg
import skimage.transform as skitrans
from PyQt5 import QtCore
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QPoint, QPointF, QModelIndex
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem
from pydantic import BaseModel
from skimage.color import gray2rgb

from oat import config
from oat.models.config import FEATUREID_ROLE, MATCHID_ROLE, SCENE_ROLE, \
    POINT_ROLE, FEATURE_DICT_ROLE

f_dict = {0: "feature1", 1: "feature2"}

class EnfaceImage(BaseModel):
    created_by: int
    visit_date: Optional[datetime] = None
    modality: str
    patient_id: int

    size_x: int
    size_y: int
    scale_x: Optional[float] = None
    scale_y: Optional[float] = None
    field_size: int = None


def get_enface_by_id(img_id):
    response = requests.get(
        f"{config.api_server}/enfaceimages/data/tiff/{img_id}",
        headers=config.auth_header)
    if response.status_code == 200:
        meta = {k.lower(): v for k, v in response.headers.items()}
        img = imageio.imread(io.BytesIO(response.content), format="tiff")
        return img, meta
    else:
        raise ValueError(f"Status Code: {response.status_code}")


class SceneModel(QtWidgets.QGraphicsScene):
    def __init__(self, parent, scene_id):
        super().__init__(parent)
        self.scene_id = scene_id


class RegistrationModel(QtCore.QAbstractTableModel):
    # Changing the marker does not trigger an DB update
    markerChanged = QtCore.pyqtSignal(QModelIndex)
    markersChanged = QtCore.pyqtSignal()

    def __init__(self, *args):
        super().__init__()

        self.image_ids = args
        self.images, self.images_meta = zip(*[get_enface_by_id(i)
                                              for i in self.image_ids])
        self.checker_images, self.checker_scale = \
            zip(*[self.img_rescale(img, 300) for img in self.images])

        self.scenes = {i: SceneModel(self, scene_id=i)
                       for i in range(len(self.image_ids))}
        # self.reg_scene = SceneModel(self, )
        for i, scene in self.scenes.items():
            scene.addItem(self.array2qgraphicspixmapitem(self.images[i]))
        self.scenes[-1] = SceneModel(self, scene_id=-1)

        self._data = None
        self.markers = {}

        self.markerChanged.connect(self.set_marker)
        self.markersChanged.connect(self.set_markers_from_model)
        self.markersChanged.connect(self.estimate_transformation)

        self.markerChanged.connect(self.estimate_transformation)

        self._changed_localy = defaultdict(lambda: False)

        self._tmodel = "similarity"
        self._checkerboard_size = 60
        self._tmodel_choices = ["similarity", "affine"]
        self.reload_data()

    def img_rescale(self, img, height):
        scale = height / img.shape[0]
        if len(img.shape) == 2:
            multichannel = False
        else:
            multichannel = True
        img = skitrans.rescale(img, scale, multichannel=multichannel,
                               anti_aliasing=False, preserve_range=True)
        return img, scale

    @property
    def tmodel(self):
        return self._tmodel

    @tmodel.setter
    def tmodel(self, value):
        if value in self._tmodel_choices:
            self._tmodel = value
            self.estimate_transformation()
        else:
            raise ValueError(f"'{value}' not available as a transformation"
                             f" model")

    @property
    def checkerboard_size(self):
        return self._checkerboard_size

    @checkerboard_size.setter
    def checkerboard_size(self, value):
        self._checkerboard_size = value
        self.update_checkerboard()

    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(QModelIndex)
    def estimate_transformation(self, index: QModelIndex = None):
        matches = self._data["enfacefeaturematchs"][:-1]
        dst = np.array([[m["feature1"]["x"], m["feature1"]["y"]]
                        for m in matches])
        src = np.array([[m["feature2"]["x"], m["feature2"]["y"]]
                        for m in matches])

        if dst.shape[0] >= 3:
            tform = skitrans.estimate_transform(
                self.tmodel, src * self.checker_scale[1],
                             dst * self.checker_scale[0])
            reg_img = skitrans.warp(self.checker_images[1],
                                    inverse_map=tform.inverse,
                                    output_shape=self.checker_images[0].shape,
                                    preserve_range=True)

            self.reg_img = reg_img
            self.update_checkerboard()

    def update_checkerboard(self):
        img1 = self.checker_images[0]
        img2 = self.reg_img
        size = self.checkerboard_size

        mask = skiseg.checkerboard_level_set(
            img1.shape[:2], size).astype(bool)

        if len(img1.shape) == 2:
            img1 = gray2rgb(img1)

        if len(img2.shape) == 2:
            img2 = gray2rgb(img2)

        checkerboard = np.copy(img1)
        checkerboard[np.where(mask)] = img2[np.where(mask)]

        self.scenes[-1].clear()
        self.scenes[-1].addItem(self.array2qgraphicspixmapitem(checkerboard))

    @QtCore.pyqtSlot()
    def set_markers_from_model(self):
        for col in range(self.columnCount()):
            for row in range(self.rowCount()):
                index = self.createIndex(row, col)
                try:
                    pos = self._get_marker_pos(index)
                except ValueError:
                    continue
                try:
                    self.markers[(index.row(), index.column())].setPos(pos)
                except KeyError:
                    marker = self._marker_1(pos)
                    self.markers[(index.row(), index.column())] = marker
                    self.scenes[index.column()].addItem(marker)

    @QtCore.pyqtSlot(QModelIndex)
    def set_marker(self, index: QModelIndex):
        # img is 0 for the fixed image and increases by one for every additional
        # moving image
        pos = self._get_marker_pos(index)
        if pos:
            try:
                self.markers[(index.row(), index.column())].setPos(pos)
            except KeyError:
                marker = self._marker_1(pos)
                self.markers[(index.row(), index.column())] = marker
                self.scenes[index.column()].addItem(marker)

    def _get_marker_pos(self, index):
        try:
            point = self.data(index, role=POINT_ROLE)
            return QtCore.QPointF(0.5, 0.5) + point
        except:
            raise ValueError(f"No feature position set at index"
                             f" ({index.row(), index.column()})")

    def _marker_1(self, pos):
        pos = QPoint(int(pos.x()), int(pos.y())) + QPointF(0.5, 0.5)
        marker = self._create_marker_1()
        marker.setPos(pos)
        marker.setZValue(10)
        return marker

    def _create_marker_1(self):
        marker_group = QGraphicsItemGroup()
        marker_group.addToGroup(QGraphicsLineItem(0, -3, 0, -2))
        marker_group.addToGroup(QGraphicsLineItem(0, 2, 0, 3))

        marker_group.addToGroup(QGraphicsLineItem(-3, 0, -2, 0))
        marker_group.addToGroup(QGraphicsLineItem(2, 0, 3, 0))

        return marker_group

    def array2qgraphicspixmapitem(self, image):
        return QtWidgets.QGraphicsPixmapItem(
            QtGui.QPixmap().fromImage(qimage2ndarray.array2qimage(image)))

    @QtCore.pyqtSlot(QModelIndex, QModelIndex)
    def upload_data(self, current_index, previous_index):
        index = previous_index
        if not self._changed_localy[index]:
            return None
        elif not self.data(index, POINT_ROLE):
            # Delete feature on server
            response = requests.delete(
                f"{config.api_server}/enfacefeatures/"
                f"{self.data(index, FEATUREID_ROLE)}",
                headers=config.auth_header)
            self._data["enfacefeaturematchs"][index.row()][
                f_dict[index.column()]] \
                = self._new_feature()
        elif self.data(index, FEATUREID_ROLE) is None:
            # Create feature on server
            response = requests.post(
                f"{config.api_server}/enfacefeatures/",
                json=self.data(index, FEATURE_DICT_ROLE),
                headers=config.auth_header)
            self._data["enfacefeaturematchs"][index.row()][
                f_dict[index.column()]] \
                = response.json()
        else:
            # Update feature on server
            response = requests.put(
                f"{config.api_server}/enfacefeatures/",
                json=self.data(index, FEATURE_DICT_ROLE),
                headers=config.auth_header)
            self._data["enfacefeaturematchs"][index.row()][
                f_dict[index.column()]] \
                = response.json()
        # Create new complete matches on server
        if self._data["enfacefeaturematchs"][index.row()]["id"] is None:
            if self.match_is_complete(index.row()):
                # Create new match in DB
                response = requests.post(
                    f"{config.api_server}/enfacefeaturematches/",
                    json=self._data["enfacefeaturematchs"][index.row()],
                    headers=config.auth_header)
                self._data["enfacefeaturematchs"][index.row()] = response.json()
        else:
            if not self.match_is_complete(index.row()):
                # Delete Match from DB
                response = requests.delete(
                    f"{config.api_server}/enfacefeaturematches/",
                    json=self._data["enfacefeaturematchs"][index.row()]["id"],
                    headers=config.auth_header)
                match = self._new_match()
                match["feature1"] = \
                    self._data["enfacefeaturematchs"][index.row()]["feature1"]
                match["feature2"] = \
                    self._data["enfacefeaturematchs"][index.row()]["feature2"]
                self._data["enfacefeaturematchs"][index.row()] = match

        # Add complete matches to registration
        matches = self._data["enfacefeaturematchs"]
        complete = [m for i, m in enumerate(matches)
                    if self.match_is_complete(i)]
        data = self._data
        data["enfacefeaturematchs"] = complete
        if self._data["id"] is None:
            # Create new registration
            response = requests.post(
                f"{config.api_server}/registrations/",
                json=data,
                headers=config.auth_header)
            new_data = response.json()
            new_data["enfacefeaturematchs"] = matches
            self._data = new_data
        else:
            # Update existing transformations
            response = requests.put(
                f"{config.api_server}/registrations/",
                json=data,
                headers=config.auth_header)
            new_data = response.json()
            new_data["enfacefeaturematchs"] = matches
            self._data = new_data
        self._changed_localy[index] = False

    def _new_feature(self, n):
        return {"x": None, "y": None, "id": None,
                "enfaceimage_id": self.image_ids[n - 1]}

    def _new_match(self):
        return {"id": None,
                "feature1": self._new_feature(1),
                "feature2": self._new_feature(2),
                "enfaceimage1_id": self.image_ids[0],
                "enfaceimage2_id": self.image_ids[1]
                }

    def new(self):
        data = {"enfaceimage1_id": self.image_ids[0],
                "enfaceimage2_id": self.image_ids[1],
                "similarity": [0] * 9,
                "affine": [0] * 9,
                "enfacefeaturematchs": [self._new_match()],
                "id": None,
                "created_by": None}
        return data

    def reload_data(self):
        response = requests.get(
            f"{config.api_server}/registrations/"
            f"?enfaceimage1_id={self.image_ids[0]}"
            f"&enfaceimage2_id={self.image_ids[1]}",
            headers=config.auth_header)
        if response.status_code == 200:
            self._data = response.json()
            if self._data["enfacefeaturematchs"] == []:
                self._data["enfacefeaturematchs"].append(self._new_match())
        else:
            self._data = self.new()

        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(),
                                               self.columnCount()),
                              (QtCore.Qt.DisplayRole,))
        self.markersChanged.emit()

    def data(self, index, role=QtCore.Qt.DisplayRole):

        row, col = (index.row(), index.column())
        match = self._data["enfacefeaturematchs"][row]
        feat = match[f_dict[col]]
        if role == QtCore.Qt.DisplayRole:
            return f"({feat['x']}, {feat['y']})"
        elif role == POINT_ROLE:
            try:
                return QPointF(feat["x"], feat["y"])
            except:
                return False
        elif role == FEATURE_DICT_ROLE:
            return feat
        elif role == FEATUREID_ROLE:
            return feat["id"]
        elif role == MATCHID_ROLE:
            return match["id"]
        elif role == SCENE_ROLE:
            return self.scenes[col]

    def match_is_empty(self, row):
        match = self._data["enfacefeaturematchs"][row]
        feat1 = match["feature1"]
        feat2 = match["feature2"]
        if feat1["x"] == feat1["y"] == feat2["x"] == feat2["y"] == None:
            return True
        return False

    def match_is_complete(self, row):
        match = self._data["enfacefeaturematchs"][row]
        feat1 = match["feature1"]
        feat2 = match["feature2"]
        if not (None in [feat1["x"], feat1["y"], feat2["x"], feat2["y"]]):
            return True
        return False

    def insertRows(self, row: int, count: int,
                   parent: QModelIndex = ...) -> bool:
        if row != self.rowCount() or count != 1 or self.match_is_empty(-1):
            return False
        self.beginInsertRows(parent, row, row)
        self._data["enfacefeaturematchs"].append(self._new_match())
        self.endInsertRows()
        return True

    def rowCount(self, index=None):
        # The length of the outer list.
        return len(self._data["enfacefeaturematchs"])

    def columnCount(self, index=None):
        return 2

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        names = ["Fixed Image", "Moving Image"]
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return names[section]

            if orientation == QtCore.Qt.Vertical:
                return str(section)

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        # flags |= QtCore.Qt.ItemIsEditable
        # flags |= QtCore.Qt.ItemIsSelectable
        flags |= QtCore.Qt.ItemIsEnabled
        # flags |= QtCore.Qt.ItemIsDragEnabled
        # flags |= QtCore.Qt.ItemIsDropEnabled
        return flags

    # In future this might be used for sorting by feature residuals
    # def sort(self, Ncol, order):
    #    """Sort table by given column number.
    #    """
    #    try:
    #        self.layoutAboutToBeChanged.emit()
    #        self._data["enfacefeaturematchs"] = \
    #            sorted(self._data["enfacefeaturematchs"], key=lambda x: )
    #        self.layoutChanged.emit()
    #    except Exception as e:
    #        print(e)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return False

        f_dict = {0: "feature1", 1: "feature2"}
        row, col = (index.row(), index.column())
        match = self._data["enfacefeaturematchs"][row]
        feat = match[f_dict[col]]

        if role == QtCore.Qt.EditRole:
            feat["x"], feat["y"] = (value.x(), value.y())
            self._changed_localy[index] = True
            self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole,
                                                 POINT_ROLE))
            self.markerChanged.emit(index)
        elif role == FEATUREID_ROLE:
            feat["id"] = value
        elif role == MATCHID_ROLE:
            match["id"] = value
        else:
            return False
        return True
