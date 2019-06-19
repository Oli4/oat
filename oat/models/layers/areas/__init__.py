from oat.models.layers.base import _Layer3D, _Layer2D

# Area layers
class AreaLayer3D(_Layer3D):
    def __init__(self, data, name, type='area', editable=True):
        super().__init__(data, name, type, editable)

class DrusenLayer3D(AreaLayer3D):
    def __init__(self, data, name='Drusen'):
        super().__init__(data, name)

class HrfLayer3D(AreaLayer3D):
    def __init__(self, data, name='HRF'):
        super().__init__(data, name)

# 2D Layer
class AreaLayer2D(_Layer2D):
    def __init__(self, data, name, type='area', editable=True):
        super().__init__(data, name, type, editable)

class DrusenLayer2D(AreaLayer2D):
    def __init__(self, data, name='Drusen'):
        super().__init__(data, name)

class HrfLayer2D(AreaLayer2D):
    def __init__(self, data, name='HRF'):
        super().__init__(data, name)