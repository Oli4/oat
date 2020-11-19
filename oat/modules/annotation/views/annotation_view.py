import logging

import numpy as np
import skimage.transform as skitrans
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget

from oat.models import BscanGraphicsScene, EnfaceGraphicsScene
from oat.models.utils import get_registration_from_enface_ids
from oat.modules.annotation.views.scenetab import SceneTab
from oat.views.ui.ui_annotation_view import Ui_AnnotationView

from oat.models.utils import get_volume_meta_by_id

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
        self.volume_dict = get_volume_meta_by_id(volume_id)
        self.slices = sorted(self.volume_dict["slices"],
                             key=lambda x: x["number"])
        self.bscan_scenes = [BscanGraphicsScene(parent=self, image_id=i["id"],
                                                base_name="BScan")
                             for i in self.slices]
        self.localizer_scene = EnfaceGraphicsScene(parent=self,
                                                   image_id=self.localizer_id,
                                                   base_name="NIR")
        self.enface_scene = EnfaceGraphicsScene(parent=self,
                                                image_id=self.enface_id,
                                                base_name="CFP")
        self.set_enface_tforms()

        # Add scenes to toolbox
        self.enface_scenes = [self.localizer_scene, self.enface_scene]
        self.volume_scenes = [self.bscan_scenes]
        self.enface_views = [self.graphicsViewLocalizer,
                             self.graphicsViewEnface]
        self.volume_views = [self.graphicsViewBscan]

        # Add toolbox enface entries
        for scene in self.enface_scenes:
            self.layerOverview.addTab(SceneTab(self.layerOverview, scene),
                                      scene.name)
        for scenes in self.volume_scenes:
            self.slice_tabs = [SceneTab(self.layerOverview, scenes[x]) for x in scenes]
            self.layerOverview.addTab(self.slice_tabs[0], scenes[0].name)
            #self.layerOverview.setCurrentWidget()

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

    @property
    def current_slice(self):
        return self.volume_views[0].current_slice

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

    def set_scenes(self):
        """ """
        for scene, view in zip(*(self.enface_scenes, self.enface_views)):
            view.setScene(scene)
            view.zoomToFit()
        for scene, view in zip(*(self.volume_scenes, self.volume_views)):
            view.setScene(scene[self.current_slice])
            view.zoomToFit()

    def toogle_scroll_bars(self):
        [view.toggle_scroll_bars() for view in self.graphic_views]

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        try:
            self.key_actions[event.key()]()
        except:
            super().keyPressEvent(event)
