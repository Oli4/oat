from PyQt5 import QtCore, Qt

from oat.modules.annotation.views.graphicsview import CustomGraphicsView
from oat.views.ui.ui_volumelocalizer_view import Ui_VolumeLocalizerView

class VolumeLocalizerView(Qt.QWidget, Ui_VolumeLocalizerView):
    cursorPosChanged = QtCore.pyqtSignal(QtCore.QPointF, CustomGraphicsView)

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)
        self.volume_id = None

        self.graphicsViewVolume.cursorPosChanged.connect(self.emit_volume_pos)

        self.graphicsViewLocalizer.cursorPosChanged.connect(self.emit_localizer_pos)

        self._tforms = {}

    def get_data(self, volume_id):
        self.volume_id = volume_id

        self.graphicsViewVolume.get_data(volume_id=volume_id, name="OCT")
        localizer_data = self.graphicsViewVolume.volume_dict["localizer_image"]
        localizer_id = localizer_data["id"]
        self.graphicsViewLocalizer.get_data(image_id=localizer_id, name="NIR")

    def emit_volume_pos(self, pos, sender):
        # The position coming from the volume is in the localizer space.
        # Since other views can only map from the localizer to their space
        # replace the sender here.
        self.cursorPosChanged.emit(pos, self.graphicsViewLocalizer)
        self.graphicsViewLocalizer.set_fake_cursor(pos)

    def emit_localizer_pos(self, pos, sender):
        self.graphicsViewVolume.set_fake_cursor(pos, sender)
        self.cursorPosChanged.emit(pos, sender)


    def set_fake_cursor(self, pos, sender):
        pos = self.graphicsViewLocalizer.map_from_sender(pos, sender)
        self.graphicsViewLocalizer.set_fake_cursor(pos, self.graphicsViewLocalizer)
        self.graphicsViewVolume.set_fake_cursor(pos, self.graphicsViewLocalizer)
