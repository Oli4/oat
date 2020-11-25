import logging

import numpy as np
import skimage.transform as skitrans
from oat.models.utils import get_registration_from_enface_ids
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget

from oat.models import BscanGraphicsScene, EnfaceGraphicsScene

from oat.models.custom.scenetab import SceneTab
from oat.views.ui.ui_annotation_view import Ui_AnnotationView

from oat.models.utils import get_volume_meta_by_id

from oat.modules.tools import tools

logger = logging.getLogger(__name__)


class AnnotationView(QWidget, Ui_AnnotationView):
    def __init__(self, volume_id: int, enface_id: int, parent=None):
        """Initialize the components of the Toolbox subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.tools = tools()
        self.set_tool_buttons()


        # self.collection = get_collection_by_id(collection_id)
        self.volumeWidget.get_data(volume_id)
        self.graphicsViewEnface.get_data(enface_id, name="CFP")


        self.key_actions = {
            # QtCore.Qt.Key_W: self.tableViewPoints.up,
        }



        self.graphic_views = [self.volumeWidget.graphicsViewVolume,
                              self.volumeWidget.graphicsViewLocalizer,
                              self.graphicsViewEnface]
        self.scenes = [view.scene() for view in self.graphic_views]
        self.set_tabs()
        self.volumeWidget.graphicsViewVolume.sceneChanged.connect(self.set_tabs)

        # Connect VolumeLocalizerView to EnfaceView
        self.volumeWidget.cursorPosChanged.connect(
            self.graphicsViewEnface.set_fake_cursor)

        self.graphicsViewEnface.cursorPosChanged.connect(
            self.volumeWidget.set_fake_cursor)

        self._switch_to_tool("inspection")()

    def set_tool_buttons(self):
        for i, (name, tool) in enumerate(self.tools.items()):
            tool.button.setParent(self.toolsWidget)
            self.toolsWidget.layout().addWidget(tool.button, 1,i,1,1)
            tool.button.clicked.connect(self._switch_to_tool(name))

    def _switch_to_tool(self, name):
        def func():
            tool = self.tools[name]
            for n, t in self.tools.items():
                t.button.setChecked(False)
            tool.button.setChecked(True)

            # Show tool options
            tool.options_widget.setParent(self.toolboxWidget)
            self.toolboxWidget.layout().replaceWidget(self.optionsWidget, tool.options_widget)
            self.optionsWidget = tool.options_widget

            # Set the tool and preview
            for view in self.graphic_views:
                view.set_tool(tool)
                view.scene().tool_preview = tool.paint_preview
                view.scene().addItem(tool.paint_preview)
        return func

    def set_tabs(self, scene=None):
        # Todo: this is highly inefficient
        index = self.layerOverview.currentIndex()
        self.layerOverview.clear()
        if not scene is None:
            self.scenes[0] = scene
        for scene in self.scenes:
            self.layerOverview.addTab(scene.scene_tab, scene.name)
        self.layerOverview.setCurrentIndex(index)
        self.layerOverview.currentChanged.connect(
            lambda index: self.layerOverview.widget(index).scene.setFocus() if index != -1 else None)

        self.layerOverview.repaint()

    def uncheck_buttons(self):
        for button in [self.penButton, self.navigationButton]:
            button.setChecked(False)

    def toogle_scroll_bars(self):
        [view.toggle_scroll_bars() for view in self.graphic_views]

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        try:
            self.key_actions[event.key()]()
        except:
            super().keyPressEvent(event)
