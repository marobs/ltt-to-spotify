import urllib
from flask import *
import helpers
import ltt
import os
import requests
import json

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def main_route():
    if not helpers.checkAuthenticated():
        print "Must authenticate!"
        return redirect(helpers.getAuthorizationUrl())

    else:
        print "Found access or refresh token!"
        return "Found AT!"


@main.route('/login')
def login_route():
    if not helpers.checkLoginArgs(request):
        return render_template("404.html", error=request.args.get("error")), 404

    if request.args.get("state") != helpers.getState():
        return render_template("404.html", error="Different states found"), 404

    # Generate data and post to token endpoint to get access and refresh tokens
    clientId = helpers.getClientId()
    clientSecret = helpers.getClientSecret()
    spotifyCode = request.args.get("code")
    postData = helpers.getTokenRequestData(spotifyCode, clientId, clientSecret)
    response = requests.post("https://accounts.spotify.com/api/token", data=postData)

    jsonData = response.json()
    helpers.saveRefreshToken(jsonData.get('refresh_token'))
    helpers.setAccessToken(jsonData.get('access_token'))

    return render_template("message.html", message="Done")
