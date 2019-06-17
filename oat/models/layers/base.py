import numpy as np

class _base_layer(object):
    def __init__(self, data, name, type=None, editable=None):
        self._name = name
        self._data = data
        self._type = type
        self._editable = editable
        self._opacity = 100
        self._visible = True

        self._shape = None
        self._position = None
        self._save_path = ''
        self._parent_layer = None

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



    # Property setters
    @name.setter
    def name(self, value):
        if type(value) is not str or len(value) > 20:
            raise ValueError("'name' needs to be a string of length < 20 characters")
        self._name = value

    @data.setter
    def data(self, value):
        if type(value) is not np.ndarray:
            raise ValueError("'data' needs to be of type 'np.ndarray' "
                             "but it is of type {}".format(type(value)))
        self._data = value
        self._shape = self._data.shape

    @opacity.setter
    def opacity(self, value):
        if value > 100 or value < 0:
            raise ValueError("'opacity' can only have values between 0 and 100."
                             " You tried setting it to {}".format(value))
        self._opacity = value

    @visible.setter
    def visible(self, value):
        if value not in [True, False]:
            raise ValueError("'visible' can only be True or False."
                             " You tried setting it to {}".format(value))
        self._visible = value

    @editable.setter
    def editable(self, value):
        if value not in [True, False]:
            raise ValueError("'editable' can only be True or False."
                             " You tried setting it to {}".format(value))
        self._editable = value

    @position.setter
    def position(self, value):
        # Tell registered layers that the position changed
        self._position = value

    @save_path.setter
    def save_path(self, value):
        # Tell registered layers that the position changed
        self._save_path = value

    @parent_layer.setter
    def parent_layer(self, value):
        # Tell registered layers that the position changed
        self._parent_layer = value
