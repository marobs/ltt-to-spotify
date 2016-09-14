from flask import *

def checkLoginArgs(request):
	code = request.args.get("code")
	if not code:
		return False

	state = request.args.get("state")
	if not state:
		return False

	error = request.args.get("error")
	if error != None:
		return False

	return True

def checkTokenArgs(response):
	print "CHECKING JSON"
	json = response.json()

	print json

	return json