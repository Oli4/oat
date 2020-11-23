from typing import Tuple, Dict

import numpy as np
from PyQt5 import QtGui, Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem

from oat.models.custom.scene import CustomGrahpicsScene
from oat.models.utils import get_bscan_by_id, array2qgraphicspixmapitem

class BscanGraphicsScene(CustomGrahpicsScene):
    def __init__(self, parent, data, base_name="OCT", *args, **kwargs):
        self.data = data
        self.base_name = base_name
        self.urlprefix = "slice"
        super().__init__(*args, **kwargs, parent=parent, image_id=data["id"])

        # Set Scene to first B-Scan

        self.fake_cursor = self.addPixmap(
            QtGui.QPixmap(":/cursors/cursors/navigation_cursor.svg"))
        self.fake_cursor.setFlag(Qt.QGraphicsItem.ItemIgnoresTransformations)
        self.fake_cursor.hide()

    def _fetch_image(self, image_id) -> Tuple[QGraphicsPixmapItem, Dict]:
        img, meta = get_bscan_by_id(image_id)
        return array2qgraphicspixmapitem(img), meta
