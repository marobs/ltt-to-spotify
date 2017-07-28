import helpers
import json

MAX_QUERIED_TRACKS = 50

def replaceTrackObjects(spotifyData):
    trackIdList = generateTrackIdList(spotifyData)
    trackResults = queryForTracks(trackIdList)

    for track in trackResults:
        print json.dumps(track, indent=4)
        emplaceTrackResult(track, spotifyData)

def generateTrackIdList(spotifyData):
    trackSet = set()
    for spotifyEntry in spotifyData:
        trackSet.add(spotifyEntry['track']['id'])

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
            queriedTracks += trackResults['tracks']

        index += MAX_QUERIED_TRACKS

    return queriedTracks

def emplaceTrackResult(track, spotifyData):
    found = False
    for spotifyEntry in spotifyData:
        if spotifyEntry['track']['id'] == track['id']:
            track['redditData'] = spotifyEntry['track']['redditData']
            track['top'] = spotifyEntry['track']['top']
            track['isTop'] = spotifyEntry['track']['isTop']

            spotifyEntry['track'] = track
            found = True

    if not found:
        print "NO MATCH FOUND - Track"
