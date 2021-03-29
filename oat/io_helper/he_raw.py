from struct import unpack
import numpy as np
import os
import cv2

import functools

def hist_match(source, template=None):
    """
    Adjust the pixel values of a grayscale image such that its histogram
    matches that of a target image

    Arguments:
    -----------
        source: np.ndarray
            Image to transform; the histogram is computed over the flattened
            array
        template: np.ndarray
            Template image; can have different dimensions to source
    Returns:
    -----------
        matched: np.ndarray
            The transformed output image
    """

    oldshape = source.shape

    # Flatten the input arrays
    source = source.ravel()
    if template is not None:
        template = template.ravel()
        t_values, t_counts = np.unique(template, return_counts=True)
        np.savez('oct_refhist.npz', t_values=np.array(t_values), t_counts=np.array(t_counts))
    else:
        refhist_path = os.path.join(os.path.dirname(__file__), 'oct_refhist.npz')
        ref_vals = np.load(refhist_path)
        t_values, t_counts = ref_vals['t_values'], ref_vals['t_counts']

    # get the set of unique pixel values and their corresponding indices and
    # counts
    s_values, bin_idx, s_counts = np.unique(source, return_inverse=True,
                                            return_counts=True)

    # take the cumsum of the counts and normalize by the number of pixels to
    # get the empirical cumulative distribution functions for the source and
    # template images (maps pixel value --> quantile)
    s_quantiles = np.cumsum(s_counts).astype(np.float64)
    s_quantiles /= s_quantiles[-1]
    t_quantiles = np.cumsum(t_counts).astype(np.float64)
    t_quantiles /= t_quantiles[-1]

    # interpolate linearly to find the pixel values in the template image
    # that correspond most closely to the quantiles in the source image
    interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)

    return interp_t_values[bin_idx].reshape(oldshape)


