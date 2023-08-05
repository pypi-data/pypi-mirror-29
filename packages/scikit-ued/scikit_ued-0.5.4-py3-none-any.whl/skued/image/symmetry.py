# -*- coding: utf-8 -*-
"""
Image manipulation involving symmetry
=====================================
"""
from functools import partial, wraps
from warnings import warn, catch_warnings

import numpy as np
from skimage.transform import rotate
from npstreams import imean, last

# TODO: out parameter?
def nfold(im, mod, center = None, mask = None, fill_value = 0.0, **kwargs):
    """ 
    Returns an images averaged according to n-fold rotational symmetry.

    Parameters
    ----------
    im : array_like, ndim 2
        Image to be averaged.
    center : array_like, shape (2,) or None, optional
        coordinates of the center (in pixels). If ``center=None``, the image is rotated around
        its center, i.e. ``center=(rows / 2 - 0.5, cols / 2 - 0.5)``.
    mod : int
        Fold symmetry number. Valid numbers must be a divisor of 360.
    mask : `~numpy.ndarray` or None, optional
        Mask of `image`. The mask should evaluate to `True`
        (or 1) on invalid pixels. If None (default), no mask
        is used.
    fill_value : float, optional
        In the case of a mask that overlaps with itself when rotationally averaged,
        the overlapping regions will be filled with this value.
    kwargs
        Keyword arguments are passed to skimage.transform.rotate().

    Returns
    -------
    out : `~numpy.ndarray`, dtype float
        Averaged image.

    Raises
    ------
    ValueError
        If `mod` is not a divisor of 360 deg.
    
    See also
    --------
    skimage.transform.rotate : Rotate images by interpolation.
    """
    if (360 % mod):
        raise ValueError('{}-fold rotational symmetry is not valid (not a divisor of 360).'.format(mod))
    angles = range(0, 360, int(360/mod))

    im = np.array(im, dtype = np.float, copy = True)

    if mask is not None:
       im[mask] = np.nan
    
    rotate_kwargs = {'mode': 'constant', 'preserve_range': True}
    rotate_kwargs.update(kwargs)

    rotated = (rotate(im, angle, center = center, **rotate_kwargs) for angle in angles)
    avg = last(imean(rotated, axis = 2, ignore_nan = True))
    
    avg[np.isnan(avg)] = fill_value
    return avg