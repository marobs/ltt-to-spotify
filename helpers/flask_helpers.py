from flask import *

def checkLoginArgs(request):
    code = request.args.get("code")
    if not code:
        return False

    state = request.args.get("state")
    if not state:
        return False

    error = request.args.get("error")
    if error is not None:
        return False

    return True

def checkTokenArgs(response):
    print "CHECKING JSON"
    responsejson = response.json()

    print responsejson

    return responsejson