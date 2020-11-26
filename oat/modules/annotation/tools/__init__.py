from .inspection import Inspection
from .pen import Pen

tools = lambda : {"pen": Pen(),
                  "inspection": Inspection()}