from flask import Blueprint

playground = Blueprint(
    'playground',
    __name__,
    url_prefix='/playground',
)


@playground.route('/')
def playground_index():
    return 'Hello, here is index of playground.'


@playground.route('/1d_curves/')
def one_dimension_analysis():
    return 'Hello, here is 1D curves.'


@playground.route('/2d_map')
def images_analysis():
    return 'Hello, here is 2D images.'


@playground.route('/3d_density')
def density_analysis():
    return 'Hello, here is 3D density.'
