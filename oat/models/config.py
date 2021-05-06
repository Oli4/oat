from PySide6.QtCore import Qt

# models data roles
VISIBILITY_ROLE = Qt.UserRole + 1
NAME_ROLE = Qt.UserRole + 2
DATA_ROLE = Qt.UserRole + 3
SHAPE_ROLE = Qt.UserRole + 4
SLICEPOSITIONS_ROLE = Qt.UserRole + 5
XSCALING_ROLE = Qt.UserRole + 6
YSCALING_ROLE = Qt.UserRole + 7
ACTIVESLICE_ROLE = Qt.UserRole + 8

FEATURE_DICT_ROLE = Qt.UserRole + 13
FEATUREID_ROLE = Qt.UserRole + 9
MATCHID_ROLE = Qt.UserRole + 10
SCENE_ROLE = Qt.UserRole + 11
POINT_ROLE = Qt.UserRole + 12
DELETE_ROLE = Qt.UserRole + 14
EYEID_ROLE = Qt.UserRole + 15
OPACITY_ROLE = Qt.UserRole + 16
POSITION_ROLE = Qt.UserRole + 17
COLOR_ROLE = Qt.UserRole + 18
ID_ROLE = Qt.UserRole + 19
EMPTY_ROLE = Qt.UserRole + 20

role_mapping = {VISIBILITY_ROLE: "visible", NAME_ROLE: "name",
                DATA_ROLE: "data", None: "data", SHAPE_ROLE: "shape",
                SLICEPOSITIONS_ROLE: "slice_positions",
                XSCALING_ROLE: "x_scaling", YSCALING_ROLE: "y_scaling",
                ACTIVESLICE_ROLE: "active_slice"}
