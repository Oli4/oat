from oat.modules.dialogs.help.help_dialog import HelpWindow

help_text = """
# Layer Annotation Guide
"""

class LayerAnnotationHelp(HelpWindow):
    def __init__(self, parent):
        super().__init__(help_text, parent)