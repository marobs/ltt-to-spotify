from flask import *
import helpers
import os

genre = Blueprint('genre', __name__, template_folder='templates')

@genre.route('/genre')
def genre_route():
	return render_template("404.html"), 404