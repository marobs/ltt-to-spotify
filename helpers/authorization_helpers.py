import urllib
from global_helpers import *
from session_helpers import *

def getAuthorizationUrl():
	url  = "?client_id="     + urllib.quote_plus(getClientId())
	url += "&response_type=" + "code"
	url += "&redirect_uri="  + urllib.quote_plus("http://localhost:3000/login")
	url += "&scope="         + urllib.quote_plus(getScopes())
	url += "&state="         + getState()

	return "https://accounts.spotify.com/authorize" + url

def getScopes():
 	scopes = []
 	scopes.append("playlist-read-private")
 	scopes.append("playlist-read-collaborative")
 	scopes.append("playlist-modify-public")
 	scopes.append("playlist-modify-private")
 	scopes.append("user-follow-read")
 	scopes.append("user-library-read")
 	scopes.append("user-library-modify")
 	scopes.append("user-read-private")
 	scopes.append("user-read-birthdate")
 	scopes.append("user-top-read")
 	return " ".join(scopes)


def getTokenRequestData(code):
	form = {}
	form["grant_type"]    = "authorization_code"
	form["code"]          = code
	form["redirect_uri"]  = "http://localhost:3000/login"
	form["client_id"]     = getClientId()
	form["client_secret"] = getClientSecret()

	return form