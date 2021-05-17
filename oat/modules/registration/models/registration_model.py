import copy
import logging
from typing import Iterable

import numpy as np
import requests
import skimage.color as skicolor
from skimage.segmentation import checkerboard_level_set
import skimage.transform as skitrans
from PySide6.QtCore import QPointF, QModelIndex

from oat import config
from PySide6 import QtCore, QtGui, QtWidgets
from oat.models.config import FEATUREID_ROLE, MATCHID_ROLE, SCENE_ROLE, \
    POINT_ROLE, FEATURE_DICT_ROLE, DELETE_ROLE
import qimage2ndarray
from oat.models.utils import array2qgraphicspixmapitem, get_registration_from_enface_ids

logger = logging.getLogger(__name__)
f_dict = {0: "feature1", 1: "feature2"}

from typing import Tuple, Dict

from PySide6.QtWidgets import QGraphicsPixmapItem
from oat.models.utils import get_enface_by_id


class CustomGrahpicsScene(QtWidgets.QGraphicsScene):
    number = 0
    base_name = "Default"

    def __init__(self, parent, image_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)
        self._set_name()

        self.image = None
        self.image_meta = None

        self._widthForHeightFactor = 1
        # Slice number for OCT Scenes, Enfaceimages are slice 0
        self.current_slice_number = 0

        self.area_annotations = []
        self.background_on = True
        self.fake_cursor = self.addPixmap(
            QtGui.QPixmap(":/cursors/cursors/navigation_cursor.svg"))

        self.image_id = None

        self.img_array = None
        if image_id:
            self.set_image(image_id)

    def _set_name(self):
        if self.number == 0:
            self.name = self.base_name
            self.number += 1
        else:
            self.name = f"{self.base_name}_{self.number}"
            self.number += 1

    def _fetch_image(self, image_id) -> Tuple[QGraphicsPixmapItem, Dict]:
        raise NotImplementedError

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF):
        painter.translate(-0.5, -0.5)
        if self.background_on:
            painter.fillRect(self.sceneRect(), self.backgroundBrush())
        else:
            painter.fillRect(self.sceneRect(), QtCore.Qt.NoBrush)

    def set_image(self, image_id):
        self.image_id = image_id
        self.img_array, meta = self._fetch_image(image_id)
        qimage = qimage2ndarray.array2qimage(self.img_array)
        self.image_meta = meta
        self.shape = (qimage.height(), qimage.width())

        self.setSceneRect(QtCore.QRectF(0.0, 0.0, qimage.width(), qimage.height()))
        self._widthForHeightFactor = \
            1.0 * qimage.width() / qimage.height()
        brush = QtGui.QBrush(qimage)
        self.setBackgroundBrush(brush)

    def hide_background(self):
        if self.background_on:
            self.background_on = False
            self.invalidate(self.sceneRect(), QtWidgets.QGraphicsScene.BackgroundLayer)

    def show_background(self):
        if not self.background_on:
            self.background_on = True
            self.invalidate(self.sceneRect(), QtWidgets.QGraphicsScene.BackgroundLayer)


class RegistrationGraphicsScene(CustomGrahpicsScene):
    def __init__(self, parent, column, *args, **kwargs):
        self.urlprefix = "enface"
        super().__init__(*args, **kwargs, parent=parent)
        self.column = column


    def _fetch_image(self, image_id) -> Tuple[np.ndarray, Dict]:
        img, meta = get_enface_by_id(image_id)
        return img, meta


