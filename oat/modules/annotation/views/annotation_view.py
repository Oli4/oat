import logging

import numpy as np
import skimage.transform as skitrans
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget

from oat.models import BscanGraphicsScene, EnfaceGraphicsScene
from oat.models.utils import get_registration_from_enface_ids
from oat.modules.annotation.views.scenetab import SceneTab
from oat.views.ui.ui_annotation_view import Ui_AnnotationView

logger = logging.getLogger(__name__)


class AnnotationView(QWidget, Ui_AnnotationView):
    def __init__(self, volume_id: int, localizer_id: int, enface_id: int, parent=None):
        """Initialize the components of the Toolbox subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.active_tool = "navigation"

        # self.collection = get_collection_by_id(collection_id)
        self.volume_id = volume_id
        self.localizer_id = localizer_id
        self.enface_id = enface_id

        self.key_actions = {
            # QtCore.Qt.Key_W: self.tableViewPoints.up,
        }

        # Create scenes
        self.bscan_scene = BscanGraphicsScene(parent=self,
                                              image_id=self.volume_id,
                                              base_name="OCT")
        self.localizer_scene = EnfaceGraphicsScene(parent=self,
                                                   image_id=self.localizer_id,
                                                   base_name="NIR")
        self.enface_scene = EnfaceGraphicsScene(parent=self,
                                                image_id=self.enface_id,
                                                base_name="CFP")
        self.set_enface_tforms()

        # Add scenes to toolbox

        self.scenes = [self.bscan_scene, self.localizer_scene,
                       self.enface_scene]
        self.graphic_views = [self.graphicsViewBscan,
                              self.graphicsViewLocalizer,
                              self.graphicsViewEnface]

        # Add toolbox entries
        for scene in self.scenes:
            self.layerOverview.addTab(SceneTab(self.layerOverview, scene),
                                      scene.name)

        # Set Localizer from Bscan
        self.graphicsViewBscan.volumePosChanged.connect(
            self.graphicsViewLocalizer.set_fake_cursor)

        # Set Localizer from enface
        self.graphicsViewEnface.enfacePosChanged.connect(
            self.graphicsViewLocalizer.set_fake_cursor)

        # set enface from localizer
        self.graphicsViewLocalizer.localizerPosChanged.connect(
            self.graphicsViewEnface.set_fake_cursor)

        # set bscan from localizer
        self.graphicsViewLocalizer.localizerPosChanged.connect(
            self.graphicsViewBscan.set_fake_cursor)

        # Set scenes
        self.set_scenes()

        self.penButton.clicked.connect(self.switch_to_pen)
        self.navigationButton.clicked.connect(self.switch_to_navigation)
        self.switch_to_navigation()

    def switch_to_pen(self):
        self.uncheck_buttons()
        self.penButton.setChecked(True)
        self.active_tool = "pen"
        for view in self.graphic_views:
            view.set_active_tool("pen")

    def switch_to_navigation(self):
        self.uncheck_buttons()
        self.navigationButton.setChecked(True)
        self.active_tool = "navigation"
        for view in self.graphic_views:
            view.set_active_tool("navigation")

    def uncheck_buttons(self):
        for button in [self.penButton, self.navigationButton]:
            button.setChecked(False)

    def set_enface_tforms(self):
        registration_data = get_registration_from_enface_ids(
            self.localizer_id, self.enface_id)

        # Todo: Use QTransform here for faster transformations?
        tmodel = "similarity"
        matrix = np.array(registration_data[tmodel]).reshape((3, 3))
        self.enface_scene.tform = skitrans.ProjectiveTransform(matrix)

    # def center_PointSelection(self, point):
    #    if point:
    #        self.graphicsViewPointSelection.zoomToFeature()
    #        self.graphicsViewPointSelection.centerOn(point)
    #    else:
    #        self.graphicsViewPointSelection.zoomToFit()

    # def center_Patch(self, point):
    #    if point:
    # #       self.graphicsViewPatch.zoomToFeature()
    #        self.graphicsViewPatch.centerOn(point)
    #    else:
    #        self.graphicsViewPatch.zoomToFit()

    def set_scenes(self):
        """ """
        for i, view in enumerate(self.graphic_views):
            view.setScene(self.scenes[i])
            view.zoomToFit()

    def toogle_scroll_bars(self):
        [view.toggle_scroll_bars() for view in self.graphic_views]

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        try:
            self.key_actions[event.key()]()
        except:
            super().keyPressEvent(event)
