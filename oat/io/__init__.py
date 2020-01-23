from .he_raw import get_bscan_images, get_slo_image, get_vol_header
import imageio

def get_cfp(filepath):
    """

    :param filepath:
    :return:
    """
    return imageio.imread(filepath)