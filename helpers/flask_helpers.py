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

def checkArgs(argList, request):
    for arg in argList:
        argument = request.args.get(arg)
        if not argument:
            return False

    return True
