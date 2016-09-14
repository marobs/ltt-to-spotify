import urllib
from flask import *
import helpers
import ltt
import os
import requests

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def main_route():	
	if not helpers.checkAuthenticated():
		print "Must authenticate!"
		return redirect(helpers.getAuthorizationUrl())	
	else:
		print "Found access token!"
		return "Found AT!"

@main.route('/login')
def login_route():
	if not helpers.checkLoginArgs(request):
		return render_template("404.html", error=request.args.get("error")), 404

	if request.args.get("state") != helpers.getState():
		return render_template("404.html", error="Different states found"), 404

	# Generate data and post to token endpoint to get access and refresh tokens
	postData = helpers.getTokenRequestData(request.args.get("code"))
	response = requests.post("https://accounts.spotify.com/api/token", data=postData)
	json = helpers.checkTokenArgs(response)


	print "DONE CHECKING ARS"

	ltt.getRedditPosts()

	#helpers.saveRefreshToken(json)
	#helpers.setAccessToken(json)

	return render_template("message.html", message="Done")


