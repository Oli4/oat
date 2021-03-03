from .inspection import Inspection
from .pen import Pen
from .splinetool import Spline


#def tools():
#    return {"areatools": {"pen": Pen(),
#                          "inspection": Inspection()},
#            "linetools": {},
#            }

def tools():
    return {"pen": Pen(),
            "inspection": Inspection(),
            "spline": Spline()}
