import io
from datetime import datetime
from typing import Optional

import imageio
import itertools
import pandas as pd
import qimage2ndarray
import requests
from PyQt5 import QtCore
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QPoint, QPointF, QModelIndex
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem
from pydantic import BaseModel

from oat import config
from oat.models.config import FEATUREID_ROLE, MATCHID_ROLE


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
        print(response.headers)
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
    markerChanged = QtCore.pyqtSignal(QModelIndex)
    markersChanged = QtCore.pyqtSignal()

    def __init__(self, *args):
        super().__init__()

        self.image_ids = args
        self.images, self.images_meta = zip(*[get_enface_by_id(i)
                                              for i in self.image_ids])

        self.scenes = [SceneModel(self, scene_id=i)
                       for i in range(len(self.image_ids))]
        for i, scene in enumerate(self.scenes):
            scene.addItem(self.array2qgraphicspixmapitem(self.images[i]))

        self._data = None
        self.markers = {}

        self.markerChanged.connect(self.set_marker)
        self.markersChanged.connect(self.set_markers_from_model)

        self.reload_data()

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
        try:
            self.markers[(index.row(), index.column())].setPos(pos)
        except KeyError:
            marker = self._marker_1(pos)
            self.markers[(index.row(), index.column())] = marker
            self.scenes[index.column()].addItem(marker)
        # self.markers[(scene_id, row)] = self._marker_1(pos)

        self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole,))

    def _get_marker_pos(self, index):
        try:
            point = self.data(index, role=QtCore.Qt.EditRole)
            return QtCore.QPointF(0.5, 0.5) + point
        except:
            # If no marker set
            raise ValueError()

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

    def update_markers(self):
        pass

    def array2qgraphicspixmapitem(self, image):
        return QtWidgets.QGraphicsPixmapItem(
            QtGui.QPixmap().fromImage(qimage2ndarray.array2qimage(image)))

    def _from_json(self, json_data):
        ''' Parse variable number of related features from json response to a
        pandas.DataFrame
        '''
        data = json_data["enfacefeaturematchs"]

        d_id = pd.DataFrame.from_records([x["id"] for x in data])
        dfs = [d_id]
        for i, _ in enumerate(self.images_ids):
            df = pd.DataFrame.from_records([x[f"feature{i}"] for x in data])
            df.rename(columns={"id": f"img{i}_id", "x": f"x{i}", "y": f"y{i}"},
                      inplace=True)
            dfs.append(df)

        data = pd.concat(dfs, axis=1)
        for i, _ in enumerate(self.image_ids):
            data[f"Image {i}"] = list(zip(data.loc[:, f"x{i + 1}"],
                                          data.loc[:, f"y{i + 1}"]))
            data.drop(f"x{i + 1}")
            data.drop(f"y{i + 1}")
        return data

    def _to_json(self):
        {
            "enfaceimage1_id": {self.image1_id},
            "enfaceimage2_id": {self.image2_id},
            "similarity": [
                0
            ],
            "affine": [
                0
            ],
            "enfacefeaturematchs": [
                {
                    "feature1": {
                        "x": 0,
                        "y": 0
                    },
                    "feature2": {
                        "x": 0,
                        "y": 0
                    }
                }
            ]
        }

    def upload_data(self):
        response = requests.post(f"{config.api_server}/registration/",
                                 json=self._to_json(),
                                 headers=config.auth_header)

        data = self._from_json(response.json())
        self._data = data
        self.layoutChanged.emit()

    def reload_data(self):
        response = requests.get(
            f"{config.api_server}/registration/"
            f"?enfaceimage1_id={self.image_ids[0]}"
            f"&enfaceimage2_id={self.image_ids[1]}",
            headers=config.auth_header)
        print(response.json())
        if response.status_code == 200:
            data = self._from_json(response.json())
        else:
            data = self.new_registration_data()

        if data.eq(self._data).all(axis=None):
            pass
        else:
            self._data = data
            self.dataChanged.emit(self.createIndex(0, 0),
                                  self.createIndex(self.rowCount(),
                                                   self.columnCount()),
                                  (QtCore.Qt.DisplayRole,))
            self.markersChanged.emit()

    def _flatten_list(self, nested_list):
        return list(itertools.chain.from_iterable(nested_list))

    def new_registration_data(self, ):
        feat = [[f"img{i}_id", f"Image {i}"] for i, _ in
                enumerate(self.image_ids)]
        columns = ["id"] + self._flatten_list(feat) + \
                  [f"Image {i}" for i, _ in enumerate(self.image_ids)]
        dtypes = ['object' for _ in enumerate(columns)]

        data = [None, ] + \
               self._flatten_list(
                   [[img_id, (None, None)] for img_id in self.image_ids])

        df = pd.DataFrame({name: pd.Series([d], dtype=dtype)
                           for name, dtype, d in zip(columns, dtypes, data)})
        return df

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return str(self._data.iloc[index.row(), (1 + index.column()) * 2])
        elif role == QtCore.Qt.EditRole:
            return QPoint(
                *self._data.iloc[index.row(), (1 + index.column()) * 2])
        elif role == FEATUREID_ROLE:
            return self._data.iloc[index.row(), 1 + index.column() * 2]
        elif role == MATCHID_ROLE:
            return self._data.iloc[index.row(), 0]

    def insertRows(self, row: int, count: int,
                   parent: QModelIndex = ...) -> bool:
        if row != self.rowCount() or count != 1:
            return False
        self.beginInsertRows(parent, row, row)
        self._data = self._data.append(self.new_registration_data())
        self.endInsertRows()
        return True

    def rowCount(self, index=None):
        # The length of the outer list.
        return self._data.shape[0]

    def columnCount(self, index=None):
        return int((self._data.shape[1] - 1) / 2)

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self._data.columns[(1 + section) * 2])

            if orientation == QtCore.Qt.Vertical:
                return str(self._data.index[section])

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        # flags |= QtCore.Qt.ItemIsEditable
        # flags |= QtCore.Qt.ItemIsSelectable
        flags |= QtCore.Qt.ItemIsEnabled
        # flags |= QtCore.Qt.ItemIsDragEnabled
        # flags |= QtCore.Qt.ItemIsDropEnabled
        return flags

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        try:
            self.layoutAboutToBeChanged.emit()
            self._data.sort_values(self._data.columns[Ncol],
                                   ascending=not order, inplace=True)
            self.layoutChanged.emit()
        except Exception as e:
            print(e)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return False

        row = index.row()
        col = index.column()
        if role == QtCore.Qt.EditRole:
            self._data.iloc[row, (col + 1) * 2] = (value.x(), value.y())
            self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole,))
            self.markerChanged.emit(index)
        elif role == FEATUREID_ROLE:
            self._data.iloc[row, 2 + col * 2] = value
        elif role == MATCHID_ROLE:
            self._data.iloc[row, 0] = value
        else:
            return False
        return True

    def setMarker(self, scene_id: int, point: QtCore.QPoint,
                  row: Optional[int] = None):
        if row is None:
            row = self.rowCount() - 1
        x_col = self.scene_columns[scene_id][0]
        y_col = self.scene_columns[scene_id][1]
        index_x = self.createIndex(row, x_col)
        index_y = self.createIndex(row, y_col)

        if index_x.isValid() and index_y.isValid():
            x_val, y_val = point.x(), point.y()

            self._data.iloc[row, x_col] = x_val
            self._data.iloc[row, y_col] = y_val

            col = self._data.columns.get_loc(f"Image {scene_id}")

            self._data.iloc[row, col] = (self._data.iloc[row, x_col],
                                         self._data.iloc[row, y_col])

            self.markerChanged.emit(row, scene_id)
            return True
        return False
