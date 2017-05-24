from functools import partial
import time

import numpy as np
from PIL import Image

import dat


def average_tiff_imgs(filelist, mask, output_filename=None):
    mask = np.asarray(mask, dtype=float)
    xlen, ylen = mask.shape
    imgs = np.zeros([xlen, ylen, len(filelist)], dtype=float)
    for i, filename in enumerate(filelist):
        with Image.open(filename) as img:
            imgs[:, :, i] = np.array(img)

    # mean = np.mean(aver_img)
    # std = np.std(aver_img)
    # aver_img[aver_img > mean + 3 * std] = 0
    aver_img = np.average(imgs, axis=2) * mask

    if output_filename is None:
        pass
    else:
        tiff_img = Image.fromarray(aver_img)
        try:
            tiff_img.save(output_filename, 'tiff')
        except:
            raise ValueError('wrong filename for output: ', output_filename)

    return aver_img


def create_block_masks(mask, center, block_num=8):

    mask = np.asarray(mask, dtype=float)
    center = np.asarray(center, dtype=float)
    block_num = np.asarray(block_num, dtype=float)
    assert len(mask.shape) == 2
    assert center.size == 2

    yv, xv = np.indices(mask.shape)
    theta = np.arctan2(yv-center[1], xv-center[0])
    theta[theta < 0] += 2 * np.pi
    step = 2 * np.pi / block_num
    mask_list = [np.zeros(mask.shape) for i in range(int(block_num))]

    for i, block_mask in enumerate(mask_list):
        lower = step * i
        upper = step * (i + 1)
        cond = np.logical_and(theta >= lower, theta < upper)
        mask_list[i][cond] = 1

    create_masks = lambda block_mask, mask: np.logical_and(mask, block_mask)
    block_masks = [np.array(create_masks(block_mask, mask), dtype=float)
                   for block_mask in mask_list]

    return block_masks


def calc_block_radial_profile(image, center, mask_list, binsize=1., mode='sum'):

    block_radial_profile = [calc_radial_profile(image, center, mask=block_mask,
                                                binsize=binsize, mode=mode)
                            for block_mask in mask_list]
    return block_radial_profile

