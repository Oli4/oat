from oat.models.layers.base import _BaseLayer, _Layer3D, _Layer2D
from oat.io import get_cfp
from PyQt5 import QtGui, QtWidgets
import qimage2ndarray

class ImageLayer3D(_Layer3D):
    """ A class to hold image layers which can not be manipulated by the user.
    For example the original data.

    """
    def __init__(self, data, name, type='image', editable=False):
        super().__init__(data, name, type, editable)

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
    def __init__(self, data, name, type='image', editable=False):
        super().__init__(data, name, type, editable)

    @_BaseLayer.editable.setter
    def editable(self, value):
        raise ValueError("The 'editable' status of the image layer can not be changed.")

    def load(self):
        pass

    def save(self):
        pass



class OctLayer(ImageLayer3D):
    def __init__(self, data, name='OCT'):
        super().__init__(data, name)

class NirLayer(ImageLayer2D):
    def __init__(self, data, name='NIR'):
        super().__init__(data, name)

class CfpLayer(ImageLayer2D):
    def __init__(self, data, name='CFP'):
        super().__init__(data, name)

    @classmethod
    def import_cfp(cls, filepath):
        return cls(get_cfp(filepath))