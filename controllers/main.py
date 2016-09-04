from flask import *
import os

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def main_route():
	print "TESTING"
	return "MAIN ROUTE"