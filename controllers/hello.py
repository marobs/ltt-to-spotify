from flask import *

hello = Blueprint('hello', __name__, template_folder='templates')

@hello.route('/hello')
def hello_route():
	return "Hello World!"
