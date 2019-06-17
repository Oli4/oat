from oat.models.layers.base import _base_layer

# Area layers
class area_layer(_base_layer):
    def __init__(self, data, name, type='area', editable=True):
        super().__init__(data, name, type, editable)

class drusen_layer(area_layer):
    def __init__(self, data, name='Drusen'):
        super().__init__(data, name)

class hrf_layer(area_layer):
    def __init__(self, data, name='HRF'):
        super().__init__(data, name)