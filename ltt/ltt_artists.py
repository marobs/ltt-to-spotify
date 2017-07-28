import helpers

MAX_QUERIED_ARTISTS = 50

def replaceArtistObjects(spotifyData):
    artistList = generateArtistIdList(spotifyData)
    artistResults = queryForArtists(artistList)

    for artist in artistResults:
        emplaceArtistResult(artist, spotifyData)

def generateArtistIdList(spotifyData):
    artistSet = set()

    for spotifyEntry in spotifyData:
        if 'artists' in spotifyEntry['track'] and len(spotifyEntry['track']['artists']):
            artistSet.add(spotifyEntry['track']['artists'][0]['id'])

        if 'top' in spotifyEntry and 'artist' in spotifyEntry['top'] and len(spotifyEntry['top']['artists'][0]):
            artistSet.add(spotifyEntry['top']['artists'][0]['id'])

    return list(artistSet)

def queryForArtists(artistIdList):
    artistIdSet = list(set(artistIdList))
    queriedArtists = []
    index = 0
    while index < len(artistIdSet):
        queryIds = artistIdSet[index:index+MAX_QUERIED_ARTISTS]
        artistResults = helpers.queryForAllArtists(queryIds)

        if artistResults is None:
            return queriedArtists

        else:
            queriedArtists += artistResults

        index += MAX_QUERIED_ARTISTS

    return queriedArtists

def emplaceArtistResult(artistResult, spotifyData):
    found = False
    for spotifyEntry in spotifyData:
        if 'artists' in spotifyEntry['track'] and artistResult['id'] == spotifyEntry['track']['artists'][0]['id']:
            spotifyEntry['track']['artist'] = artistResult
            found = True

        if 'top' in spotifyEntry:
            if 'artists' in spotifyEntry['top'] and artistResult['id'] == spotifyEntry['top']['artists'][0]['id']:
                spotifyEntry['top']['artist'] = artistResult
                found = True

    if not found:
        print "NO MATCH FOUND - Artist"

