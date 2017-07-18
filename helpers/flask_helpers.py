def checkLoginArgs(request):
    code = request.values.get("code")
    if not code:
        return False

    state = request.values.get("state")
    if not state:
        return False

    error = request.values.get("error")
    if error is not None:
        return False

    return True

def checkArgs(argList, request):
    for arg in argList:
        argument = request.values.get(arg)
        if not argument:
            return False

    return True
