import pytest
from oat.modules.annotation.models.treeview.lineitem import CubicSplineKnotItem

def test_cubicsplineknot_from_dict():
    d = {"knot": (10.5, 10.5), "cpin": (8.4, 10.5), "cpout": (12.1, 10.5)}
    knot = CubicSplineKnotItem.from_dict(d)
    assert knot.knot.as_tuple() == d["knot"]
    assert knot.cp_in.as_tuple() == d["cpin"]
    assert knot.cp_out.as_tuple() == d["cpout"]

@pytest.fixture
def cubicsplineknot():
    d = {"knot": (10.5, 10.5), "cpin": (8.4, 10.5), "cpout": (12.1, 10.5)}
    return CubicSplineKnotItem.from_dict(d)

