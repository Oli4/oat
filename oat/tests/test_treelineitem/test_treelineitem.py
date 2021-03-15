import pytest
import json

from PyQt5 import QtCore

from oat.modules.annotation.models.treeview.lineitem import TreeLineItemOffline

layer_types = [
    {"name": "RPE", "id": 0, "default_color": "FF0000", "description": ""},
    {"name": "idealRPE", "id": 1, "default_color": "00FF00", "description": ""},
    {"name": "BM", "id": 2, "default_color": "0000FF", "description": ""},
    {"name": "ILM", "id": 3, "default_color": "FFFF00", "description": ""},
    {"name": "EZ", "id": 4, "default_color": "FF00FF", "description": ""}
]

@pytest.fixture
def treelineitem():
    data = {
        "annotationtype": layer_types[0],
        "current_color": layer_types[0]["default_color"],
        "image_id": None,
        "z_value": 1,
        "line_data": json.dumps({"curves": [], "points": []})}
    return TreeLineItemOffline.create(data, shape=(496,512))

def test_TreeLineItemOffline():
    data = {
        "annotationtype": layer_types[0],
        "current_color": layer_types[0]["default_color"],
        "image_id": None,
        "z_value": 1,
        "line_data": json.dumps({"curves": [], "points": []})}
    treelineitem = TreeLineItemOffline.create(data, shape=(496, 512))

    assert treelineitem.z_value == data["z_value"]
    assert treelineitem.annotationtype == data["annotationtype"]
    assert treelineitem.line_data == json.loads(data["line_data"])

def test_TreeLineItemOffline_add_knot(treelineitem):
    treelineitem.add_knot(QtCore.QPointF(5.0, 5.0),
                           QtCore.QPointF(4.0, 5.0),
                           QtCore.QPointF(6.0, 5.0))
    assert len(treelineitem.curve_knots) == 1
    assert len(treelineitem.curve_knots[0]) == 1
    assert treelineitem.curve_knots[0][0].knot.as_tuple() == (5.0, 5.0)
    assert treelineitem.curve_knots[0][0].cp_in.as_tuple() == (4.0, 5.0)
    assert treelineitem.curve_knots[0][0].cp_out.as_tuple() == (6.0, 5.0)

def test_TreeLineItemOffline_delete_knot(treelineitem):
    treelineitem.add_knot(QtCore.QPointF(5.0, 5.0),
                           QtCore.QPointF(4.0, 5.0),
                           QtCore.QPointF(6.0, 5.0))
    treelineitem.delete_knot(treelineitem.curve_knots[0][0])
    assert len(treelineitem.curve_knots) == 0
    assert len(treelineitem.curve_knots[0]) == 0