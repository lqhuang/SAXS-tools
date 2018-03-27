from __future__ import print_function, division

import os
import sys
import glob

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from PIL import Image

from RAW import RAWSimulator


def boxsize(array_shape, center, radius=100):
    if len(center) != len(array_shape):
        raise ValueError(
            'Length of center must be the same with dimension of array')
    size = (np.minimum(curr_center + radius, max_len) -
            np.maximum(curr_center - radius, 0)
            for curr_center, max_len in zip(center, array_shape))
    return tuple(size)


def boxslice(array, center, radius=100):
    """Slice a box with given radius from ndim array and return a view.
    Please notice the size of return is uncertain which depends on boundary.

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
            np.maximum(curr_center - radius, 0),
            np.minimum(curr_center + radius, max_len),
        ) for curr_center, max_len in zip(center, array.shape)
    ]
    return array[slicer]


def animate_frames(framefiles,
                   mask,
                   image_dim,
                   center,
                   radius=200,
                   vmin=0,
                   vmax=400,
                   show=False,
                   save_to_video=True,
                   animation_name=None):
    """[summary]
    
    Parameters:
    ----------
    framefiles : {[type]}
        [description]
    mask : {[type]}
        [description]
    image_dim : {[type]}
        [description]
    center : {[type]}
        [description]
    radius : {int}, optional
        [description] (the default is 200, which [default_description])
    vmin : {int}, optional
        [description] (the default is 0, which [default_description])
    vmax : {int}, optional
        [description] (the default is 400, which [default_description])
    show : {bool}, optional
        [description] (the default is False, which [default_description])
    save_to_video : {bool}, optional
        [description] (the default is True, which [default_description])
    animation_name : {[type]}, optional
        [description] (the default is None, which [default_description])
    
    Returns
    -------
    [type]
        [description]
    """

    boxshape = boxsize(image_dim, center, radius)
    # stack_shape: num_images, row, col
    stack_shape = [len(framefiles)] + list(boxshape)
    image_stack = np.zeros(stack_shape, dtype=float)
    boxed_mask = boxslice(mask, center, radius)
    for i, filename in enumerate(framefiles):
        with Image.open(filename) as tiff:
            image_stack[i, :, :] = boxslice(
                np.fliplr(np.asarray(tiff, dtype=float)), center,
                radius) * boxed_mask

    # for img in image_stack:
    #     img /= np.mean(img[np.bool_(boxed_mask)])

    dist = [80] * 100

    # for i in range(6):
    #     dist[i] = 170

    # for i in range(1, 6):
    #     dist[i+5] = 170 - ( (170 - 80) * (i/5) )

    fig, ax = plt.subplots()
    ax_divider = make_axes_locatable(ax)
    cax = ax_divider.append_axes('right', size='7%', pad='2%')
    im = ax.imshow(
        image_stack[0], cmap='jet', vmin=vmin, vmax=vmax, animated=True)
    title = ax.set_title('current frame: {}, magnet distance {:.2f} mm'.format(
        str(1).zfill(3), dist[0]))
    fig.colorbar(im, cax=cax)
    fig.tight_layout()

    def update_im(fr):
        im.set_data(image_stack[fr])
        title.set_text('current frame: {}, magnet distance: {:.2f} mm'.format(
            str(fr + 1).zfill(3), dist[fr]))
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


def gen_animation(raw_settings, image_filenames):

    x_center = raw_settings.get('Xcenter')[0]
    y_center = raw_settings.get('Ycenter')[0]
    image_dim = raw_settings.get('MaskDimension')[0]

    col_center = x_center
    row_center = image_dim[0] - y_center
    center = [row_center, col_center]

    mask = raw_settings.get('BeamStopMask')
    if mask is None:
        mask = raw_settings.get('Masks')['BeamStopMask'][0]

    if not image_filenames:
        raise FileNotFoundError('No image files found.')

    animate_frames(
        image_filenames,
        mask,
        image_dim,
        center,
        vmax=30,
        save_to_video=True,
        # show=True,
        animation_name='201612_EXP27_dynamics')


def main():
    raw_cfg_path = sys.argv[1]
    image_directory = sys.argv[2]

    raw_settings = RAWSimulator(raw_cfg_path)
    image_format = '.tif'

    image_filenames = sorted(
        glob.glob(os.path.join(image_directory, '*' + image_format)))
    for filename in reversed(image_filenames):
        if 'buffer' in filename:
            image_filenames.remove(filename)

    gen_animation(raw_settings, image_filenames)


if __name__ == '__main__':
    main()
