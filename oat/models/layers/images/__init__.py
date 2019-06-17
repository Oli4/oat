from oat.models.layers.base import _base_layer

class image_layer(_base_layer):
    """ A class to hold image layers which can not be manipulated by the user.
    For example the original data.

    """
    def __init__(self, data, name, type='image', editable=False):
        super().__init__(data, name, type, editable)

    @_base_layer.editable.setter
    def editable(self, value):
        raise ValueError("The 'editable' status of the image layer can not be changed.")

    def load(self):
        pass

    def save(self):
        pass



class oct_layer(image_layer):
    def __init__(self, data, name='OCT'):
        super().__init__(data, name)

class nir_layer(image_layer):
    def __init__(self, data, name='NIR'):
        super().__init__(data, name)

class cfp_layer(image_layer):
    def __init__(self, data, name='CFP'):
        super().__init__(data, name)