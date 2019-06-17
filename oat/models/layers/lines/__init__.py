from oat.models.layers.base import _base_layer

# Line layers
class line_layer(_base_layer):
    def __init__(self, data, name, type='line', editable=True):
        super().__init__(data, name, type, editable)

class rpe_layer(line_layer):
    def __init__(self, data, name='RPE'):
        super().__init__(data, name)

class bm_layer(line_layer):
    def __init__(self, data, name='BM'):
        super().__init__(data, name)

