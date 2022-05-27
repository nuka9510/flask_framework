from system.core.controller import *
from models import Example_Model

bp = Blueprint('Example', __name__, url_prefix='/')
example_model = Example_Model()

@bp.get('/')
def get():
    return render_template('example.html')

@bp.post('/')
def post():
    return render_template('example.html')

@bp.put('/')
def put():
    return render_template('example.html')

@bp.delete('/')
def delete():
    return render_template('example.html')