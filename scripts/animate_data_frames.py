from __future__ import print_function, division

import os
import sys
import glob

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from PIL import Image

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
from RAW import RAWSimulator


def get_boxcenter(array_shape, center, radius=100):
    box_center = (np.minimum(curr_center, radius, dtype=int)
                  for curr_center in zip(center))
    return np.vstack(box_center).flatten()


def get_boxsize(array_shape, center, radius=100):
    if len(center) != len(array_shape):
        raise ValueError(
            'Length of center must be the same with dimension of array')
    size = (np.minimum(curr_center + radius, max_len, dtype=int) -
            np.maximum(curr_center - radius, 0, dtype=int)
            for curr_center, max_len in zip(center, array_shape))
    return tuple(size)


def boxslice(array, center, radius=100):
    """Slice a box with given radius from ndim array and return a view.
    Please notice the size of return is uncertain, which depends on boundary.

    Parameters
    ----------
    array : array_like
    Input array.

    center : tuple of int
    Center in array to boxing. For 2D array, it's (row_center, col_center).
    Length must be the same with dimension of array.

    Returns
    -------
    out : array_like
    A view of `array` with given box range.
    """
    if len(center) != array.ndim:
        raise ValueError(
            'Length of center must be the same with dimension of array')
    slicer = [
        slice(
            np.maximum(curr_center - radius, 0, dtype=int),
            np.minimum(curr_center + radius, max_len, dtype=int),
        ) for curr_center, max_len in zip(center, array.shape)
    ]
    return array[slicer]


def subtract_radial_average(img, center, mask=None):
    """Let image subtract its radial average matrix.
    
    Parameters
    ----------
    img : numpy.ndarray
        2D matrix of input image
    center : tuple of int
        center of image
    mask : numpy.ndarray, optional
        mask for image. 1 means valid area, 0 means masked area.
        (the default is None, which is no mask.)
    
    Returns
    -------
    numpy.ndarray
        return residual image.
    """
    assert img.ndim == 2, 'Wrong dimension for image.'
    assert len(center) == 2, 'Wrong dimension for center.'
    if mask is not None:
        masked_img = img * mask
    else:
        masked_img = img
    center = np.round(center)
    meshgrids = np.indices(img.shape)  # return (xx, yy)
    # eq: r = sqrt( (x - x_center)**2 + (y - y_center)**2 + (z - z_center)**2 )
    r = np.sqrt(sum(((grid - c)**2 for grid, c in zip(meshgrids, center))))
    r = np.round(r).astype(np.int)

    total_bin = np.bincount(r.ravel(), masked_img.ravel())
    nr = np.bincount(r.ravel())  # count for each r
    if mask is not None:
        r_mask = np.zeros(r.shape)
        r_mask[np.where(mask == 0.0)] = 1
        nr_mask = np.bincount(r.ravel(), r_mask.ravel())
        nr = nr - nr_mask
    radialprofile = np.zeros_like(nr)
    # r_pixel = np.unique(r.ravel())  # sorted
    nomaskr = np.where(nr > 0)
    radialprofile[nomaskr] = total_bin[nomaskr] / nr[nomaskr]
    if mask is None:
        residual_img = masked_img - radialprofile[r]  # subtract mean matrix
    else:
        residual_img = masked_img - radialprofile[r] * mask
    return residual_img


