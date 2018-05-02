from flask import render_template, Blueprint

index = Blueprint(
    'index',
    __name__,
    # template_folder='templates',  # Path for templates
    # static_folder='static',  # Path for static files
)


@index.route('/')
def cover():
    return render_template('cover.html')


@index.route('/index')
def blog_index():
    return render_template('index.html')


@index.route('/export')
def export():
    return render_template('export.html')


@index.route('/timer')
def timer():
    return render_template('timer.html')
