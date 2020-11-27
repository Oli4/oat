from .inspection import Inspection
from .pen import Pen
from functools import lru_cache

@lru_cache()
def tools():
    return {"pen": Pen(),
            "inspection": Inspection()}