def cart2pol(x, y):
    """Summary

    Parameters
    ----------
    x : array_like
        x values in Cartesian coordinates
    y : array_like with the same shape of x
        y values in Cartesian coordinates

    Returns
    -------
    rho, theta: ndarray
        rho and theta values in polar coordinates
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    assert x.shape == y.shape
    rho = np.sqrt(np.power(x, 2) + np.power(y, 2))
    theta = np.arctan2(y, x)
    return rho, theta


def pol2cart(rho, theta):
    """Summary

    Parameters
    ----------
    rho : array_like
        rho values in polar coordinates
    theta : array_like
        theta values in polar coordinates

    Returns
    -------
    x, y: ndarray
        x and y values in Cardisian coordinates
    """
    rho = np.asarray(rho, dtype=np.float64)
    theta = np.asarray(theta, dtype=np.float64)
    assert rho.shape == theta.shape
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y

# Calculate profiles
def calc_radial_profile(image, center, binsize=1., mask=None, mode='sum'):
    """Summary

    Parameters
    ----------
    image : 2d array
        Input image to calculate radial profile
    center : array_like with 2 elements
        Center of input image
    binsize : float, optional
        By default, the binsize is 1 in pixel.
    mask : 2d array, optional
        Binary 2d array used in radial profile calculation. The shape must be same with image. 1 means valid while 0 not.
    mode : {'sum', 'mean'}, optional
        'sum'
        By default, mode is 'sum'. This returns the summation of each ring.

        'mean'
        Mode 'mean' returns the average value of each ring.

    Returns
    -------
    Radial profile: 1d array
        Output array, contains summation or mean value of each ring with binsize of 1 along rho axis.

    Raises
    ------
    ValueError
        Description
    """
    t1 = time.time()
    image = np.asarray(image, dtype=np.float64)
    assert len(image.shape) == 2
    center = np.asarray(center, dtype=np.float64)
    assert center.size == 2
    if mask is not None:
        mask = np.asarray(mask, dtype=np.float64)
        assert mask.shape == image.shape
        assert mask.min() >= 0. and mask.max() <= 1.
        mask = (mask > 0.5).astype(np.float64)
    else:
        mask = np.ones_like(image)
    image = image * mask
    y, x = np.indices((image.shape))
    r = np.sqrt((x - center[0])**2. + (y - center[1])**2.)
    bin_r = r / binsize
    bin_r = np.round(bin_r).astype(int)
    radial_sum = np.bincount(bin_r.ravel(), image.ravel())  # summation of each ring

    radial_std = np.zeros_like(radial_sum)
    for x in range(bin_r.max()):
        radial_std[x] = image[bin_r == x].std()
    nr = np.bincount(bin_r.ravel(), mask.ravel())
    radial_mean = radial_sum / nr
    radial_mean[np.isinf(radial_mean)] = 0.
    radial_mean[np.isnan(radial_mean)] = 0.
    radial_rstd = radial_std / radial_mean
    radial_rstd[np.isinf(radial_rstd)] = 0.
    radial_rstd[np.isnan(radial_rstd)] = 0.
    print('time is ', time.time()-t1)
    if mode == 'sum':
        return radial_sum
    elif mode == 'mean':
        return radial_mean
    elif mode == 'std':
        return radial_std
    elif mode == 'rstd':
        return radial_rstd
    else:
        raise ValueError('Wrong mode: %s' %mode)

def calc_angular_profile(image, center, binsize=1., mask=None, mode='sum'):
    """Summary

    Parameters
    ----------
    image : 2d array
        Input image to calculate angular profile in range of 0 to 180 deg.
    center : array_like with 2 elements
        Center of input image
    binsize : float, optional
        By default, the binsize is 1 in degree.
    mask : 2d array, optional
        Binary 2d array used in angular profile calculation. The shape must be same with image. 1 means valid while 0 not.
    mode : {'sum', 'mean'}, optional
        'sum'
        By default, mode is 'sum'. This returns the summation of each ring.

        'mean'
        Mode 'mean' returns the average value of each ring.

    Returns
    -------
    Angular profile: 1d array
        Output array, contains summation or mean value of each ring with binsize of 1 along rho axis.
    """
    image = np.asarray(image, dtype=np.float64)
    assert len(image.shape) == 2
    center = np.asarray(center, dtype=np.float64)
    assert center.size == 2
    if mask is not None:
        mask = np.asarray(mask, dtype=np.float64)
        assert mask.shape == image.shape
        assert mask.min() >= 0. and mask.max() <= 1.
        mask = (mask > 0.5).astype(np.float64)
    else:
        mask = np.ones_like(image)
    image = image * mask
    y, x = np.indices((image.shape))
    theta = np.rad2deg(np.arctan2(y-center[1], x-center[0]))
    bin_theta = theta.copy()
    bin_theta[bin_theta<0.] += 180.
    bin_theta = bin_theta / binsize
    bin_theta = np.round(bin_theta).astype(int)
    angular_sum = np.bincount(bin_theta.ravel(), image.ravel())  # summation of each ring

    if mode == 'sum':
        return angular_sum
    elif mode == 'mean':
        ntheta = np.bincount(bin_theta.ravel(), mask.ravel())
        angular_mean = angular_sum / ntheta
        angular_mean[np.isinf(angular_mean)] = 0.
        return angular_mean
    else:
        raise ValueError('Wrong mode: %s' %mode)


def calc_across_center_line_profile(image, center, angle=0., width=1, mask=None, mode='sum'):
    """Summary

    Parameters
    ----------
    image : 2d array
        Input image to calculate angular profile in range of 0 to 180 deg.
    center : array_like with 2 elements
        Center of input image
    angle : float, optional
        Line angle in degrees.
    width : int, optional
        Line width. The default is 1.
    mask : 2d array, optional
        Binary 2d array used in angular profile calculation. The shape must be same with image. 1 means valid while 0 not.
    mode : {'sum', 'mean'}, optional
        'sum'
        By default, mode is 'sum'. This returns the summation of each ring.

        'mean'
        Mode 'mean' returns the average value of each ring.

    Returns
    -------
    Across center line profile with given width at specified angle: 2d array
        Output array, contains summation or mean value alone the across center line and its indices with respect to the center.
    """
    image = np.asarray(image, dtype=np.float64)
    assert len(image.shape) == 2
    center = np.asarray(center, dtype=np.float64)
    assert center.size == 2
    if mask is not None:
        mask = np.asarray(mask, dtype=np.float64)
        assert mask.shape == image.shape
        assert mask.min() >= 0. and mask.max() <= 1.
        mask = (mask > 0.5).astype(np.float64)
    else:
        mask = np.ones_like(image)
    image = image * mask 
    # generate a larger image if the given center is not the center of the image.
    sy, sx = image.shape
    if sy % 2 == 0:
        # print('padding along first axis')
        image = np.pad(image, ((0,1), (0,0)), 'constant', constant_values=0)
    if sx % 2 == 0:
        # print('padding along second axis')
        image = np.pad(image, ((0,0), (0,1)), 'constant', constant_values=0)
    sy, sx = image.shape
    if center[0] < sx//2 and center[1] < sy//2:
        # print('case1')
        sx_p = int((sx - center[0]) * 2 - 1)
        sy_p = int((sy - center[1]) * 2 - 1)
        ex_img = np.zeros((sy_p, sx_p))
        ex_img[sy_p-sy:sy_p, sx_p-sx:sx_p] = image
    elif center[0] < sx//2 and center[1] > sy//2:
        # print('case2')
        sx_p = int((sx - center[0]) * 2 - 1)
        sy_p = int((center[1]) * 2 - 1)
        ex_img = np.zeros((sy_p, sx_p))
        ex_img[0:sy, sx_p-sx:sx_p] = image
    elif center[0] > sx//2 and center[1] < sy//2:
        sx_p = int((center[0]) * 2 - 1)
        sy_p = int((sy - center[1]) * 2 - 1)
        ex_img = np.zeros((sy_p, sx_p))
        ex_img[sy_p-sy:sy_p, 0:sx] = image
    else:
        # print('case4')
        sx_p = int((center[0]) * 2 + 1)
        sy_p = int((center[1]) * 2 + 1)
        ex_img = np.zeros((sy_p, sx_p))
        ex_img[0:sy, 0:sx] = image
    rot_img = rotate(ex_img, angle)
    rot_sy, rot_sx = rot_img.shape
    across_line = rot_img[rot_sy//2-width//2:rot_sy//2-width//2+width, :].copy()
    across_line_sum = np.sum(across_line, axis=0)
    line_indices = np.indices(across_line_sum.shape)[0] - rot_sx//2
    line_sum = np.bincount(np.abs(line_indices).ravel(), across_line_sum.ravel())
    if mode == 'sum':
        return line_sum
    elif mode == 'mean':
        line_mean = line_sum.astype(np.float) / width
        return line_mean
    else:
        raise ValueError('Wrong mode: %s' %mode)
