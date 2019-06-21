from .images import *
from .areas import *
from .lines import *

layer_types_2d = {'Line Layer': LineLayer2D,
                  'Area Layer': AreaLayer2D,
                  'HRF Layer': HrfLayer2D,
                  'HP Layer': HPLayer2D,
                  'Drusen Layer': DrusenLayer2D,
                  'Image Layer': ImageLayer2D,
                  'NIR Layer': NirLayer,
                  'CFP Layer': CfpLayer}
layer_types_3d = {'Line Layer': LineLayer3D,
                  'RPE Layer': RpeLayer,
                  'BM Layer': BmLayer,
                  'EZ Layer': EzLayer,
                  'Area Layer': AreaLayer3D,
                  'HRF Layer': HrfLayer3D,
                  'Drusen Layer': DrusenLayer3D,
                  'Image Layer': ImageLayer3D,
                  'OCT Layer': OctLayer,}