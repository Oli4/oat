from oat.models.layers.base import _BaseLayer

# Line layers
class LineLayer(_BaseLayer):
    def __init__(self, data, name, type='line', editable=True):
        super().__init__(data, name, type, editable)

class RpeLayer(LineLayer):
    def __init__(self, data, name='RPE'):
        super().__init__(data, name)

class BmLayer(LineLayer):
    def __init__(self, data, name='BM'):
        super().__init__(data, name)

class EzLayer(LineLayer):
    def __init__(self, data, name='EZ'):
        super().__init__(data, name)

