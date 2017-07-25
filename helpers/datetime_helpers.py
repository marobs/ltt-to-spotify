import datetime

def getNow():
    return datetime.datetime.utcnow()

def isoToEpoch(iso):
    utc_dt = datetime.datetime.strptime(iso, '%Y-%m-%dT%H:%M:%S.%fZ')
    return datetimeToEpochMs(utc_dt)

def datetimeToEpochMs(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds() * 1000)

