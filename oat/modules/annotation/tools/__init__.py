from .inspection import Inspection
from .pen import Pen

def tools():
    return {"pen": Pen(),
            "inspection": Inspection()}
