from global_helpers import basePath
import cPickle
import os.path
import json
from helpers import flag_helpers

###
### Objects
###

VALUE_NOT_FOUND = "VALUE_NOT_FOUND"
rCacheDict = {}
sCacheDict = {}
sCachePath = basePath + '/../cache/spotifyCache.pkl'
idCacheDict = {}
idCachePath = basePath + '/../cache/idCache.pkl'

#####################################################
#                                                   #
#                   Spotify                         #
#                                                   #
#####################################################

def saveToSCacheByKeyList(spotifyTrack, keyList):
    if not checkCacheEnabled("save to SCache"):
        return

    global sCacheDict

    for key in keyList:
        if spotifyTrack is not None:
            sCacheDict[str(key)] = dict(spotifyTrack)
        else:
            sCacheDict[str(key)] = None

def getFromSCache(trackId):
    if not checkCacheEnabled("get from SCache"):
        return None

    global notFoundValue
    global sCacheDict

    if trackId in sCacheDict:
        if sCacheDict[trackId] is not None:
            return sCacheDict[trackId]

        else:  # Not found entry
            return notFoundValue

    else:
        return None

def initializeSCache():
    if not checkCacheEnabled("initializing SCache"):
        return

    print "Initializing SCache"
    global sCacheDict

    if not os.path.isfile(sCachePath):
        return {}

    with open(sCachePath, 'rb') as f:
        obj = cPickle.load(f)

        if obj is not None:
            sCacheDict = obj

        else:
            sCacheDict = {}

def flushSCache():
    if not checkCacheEnabled("flushing SCache"):
        return

    global sCacheDict
    with open(sCachePath, 'wb') as f:
        f.seek(0)
        f.truncate()
        cPickle.dump(sCacheDict, f, cPickle.HIGHEST_PROTOCOL)

#####################################################
#                                                   #
#                   Reddit                          #
#                                                   #
#####################################################

def saveToRCache(redditData, queryType):
    if not checkCacheEnabled("saving to RCache"):
        return

    global rCacheDict

    if redditData is not None and queryType is not None and checkQueryType(queryType):
        rCacheDict[str(queryType)] = list(redditData)

def getFromRCache(queryType):
    if not checkCacheEnabled("getting from RCache"):
        return None

    global rCacheDict
    if queryType in rCacheDict:
        return list(rCacheDict[queryType])

def checkQueryType(queryType):
    return queryType == 'top' or \
           queryType == 'hot' or \
           queryType == 'new' or \
           queryType == 'rising' or \
           queryType == 'controversial'

def checkCacheEnabled(action):
    if not flag_helpers.CACHE_ENABLED():
        print "No-cache mode enabled, not " + str(action)
        return False

    return True

#####################################################
#                                                   #
#                     Ids                           #
#                                                   #
#####################################################

def saveToIDCache(spotifyId, name):
    if not checkCacheEnabled("save to idcache"):
        return

    global idCachedict
    idCacheDict[spotifyId] = name

def getFromIDCache(spotifyId):
    if not checkCacheEnabled("get from idCache"):
        return None

    global notFoundValue
    global sCacheDict

    if spotifyId in idCacheDict:
        if idCacheDict[spotifyId] is not None:
            return idCacheDict[spotifyId]

        else:  # Not found entry
            return notFoundValue

    else:
        return None

def initializeIDCache():
    if not checkCacheEnabled("initializing idCache"):
        return

    print "Initializing SCache"
    global idCacheDict

    if not os.path.isfile(idCachePath):
        return {}

    with open(idCachePath, 'rb') as f:
        obj = cPickle.load(f)

        if obj is not None:
            idCacheDict = obj

        else:
            idCacheDict = {}

def flushIDCache():
    if not checkCacheEnabled("flushing idCacheDict"):
        return

    global sCacheDict
    with open(idCachePath, 'wb') as f:
        f.seek(0)
        f.truncate()
        cPickle.dump(idCacheDict, f, cPickle.HIGHEST_PROTOCOL)
