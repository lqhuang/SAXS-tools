from flask import Blueprint

features = Blueprint(
    'features',
    __name__,
    url_prefix='/features',
)


@features.route('/')
def features_index():
    return 'Hello, here is index of features page.'
