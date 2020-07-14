import logging

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget

from oat.models.custom_scene import BscanGraphicsScene, EnfaceGraphicsScene
from oat.views.ui.ui_annotation_view import Ui_AnnotationView

logger = logging.getLogger(__name__)


class AnnotationView(QWidget, Ui_AnnotationView):
    def __init__(self, collection_id: int, parent=None):
        """Initialize the components of the Toolbox subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        # self.collection = get_collection_by_id(collection_id)
        volume_id = 1
        localizer_id = 2
        enface_id = 3

        self.key_actions = {
            # QtCore.Qt.Key_W: self.tableViewPoints.up,
        }

        # Create scenes
        self.bscan_scene = BscanGraphicsScene(parent=self, image_id=volume_id)
        self.localizer_scene = EnfaceGraphicsScene(parent=self,
                                                   image_id=localizer_id)
        self.enface_scene = EnfaceGraphicsScene(parent=self, image_id=enface_id)

        self.scenes = [self.bscan_scene, self.localizer_scene,
                       self.enface_scene]
        self.graphic_views = [self.graphicsViewBscan,
                              self.graphicsViewLocalizer,
                              self.graphicsViewEnface]

        self.graphicsViewBscan.localizerPosChanged.connect(
            self.graphicsViewLocalizer.set_cursor)
        self.graphicsViewEnface.localizerPosChanged.connect(
            self.graphicsViewLocalizer.set_cursor)
        self.graphicsViewLocalizer.localizerPosChanged.connect(
            self.graphicsViewEnface.set_cursor_from_localizer)
        self.graphicsViewLocalizer.localizerPosChanged.connect(
            self.graphicsViewBscan.set_cursor_from_localizer)

        # x position from x position in B-Scan
        # y position from Bscan number

        # Set scenes
        self.set_scenes()
        self.toggle_cursor_crosses()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        # Make sure images are filling the view when Widget is opened
        [view.zoomToFit() for view in self.graphic_views]

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        [view.zoomToFit() for view in self.graphic_views]

    def center_PointSelection(self, point):
        if point:
            self.graphicsViewPointSelection.zoomToFeature()
            self.graphicsViewPointSelection.centerOn(point)
        else:
            self.graphicsViewPointSelection.zoomToFit()

    def center_Patch(self, point):
        if point:
            self.graphicsViewPatch.zoomToFeature()
            self.graphicsViewPatch.centerOn(point)
        else:
            self.graphicsViewPatch.zoomToFit()

    def set_scenes(self):
        """ """
        for i, view in enumerate(self.graphic_views):
            view.setScene(self.scenes[i])
            view.zoomToFit()

    def toggle_cursor_crosses(self):
        [view.toggle_cursor_cross() for view in self.graphic_views]

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        try:
            self.key_actions[event.key()]()
        except:
            super().keyPressEvent(event)
