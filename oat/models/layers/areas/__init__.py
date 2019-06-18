from oat.models.layers.base import _BaseLayer

# Area layers
class AreaLayer(_BaseLayer):
    def __init__(self, data, name, type='area', editable=True):
        super().__init__(data, name, type, editable)

class DrusenLayer(AreaLayer):
    def __init__(self, data, name='Drusen'):
        super().__init__(data, name)

class HrfLayer(AreaLayer):
    def __init__(self, data, name='HRF'):
        super().__init__(data, name)