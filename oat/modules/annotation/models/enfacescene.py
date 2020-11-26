from typing import Tuple, Dict

from PyQt5.QtWidgets import QGraphicsPixmapItem
from skimage import transform as skitrans

from oat.modules.annotation.models.scene import CustomGrahpicsScene
from oat.models.utils import get_enface_by_id, array2qgraphicspixmapitem

class EnfaceGraphicsScene(CustomGrahpicsScene):
    def __init__(self, parent, data, base_name="Enface", *args,
                 **kwargs):
        self.data = data
        self.base_name = base_name
        self.urlprefix = "enface"
        super().__init__(*args, **kwargs, parent=parent, image_id=data["id"])

    def _fetch_image(self, image_id) -> Tuple[QGraphicsPixmapItem, Dict]:
        img, meta = get_enface_by_id(image_id)
        return array2qgraphicspixmapitem(img), meta

    @property
    def tform(self):
        if self._tform is None:
            raise AttributeError("tform has not been set.")
        else:
            return self._tform

    @tform.setter
    def tform(self, value: skitrans.ProjectiveTransform):
        self._tform = value
