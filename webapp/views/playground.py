import os
import glob

from flask import Blueprint, render_template, redirect

from ..forms import LayoutConfigCheckbox, LocalFilePattern

playground = Blueprint(
    'playground',
    __name__,
    url_prefix='/playground',
)


@playground.route('/')
def playground_index():
    return render_template('playground.html')


@playground.route('/1d_profile', methods=('GET', 'POST'))
def profile_analysis():
    filepattern_input = LocalFilePattern()
    layouts_checkbox = LayoutConfigCheckbox({})

    if filepattern_input.validate_on_submit():
        p = filepattern_input.filepattern.data
        # print(p)
        files = sorted(glob.glob(p))
        # print(files)
        # return redirect('/playground/1d_profile')
    else:
        files = []
    files = [os.path.split(f)[-1] for f in files]
    return render_template(
        '1d_profile.html',
        filepattern_input=filepattern_input,
        files=enumerate(files),
        layouts_checkbox=layouts_checkbox,
    )


@playground.route('/2d_image')
def image_analysis():
    return 'Hello, here is 2D images.'


@playground.route('/3d_density')
def density_analysis():
    return render_template('3d_density.html')
