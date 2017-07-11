cacheDict = {}

def saveToCache(spotifyTrack, topTrack):
    global cacheDict

    trackId = spotifyTrack['id']
    cacheDict[trackId] = spotifyTrack

    if topTrack is not None:
        topId = topTrack['id']
        cacheDict[topId] = topTrack

def getFromCache(trackId):
    global cacheDict

    if trackId in cacheDict:
        return cacheDict[trackId]

    else:
        return None