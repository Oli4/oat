from typing import Tuple, Dict

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

from .utils import get_enface_by_id, get_bscan_by_id, get_volume_meta_by_id


class CustomGrahpicsScene(QGraphicsScene):
    def __init__(self, parent, image_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)

        self.image = None
        self.image_meta = None

        if image_id:
            self.add_image(image_id)

    def _fetch_image(self, image_id) -> Tuple[QGraphicsPixmapItem, Dict]:
        raise NotImplementedError

    def add_image(self, image_id):
        # if image not in scene, fetch and add
        pixmap, meta = self._fetch_image(image_id)
        if not pixmap in self.items():
            self.addItem(pixmap)
        # else, bring image to the front


class BscanGraphicsScene(CustomGrahpicsScene):
    def __init__(self, parent, image_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent)

        # Fetch Volume image
        self.volume_dict = get_volume_meta_by_id(image_id)
        # Make sure slices are correctly ordered
        self.slices = sorted(self.volume_dict["slices"],
                             key=lambda x: x["number"])

        # Set Scene to first B-Scan
        self.current_slice = 0
        self.add_image(self.slices[self.current_slice]["id"])

        # Asynchronously load remaining B-Scans

    def _fetch_image(self, image_id) -> Tuple[QGraphicsPixmapItem, Dict]:
        return get_bscan_by_id(image_id)

    def next_slice(self):
        if self.current_slice + 1 < len(self.slices):
            previous_pixmap, _ = \
                self._fetch_image(self.slices[self.current_slice]["id"])
            self.current_slice += 1
            pixmap, _ = \
                self._fetch_image(self.slices[self.current_slice]["id"])
            previous_pixmap.setZValue(0)
            pixmap.setZValue(1)
            if pixmap not in self.items():
                self.addItem(pixmap)

    def set_slice(self, number):
        if 0 <= number < len(self.slices):
            previous_pixmap, _ = \
                self._fetch_image(self.slices[self.current_slice]["id"])
            self.current_slice = number
            pixmap, _ = \
                self._fetch_image(self.slices[self.current_slice]["id"])
            previous_pixmap.setZValue(0)
            pixmap.setZValue(1)
            if pixmap not in self.items():
                self.addItem(pixmap)

    def last_slice(self):
        if self.current_slice - 1 >= 0:
            previous_pixmap, _ = \
                self._fetch_image(self.slices[self.current_slice]["id"])
            self.current_slice -= 1
            pixmap, _ = \
                self._fetch_image(self.slices[self.current_slice]["id"])
            previous_pixmap.setZValue(0)
            pixmap.setZValue(1)
            if pixmap not in self.items():
                self.addItem(pixmap)


class EnfaceGraphicsScene(CustomGrahpicsScene):
    def __init__(self, parent, image_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs, parent=parent, image_id=image_id)

    def _fetch_image(self, image_id) -> Tuple[QGraphicsPixmapItem, Dict]:
        return get_enface_by_id(image_id)
