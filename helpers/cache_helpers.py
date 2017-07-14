from global_helpers import basePath
import cPickle
import os.path
import json


###
### Objects
###

notFoundValue = "VALUE_NOT_FOUND"
rCacheDict = {}
sCacheDict = {}
sCachePath = basePath + '/../cache/spotifyCache.pkl'

#####################################################
#                                                   #
#                   Spotify                         #
#                                                   #
#####################################################

# Need to cache by reddit title/artist to get benefit out of caching (don't have to search)
# Also need to cache by id? Not sure
# Should cache top songs as well but those won't be cached by reddit post
# Add reddit data and top song data to reddit songs to be able to grab the top song with just the other one?
# Think about when stuff is needed/not needed/inputs/outputs/etc

def saveToSCacheByKeyList(spotifyTrack, keyList):
    print "Saving spotify track data to SCache"
    global sCacheDict

    for key in keyList:
        print "    Saving track by id " + str(key)
        if spotifyTrack is not None:
            sCacheDict[str(key)] = dict(spotifyTrack)
        else:
            sCacheDict[str(key)] = None

def getFromSCache(trackId):
    print "Grabbing spotify track id <" + str(trackId) + "> from SCache"
    global notFoundValue
    global sCacheDict

    if trackId in sCacheDict:
        print "    Found track"
        if sCacheDict[trackId] is not None:
            return sCacheDict[trackId]

        else:  # Not found entry
            return notFoundValue

    else:
        return None

def initializeSCache():
    print "Initializing SCache"
    global sCacheDict

    if not os.path.isfile(sCachePath):
        return {}

    with open(sCachePath, 'rb') as f:
        obj = cPickle.load(f)

        print "Loaded Spotify Cache: "
        print json.dumps(obj, indent=4)

        if obj is not None:
            sCacheDict = obj

        else:
            sCacheDict = {}

def flushSCache():
    print "Saving SCache to file"
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
    print "Saving data to RCache"
    global rCacheDict

    if redditData is not None and queryType is not None and checkQueryType(queryType):
        rCacheDict[str(queryType)] = list(redditData)

def getFromRCache(queryType):
    print "Grabbing data from RCache for query " + str(queryType)
    global rCacheDict
    if queryType in rCacheDict:
        return list(rCacheDict[queryType])

def checkQueryType(queryType):
    return queryType == 'top' or \
           queryType == 'hot' or \
           queryType == 'new' or \
           queryType == 'rising' or \
           queryType == 'controversial'
