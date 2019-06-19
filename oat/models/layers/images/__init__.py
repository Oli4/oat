from oat.models.layers.base import _BaseLayer, _Layer3D, _Layer2D
from oat.io import get_vol_header, get_bscan_images, get_slo_image

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

    @classmethod
    def import_vol(cls, filepath):
        b_hdrs, b_seglines, b_scans = get_bscan_images(filepath, improve_constrast='hist_match')
        return cls(b_scans)


class NirLayer(ImageLayer2D):
    def __init__(self, data, name='NIR'):
        super().__init__(data, name)

    @classmethod
    def import_vol(cls, filepath):
        # SLO is Scanning Laser Ophthalmoskopie -> NIR
        slo = get_slo_image(filepath)
        return cls(slo)

class CfpLayer(ImageLayer2D):
    def __init__(self, data, name='CFP'):
        super().__init__(data, name)