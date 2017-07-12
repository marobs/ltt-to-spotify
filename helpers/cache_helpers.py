from global_helpers import basePath
import cPickle
import os.path


###
### Objects
###

rCacheDict = {}
sCacheDict = {}
sCachePath = basePath + '/../cache/spotifyCache.pkl'

#####################################################
#                                                   #
#                   Spotify                         #
#                                                   #
#####################################################

def saveToSCache(spotifyTrack, topTrack):
    global sCacheDict

    trackId = spotifyTrack['id']
    sCacheDict[trackId] = spotifyTrack

    if topTrack is not None:
        topId = topTrack['id']
        sCacheDict[topId] = topTrack

def getFromSCache(trackId):
    global sCacheDict

    if trackId in sCacheDict:
        return sCacheDict[trackId]

    else:
        return None

def initializeSCache():
    global sCacheDict

    if not os.path.isfile(sCachePath):
        return {}

    with open(sCachePath, 'rb') as f:
        obj = cPickle.load(f)

        print "LOADED OBJ: "
        print str(obj)

        if obj is not None:
            sCacheDict = obj

        else:
            sCacheDict = {}

def flushSCache():
    global sCacheDict
    with open(sCachePath, 'wb') as f:
        cPickle.dump(sCacheDict, f, cPickle.HIGHEST_PROTOCOL)

#####################################################
#                                                   #
#                   Reddit                          #
#                                                   #
#####################################################

def saveToRCache(redditData, queryType):
    global rCacheDict
    if redditData is not None and queryType is not None and checkQueryType(queryType):
        rCacheDict[queryType] = redditData

def getFromRCache(queryType):
    global rCacheDict
    if queryType in rCacheDict:
        return rCacheDict[queryType]

def checkQueryType(queryType):
    return queryType == 'top' or \
           queryType == 'hot' or \
           queryType == 'new' or \
           queryType == 'rising' or \
           queryType == 'controversial'
