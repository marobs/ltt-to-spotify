import helpers

MAX_QUERIED_TRACKS = 50

def replaceTrackObjects(spotifyData):
    trackIdList = generateTrackIdList(spotifyData)
    trackResults = queryForTracks(trackIdList)

    for track in trackResults:
        emplaceTrackResult(track, spotifyData)

def generateTrackIdList(spotifyData):
    trackSet = set()
    for spotifyEntry in spotifyData:
        trackSet.add(spotifyEntry['track'])

    return trackSet

def queryForTracks(trackIdList):
    trackIdSet = list(set(trackIdList))
    queriedTracks = []
    index = 0

    while index < len(trackIdSet):
        queryIds = trackIdSet[index:index+MAX_QUERIED_TRACKS]
        trackResults = helpers.queryForFullTrackObjects(queryIds)

        if trackResults is None:
            return queriedTracks

        else:
            queriedTracks += trackResults

        index += MAX_QUERIED_TRACKS

def emplaceTrackResult(track, spotifyData):
    found = False
    for spotifyEntry in spotifyData:
        if spotifyEntry['track']['id'] == track['id']:
            track['redditData'] = spotifyEntry['track']['redditData']
            track['top'] = spotifyEntry['top']
            track['isTop'] = spotifyEntry['isTop']

            spotifyEntry['track'] = track
            found = True

    if not found:
        print "NO MATCH FOUND - Track"
