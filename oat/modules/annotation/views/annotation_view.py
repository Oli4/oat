import logging
from typing import List

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget

from oat.views.ui.ui_annotation_view import Ui_AnnotationView

from oat.modules.annotation.tools import tools
from oat.modules.annotation.views.volume_localizer_view import VolumeLocalizerView
from oat.modules.annotation.views.volume_view import VolumeView
from oat.modules.annotation.views.enface_view import EnfaceView

from oat.modules.annotation.models.treeview.areaitem import TreeAreaItem
from oat.modules.annotation.models.treeview.lineitem import TreeLineItem

logger = logging.getLogger(__name__)


class AnnotationView(QWidget, Ui_AnnotationView):
    def __init__(self, volume_ids_with_localizer: List[int],
                 volume_ids_without_localizer: List[int],
                 other_enface_ids: List[int], parent=None):
        """Initialize the components of the Toolbox subwindow."""
        super().__init__(parent)
        self.setupUi(self)

        self.tools = tools()
        self.set_tool_buttons()


        # self.collection = get_collection_by_id(collection_id)
        self.volume_widgets = []
        self.enface_views = []
        self.volume_views = []

        self.volume_ids_with_localizer = volume_ids_with_localizer
        self.volume_ids_without_localizer = volume_ids_without_localizer
        self.other_enface_ids = other_enface_ids

        self.add_volumelocalizer_widgets()
        self.add_volume_views()
        self.add_enface_views()

        self.key_actions = {
            QtCore.Qt.Key_Alt: self.toggle_linked_navigation
            # QtCore.Qt.Key_W: self.tableViewPoints.up,
        }

        self.graphic_views = (
                self.enface_views + self.volume_views +
                [vw.graphicsViewVolume for vw in self.volume_widgets] +
                [vw.graphicsViewLocalizer for vw in self.volume_widgets])

        self.set_tabs()

        # Connect all VolumeLocalizerViews to all EnfaceViews
        # Volume views can not be connected since the connection uses the localizer
        # In future a localizer can be produced by projecting the volume.
        for volume_widget in self.volume_widgets:
            volume_widget.graphicsViewVolume.sceneChanged.connect(self.set_tabs)
            for enface_view in self.enface_views:
                volume_widget.cursorPosChanged.connect(enface_view.set_fake_cursor)
                enface_view.cursorPosChanged.connect(volume_widget.set_fake_cursor)

        for enface_view in self.enface_views:
            for enface_view2 in self.enface_views:
                if not enface_view is enface_view2:
                    enface_view.cursorPosChanged.connect(enface_view2.set_fake_cursor)
                    enface_view2.cursorPosChanged.connect(enface_view.set_fake_cursor)

        for volume_widget in self.volume_widgets:
            for volume_widget2 in self.volume_widgets:
                if not volume_widget is volume_widget2:
                    volume_widget.cursorPosChanged.connect(volume_widget2.set_fake_cursor)
                    volume_widget2.cursorPosChanged.connect(volume_widget.set_fake_cursor)

        self._switch_to_tool("inspection")()
        self.linked_navigation = False

    @property
    def scenes(self):
        return [view.scene() for view in self.graphic_views]

    def add_volumelocalizer_widgets(self):
        for volume_id in self.volume_ids_with_localizer:
            volume_widget = VolumeLocalizerView(parent=self.data_widget)
            volume_widget.get_data(volume_id)
            self.volume_widgets.append(volume_widget)

            self.data_widget.layout().addWidget(volume_widget)

    def add_volume_views(self):
        for volume_id in self.volume_ids_without_localizer:
            volume_view = VolumeView(parent=self.data_widget)
            volume_view.get_data(volume_id)

            sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.MinimumExpanding,
                QtWidgets.QSizePolicy.MinimumExpanding)
            sizePolicy.setHorizontalStretch(5)
            sizePolicy.setVerticalStretch(1)
            volume_view.setSizePolicy(sizePolicy)

            self.volume_views.append(volume_view)
            self.data_widget.layout().addWidget(volume_view)

    def add_row_widget(self):
        row_widget = QtWidgets.QWidget(self.data_widget)
        QtWidgets.QHBoxLayout(row_widget)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(1)
        row_widget.setSizePolicy(sizePolicy)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(2)

        self.data_widget.layout().addWidget(row_widget)
        return row_widget

    def add_enface_views(self):
        for i, enface_id in enumerate(self.other_enface_ids):
            if i % 3 == 0:
                row_widget = self.add_row_widget()
            enface_view = EnfaceView(parent=self.data_widget)
            enface_view.get_data(enface_id, name=f"Enface_{i}")
            self.enface_views.append(enface_view)
            row_widget.layout().addWidget(enface_view)

    def toggle_linked_navigation(self):
        if self.linked_navigation:
            self.linked_navigation = False
            for view in self.graphic_views:
                view.unlink_navigation()

        else:
            self.linked_navigation = True
            for view in self.graphic_views:
                view.link_navigation()

    def current_tools(self):
        crrnt_item = self.layerOverview.currentWidget().scene.mouseGrabberItem()
        if type(crrnt_item) == TreeAreaItem:
            return "areatools"
        elif type(crrnt_item) == TreeLineItem:
            return "linetools"
        else:
            return None

    def set_tool_buttons(self):
        for i, (name, tool) in enumerate(self.tools.items()):
            self.toolsWidget.layout().addWidget(tool.button, 1,i,1,1)
            tool.button.clicked.connect(self._switch_to_tool(name))

    def _switch_to_tool(self, name):
        def func():
            tool = self.tools[name]
            for n, t in self.tools.items():
                t.button.setChecked(False)
            tool.button.setChecked(True)

            # Show tool options
            self.toolboxWidget.layout().removeWidget(self.optionsWidget)
            self.optionsWidget.setParent(None)
            self.toolboxWidget.layout().addWidget(tool.options_widget)

            self.optionsWidget = tool.options_widget
            self.toolboxWidget.repaint()

            # Set the tool and preview
            for view in self.graphic_views:
                view.set_tool(tool)
        return func

    def set_tabs(self):
        # Todo: this is highly inefficient
        index = self.layerOverview.currentIndex()
        self.layerOverview.clear()
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
