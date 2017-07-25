from global_helpers import basePath

logPath = basePath + '/../log/log.txt'

def logGeneral(toLog):
    global logPath
    with open(logPath, 'wb') as f:
        f.seek(0)
        f.truncate()
        f.write(str(toLog))

def logAppend(toLog):
    global logPath
    with open(logPath, 'a') as f:
        f.write(str(toLog))