class RegistrationModel(QtCore.QAbstractTableModel):
    def __init__(self, collection_data):
        super().__init__()

        self.collection_data = collection_data
        self.cfp = [image for image in self.collection_data["enfaceimages"] if image["modality"] == "CFP"][0]
        self.nir = [image for image in self.collection_data["enfaceimages"] if image["modality"] == "NIR"][0]
        self.image_ids = [self.cfp["id"], self.nir["id"]]

        self.scenes = {0: RegistrationGraphicsScene(self, 0, image_id=self.nir["id"]),
                       1: RegistrationGraphicsScene(self, 1, image_id=self.cfp["id"])}

        self.checker_images, self.checker_scale = zip(*[self.img_rescale(scene.img_array, 300)
                                                        for scene in self.scenes.values()])

        self.scenes[-1] = RegistrationGraphicsScene(self, -1)

        self._data = None
        self.markers = {}

        self.dataChanged.connect(self.update_markers)
        self.dataChanged.connect(self.update_checkerboard)

        self._tmodel = "similarity"
        self._checkerboard_size = 60
        self._tmodel_choices = ["similarity", "affine"]

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
    def tform(self):
        self.estimate_transformation()
        return self._tform

    @property
    def local_tform(self):
        self.estimate_transformation()
        return self._local_tform


    @property
    def checkerboard_size(self):
        return self._checkerboard_size

    @checkerboard_size.setter
    def checkerboard_size(self, value):
        self._checkerboard_size = value
        self.update_checkerboard()

    def estimate_transformation(self):
        matches = [m for i, m in enumerate(self._data["enfacefeaturematchs"])
                   if self.match_is_complete(i)]
        dst = np.array([[m["feature1"]["x"], m["feature1"]["y"]]
                        for m in matches])
        src = np.array([[m["feature2"]["x"], m["feature2"]["y"]]
                        for m in matches])

        if dst.shape[0] >= 3:
            local_tform = skitrans.estimate_transform(
                self.tmodel, src * self.checker_scale[1],
                             dst * self.checker_scale[0])
            tform = skitrans.estimate_transform(
                self.tmodel, src, dst)

        else:
            matrix = np.array([1, 0, 0, 0, 1, 0, 0, 0, 1]).reshape((3, 3))
            local_tform = skitrans.ProjectiveTransform(matrix)
            tform = local_tform
        self._data[self.tmodel] = [float(p) for p in tform.params.flatten()]
        self._local_tform = local_tform
        self._tform = tform

    def update_checkerboard(self):
        img1 = self.checker_images[0]
        print(self.checker_images[1].shape)
        img2 = skitrans.warp(self.checker_images[1],
                             inverse_map=self.local_tform.inverse,
                             output_shape=self.checker_images[0].shape,
                             preserve_range=True)

        size = self.checkerboard_size

        mask = checkerboard_level_set(
            img1.shape[:2], size).astype(bool)

        if len(img1.shape) == 2:
            img1 = skicolor.gray2rgb(img1)

        if len(img2.shape) == 2:
            img2 = skicolor.gray2rgb(img2)

        checkerboard = np.copy(img1)
        checkerboard[np.where(mask)] = img2[np.where(mask)]

        self.scenes[-1].clear()
        self.scenes[-1].addItem(array2qgraphicspixmapitem(checkerboard))

    def update_markers(self, topLeft: QtCore.QModelIndex,
                       bottomRight: QtCore.QModelIndex,
                       roles: Iterable[int]):
        for col in range(topLeft.column(), bottomRight.column() + 1):
            for row in range(topLeft.row(), bottomRight.row() + 1):
                index = self.createIndex(row, col)
                point = self.data(index, role=POINT_ROLE)
                if point:
                    pos = QtCore.QPointF(0.5, 0.5) + point
                    try:
                        self.markers[row, col].setPos(pos)
                    except KeyError:
                        marker = self._marker_1(pos)
                        self.markers[row, col] = marker
                        self.scenes[index.column()].addItem(marker)
                else:
                    try:
                        self.scenes[col].removeItem(self.markers[row, col])
                        del self.markers[row, col]
                    except KeyError:
                        pass

    def _marker_1(self, pos):
        pos = QPointF(int(pos.x()), int(pos.y())) + QPointF(0.5, 0.5)
        marker = self._create_marker_1()
        marker.setPos(pos)
        marker.setZValue(10)
        return marker

    def _create_marker_1(self):
        marker_group = QtWidgets.QGraphicsItemGroup()
        marker_group.addToGroup(QtWidgets.QGraphicsLineItem(0, -3, 0, -2))
        marker_group.addToGroup(QtWidgets.QGraphicsLineItem(0, 2, 0, 3))

        marker_group.addToGroup(QtWidgets.QGraphicsLineItem(-3, 0, -2, 0))
        marker_group.addToGroup(QtWidgets.QGraphicsLineItem(2, 0, 3, 0))

        return marker_group

    def delete_enfacefeature(self, id):
        logger.debug(f"Delete feature with id '{id}'")
        return requests.delete(
            f"{config.api_server}/enfacefeatures/{id}",
            headers=config.auth_header).json()

    def create_enfacefeature(self, data):
        logger.debug(f"Create feature: {data}")
        return requests.post(
            f"{config.api_server}/enfacefeatures/",
            json=data,
            headers=config.auth_header).json()

    def update_enfacfeature(self, data):
        logger.debug(f"Updated feature: {data}")
        return requests.put(
            f"{config.api_server}/enfacefeatures/",
            json=data,
            headers=config.auth_header).json()

    def create_enfacefeaturematch(self, data):
        logger.debug(f"Create EnfaceFeatureMatch: {data}")
        return requests.post(
            f"{config.api_server}/enfacefeaturematches/",
            json=data,
            headers=config.auth_header).json()

    def delete_enfacefeaturematch(self, id):
        logger.debug(f"Delete EnfaceFeatureMatch with id '{id}'")
        return requests.delete(
            f"{config.api_server}/enfacefeaturematches/{id}",
            headers=config.auth_header).json()

    def upload_data(self, index):
        if not self.data(index, POINT_ROLE):
            # Delete feature on server
            self.delete_enfacefeature(self.data(index, FEATUREID_ROLE))
            self._data["enfacefeaturematchs"][index.row()][
                f_dict[index.column()]] \
                = self._new_feature(index.column())

        elif self.data(index, FEATUREID_ROLE) is None:
            # Create feature on server
            feat = self.create_enfacefeature(
                self.data(index, FEATURE_DICT_ROLE))
            self._data["enfacefeaturematchs"][index.row()][
                f_dict[index.column()]] = feat

        else:
            # Update feature on server
            feat = self.update_enfacfeature(self.data(index, FEATURE_DICT_ROLE))
            self._data["enfacefeaturematchs"][index.row()][
                f_dict[index.column()]] = feat

        # Create new complete matches on server
        current_match = self._data["enfacefeaturematchs"][index.row()]
        if self.match_is_complete(index.row()):
            # Create new match in DB
            if current_match["id"] is None:
                match = self.create_enfacefeaturematch(current_match)
                self._data["enfacefeaturematchs"][index.row()] = match
        else:
            if current_match["id"]:
                # Delete Match from DB when id exists but not complete
                self.delete_enfacefeaturematch(current_match["id"])
                # Keep remaining feature
                match = self._new_match()
                if "id" in current_match["feature1"]:
                    match["feature1"] = current_match["feature1"]
                    match["feature2"] = self._new_feature(1)
                    self._data["enfacefeaturematchs"][index.row()] = match
                elif "id" in current_match["feature2"]:
                    match["feature1"] = self._new_feature(0)
                    match["feature2"] = current_match["feature2"]
                    self._data["enfacefeaturematchs"][index.row()] = match

        # Add complete matches to registration
        matches = self._data["enfacefeaturematchs"]
        complete = [m for i, m in enumerate(matches)
                    if self.match_is_complete(i)]
        data = copy.copy(self._data)
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

    def _new_feature(self, n):
        return {"x": None, "y": None, "id": None,
                "enfaceimage_id": self.image_ids[n]}

    def _new_match(self):
        return {"id": None,
                "feature1": self._new_feature(0),
                "feature2": self._new_feature(1),
                "enfaceimage1_id": self.image_ids[0],
                "enfaceimage2_id": self.image_ids[1]
                }

    def new(self):
        data = {"enfaceimage1_id": self.image_ids[0],
                "enfaceimage2_id": self.image_ids[1],
                "similarity": [1, 0, 0, 0, 1, 0, 0, 0, 1],
                "affine": [1, 0, 0, 0, 1, 0, 0, 0, 1],
                "enfacefeaturematchs": [self._new_match()],
                "id": None,
                "created_by": None}
        return data

    def reload_data(self):
        try:
            self._data = get_registration_from_enface_ids(
                self.image_ids[0], self.image_ids[1])
            if self._data["enfacefeaturematchs"] == []:
                self._data["enfacefeaturematchs"].append(self._new_match())
        except ValueError:
            self._data = self.new()

        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount() - 1,
                                               self.columnCount() - 1),
                              (QtCore.Qt.DisplayRole,))

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if self._data is None:
            self.reload_data()
        row, col = (index.row(), index.column())
        if row < 0 or col < 0:
            return False
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

    def removeRows(self, row: int, count: int,
                   parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(row, row + count):
            self.setData(self.index(i, 0), None, role=DELETE_ROLE)
            self.setData(self.index(i, 1), None, role=DELETE_ROLE)
            self.dataChanged.emit(self.index(row, 0),
                                  self.index(row + count - 1, 1))
            del self._data["enfacefeaturematchs"][i]
        self.endRemoveRows()

        # Make sure there is always a match you can add new features to
        if len(self._data["enfacefeaturematchs"]) == 0:
            self.beginInsertRows(parent, 0, 0)
            self._data["enfacefeaturematchs"].append(self._new_match())
            self.endInsertRows()
        return True

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
        self.beginInsertRows(parent, row, row + count - 1)
        self._data["enfacefeaturematchs"].append(self._new_match())
        self.endInsertRows()
        return True

    def rowCount(self, index=None):
        # The length of the outer list.
        try:
            return len(self._data["enfacefeaturematchs"])
        except TypeError:
            self.reload_data()
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
            self.upload_data(index)
            self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole,
                                                 POINT_ROLE))
        elif role == DELETE_ROLE:
            feat["x"], feat["y"] = (None, None)
            self.upload_data(index)
            # Remove row if all None
            self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole,
                                                 POINT_ROLE))
        elif role == FEATUREID_ROLE:
            feat["id"] = value
        elif role == MATCHID_ROLE:
            match["id"] = value
        else:
            return False
        return True
