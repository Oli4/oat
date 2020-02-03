from oat.models.layers.base import _BaseLayer, _Layer3D, _Layer2D
from oat.io import get_cfp
from PyQt5 import QtGui, QtWidgets
import qimage2ndarray

class ImageLayer3D(_Layer3D):
    """ A class to hold image layers which can not be manipulated by the user.
    For example the original data.

    """
    def __init__(self, data, name):
        super().__init__(data, name, type='image', editable=False)

    @_BaseLayer.editable.setter
    def editable(self, value):
        raise ValueError("The 'editable' status of the image layer can not be changed.")

    def load(self):
        pass

    def save(self):
        pass

class ImageLayer2D(_Layer2D):
    """ A class to hold image layers which can not be manipulated by the user.
    For example the original data.

    """
    def __init__(self, data, name):
        super().__init__(data, name, type='image', editable=False)

    @_BaseLayer.editable.setter
    def editable(self, value):
        raise ValueError("The 'editable' status of the image layer can not be changed.")

    def load(self):
        pass

    def save(self):
        pass


class OctLayer(ImageLayer3D):
    def __init__(self, data, meta, bscan_meta):
        super().__init__(data, name='OCT')
        self._meta = meta
        self._bscan_meta = bscan_meta

    @property
    def slice_positions(self):
        return [((x["StartX"], x["StartY"]), (x["EndX"], x["EndY"]))
                for x in self._bscan_meta]

    @property
    def x_scaling(self):
        return self._meta["ScaleX"]

    @property
    def y_scaling(self):
        return self._meta["ScaleY"]

    @property
    def z_scaling(self):
        return self._meta["ScaleZ"]

class NirLayer(ImageLayer2D):
    def __init__(self, data):
        super().__init__(data, name='NIR')

class CfpLayer(ImageLayer2D):
    def __init__(self, data):
        super().__init__(data, name='CFP')

    @classmethod
    def import_cfp(cls, filepath):
        return cls(get_cfp(filepath))