import numpy as np
from PyQt5.QtCore import pyqtSignal


class _BaseLayer(object):
    def __init__(self, data, name, type=None, editable=None, dimension=None,):
        self._name = name
        self._data = data
        self._type = type
        self._editable = editable
        self._dimension = dimension
        self._opacity = 100
        self._visible = True

        self._shape = None
        self._position = None
        self._save_path = ''
        self._parent_layer = None

        self.name_changed = pyqtSignal(str)
        self.data_changed = pyqtSignal(np.ndarray)
        self.opacity_changed = pyqtSignal(int)
        self.visible_changed = pyqtSignal(bool)
        self.editable_changed = pyqtSignal(bool)
        self.shape_changed = pyqtSignal(tuple)
        self.position_changed = pyqtSignal(tuple)
        self.save_path_changed = pyqtSignal(str)

    # Property getters
    @property
    def name(self):
        return self._name

    @property
    def data(self):
        return self._data

    @property
    def opacity(self):
        return self._opacity

    @property
    def visible(self):
        return self._visible

    @property
    def editable(self):
        return self._editable

    @property
    def shape(self):
        return self._shape

    @property
    def position(self):
        return self._position

    @property
    def save_path(self):
        return self._save_path

    @property
    def parent_layer(self):
        return self._parent_layer

    @property
    def dimension(self):
        return self._dimension

    # Property setters
    @name.setter
    def name(self, value):
        if type(value) is not str or len(value) > 20:
            raise ValueError("'name' needs to be a string of length < 20 characters")
        self._name = value
        self.name_changed.emit(value)

    @data.setter
    def data(self, value):
        if type(value) is not np.ndarray:
            raise ValueError("'data' needs to be of type 'np.ndarray' "
                             "but it is of type {}".format(type(value)))
        self._data = value
        self._shape = self._data.shape
        self.data_changed.emit(value)

    @opacity.setter
    def opacity(self, value):
        if value > 100 or value < 0:
            raise ValueError("'opacity' can only have values between 0 and 100."
                             " You tried setting it to {}".format(value))
        self._opacity = value
        self.opacity_changed.emit(value)

    @visible.setter
    def visible(self, value):
        if value not in [True, False]:
            raise ValueError("'visible' can only be True or False."
                             " You tried setting it to {}".format(value))
        self._visible = value
        self.visible_changed.emit(value)

    @editable.setter
    def editable(self, value):
        if value not in [True, False]:
            raise ValueError("'editable' can only be True or False."
                             " You tried setting it to {}".format(value))
        self._editable = value
        self.editable_changed.emit(value)

    @position.setter
    def position(self, value):
        # Tell registered layers that the position changed
        self._position = value
        self.position_changed.emit(value)

    @save_path.setter
    def save_path(self, value):
        self._save_path = value
        self.save_path_changed.emit(value)

    @parent_layer.setter
    def parent_layer(self, value):
        raise ValueError("The 'parent_layer' status of a layer can not be changed.")

    @dimension.setter
    def dimension(self, value):
        raise ValueError("The 'dimension' status of a layer can not be changed.")

class _Layer3D(_BaseLayer):
    def __init__(self, data, name, type=None, editable=None, dimension=3):
        super().__init__(data, name, type, editable, dimension)

class _Layer2D(_BaseLayer):
    def __init__(self, data, name, type=None, editable=None, dimension=2):
        super().__init__(data, name, type, editable, dimension)
