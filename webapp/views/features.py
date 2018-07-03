from flask import render_template, Blueprint

features = Blueprint(
    'features',
    __name__,
    url_prefix='/features',
)


@features.route('/')
def features_index():
    return render_template('features.html')
