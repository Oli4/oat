from oat.models.layers.base import _Layer2D, _Layer3D

# Line layers
class LineLayer2D(_Layer2D):
    def __init__(self, data, name, type='line', editable=True):
        super().__init__(data, name, type, editable)

class LineLayer3D(_Layer3D):
    def __init__(self, data, name, type='line', editable=True):
        super().__init__(data, name, type, editable)


class RpeLayer(LineLayer3D):
    def __init__(self, data, name='RPE'):
        super().__init__(data, name)

class BmLayer(LineLayer3D):
    def __init__(self, data, name='BM'):
        super().__init__(data, name)

class EzLayer(LineLayer3D):
    def __init__(self, data, name='EZ'):
        super().__init__(data, name)