def animate_frames(framefiles,
                   mask,
                   image_dim,
                   center,
                   radius=150,
                   subtract_average=False,
                   vmin=0,
                   vmax=400,
                   show=False,
                   save_to_video=True,
                   animation_name=None):
    """animate sas data frames
    """
    boxshape = get_boxsize(image_dim, center, radius)
    # stack_shape: num_images, row, col
    stack_shape = [len(framefiles)] + list(boxshape)
    image_stack = np.zeros(stack_shape, dtype=float)
    boxed_mask = boxslice(mask, center, radius)
    box_center = get_boxcenter(image_dim, center, radius)

    for i, filename in enumerate(framefiles):
        with Image.open(filename) as tiff:
            boxed_image = boxslice(
                np.fliplr(np.asarray(tiff, dtype=float)), center,
                radius) * boxed_mask
            if subtract_average:
                boxed_image = subtract_radial_average(boxed_image, box_center,
                                                      boxed_mask)
            image_stack[i, :, :] = boxed_image

    fig, ax = plt.subplots()
    ax_divider = make_axes_locatable(ax)
    cax = ax_divider.append_axes('right', size='7%', pad='2%')
    if subtract_average:
        im = ax.imshow(image_stack[0], cmap='jet', animated=True)
    else:
        im = ax.imshow(
            image_stack[0], cmap='jet', vmin=vmin, vmax=vmax, animated=True)
    title = ax.set_title('current frame: {}'.format(str(1).zfill(3)))
    cb = fig.colorbar(im, cax=cax)

    fig.tight_layout()

    def update_im(fr):
        im.set_data(image_stack[fr])
        cb.set_array(image_stack[fr])
        cb.autoscale()
        title.set_text('current frame: {}'.format(str(fr + 1).zfill(3)))
        cb.draw_all()
        fig.canvas.draw_idle()
        # return a sequence of artists, not a single artist
        return im,

    # call the animator.  blit=True means only re-draw the parts that have changed.
    # interval: Delay between frames in milliseconds. Defaults to 200.
    # Additional arguments to pass to each call to func
    # http://matplotlib.org/api/_as_gen/matplotlib.animation.FuncAnimation.html
    # anim = animation.ArtistAnimation(fig, ims, interval=100, blit=True)
    frames_iter = range(len(framefiles))
    anim = animation.FuncAnimation(
        fig, update_im, frames_iter, interval=500, blit=True, repeat=False)

    if save_to_video:
        # save the animation as an mp4.  This requires ffmpeg or mencoder to be
        # installed.  The extra_args ensure that the x264 codec is used, so that
        # the video can be embedded in html5.  You may need to adjust this for
        # your system: for more information, see
        # http://matplotlib.sourceforge.net/api/animation_api.html
        if animation_name is None:
            animation_name = 'animation.mp4'
        elif not animation_name.endswith('.mp4'):
            animation_name += '.mp4'
        anim.save(animation_name, fps=4, extra_args=['-vcodec', 'libx264'])

    if show:
        plt.show()


def gen_animation(raw_settings, image_filenames, animation_name='./animation'):
    x_center = int(raw_settings.get('Xcenter'))
    y_center = int(raw_settings.get('Ycenter'))
    image_dim = tuple(int(v) for v in raw_settings.get('MaskDimension'))

    col_center = x_center
    row_center = image_dim[0] - y_center
    center = [row_center, col_center]

    mask = raw_settings.get('BeamStopMask')
    if mask is None:
        mask = raw_settings.get('Masks')['BeamStopMask']

    if not image_filenames:
        raise FileNotFoundError('No image files found.')

    animate_frames(
        image_filenames,
        mask,
        image_dim,
        center,
        vmax=70,
        save_to_video=True,
        # show=True,
        animation_name=animation_name)


def main():
    image_directory = sys.argv[1]
    raw_cfg_path = sys.argv[2]

    raw_simulator = RAWSimulator(raw_cfg_path)
    raw_settings = raw_simulator.get_raw_settings()
    image_format = '.tif'

    image_filenames = sorted(
        glob.glob(os.path.join(image_directory, '*' + image_format)))
    for filename in reversed(image_filenames):
        if 'buffer' in filename:
            image_filenames.remove(filename)

    root = os.path.dirname(image_directory)
    root_name = os.path.basename(root)
    animation_name = os.path.join(root, 'Figures',
                                  root_name + '_dynamic_video')
    os.makedirs(os.path.join(root, 'Figures'), exist_ok=True)
    gen_animation(raw_settings, image_filenames, animation_name)


if __name__ == '__main__':
    main()
