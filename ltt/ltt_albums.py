import helpers

MAX_QUERIED_ALBUMS = 20

def replaceAlbumObjects(spotifyData):
    albumIdSet = generateAlbumIdSet(spotifyData)
    albumResults = queryForAlbums(albumIdSet)

    for album in albumResults:
        emplaceAlbumResult(album, spotifyData)

def generateAlbumIdSet(spotifyData):
    albumSet = set()

    for spotifyEntry in spotifyData:
        if 'album' in spotifyEntry['track']:
            albumSet.add(spotifyEntry['track']['album']['id'])

        if 'top' in spotifyEntry and 'album' in spotifyEntry['top']:
            albumSet.add(spotifyEntry['top']['album']['id'])

    return list(albumSet)

def queryForAlbums(albumIdList):
    albumIdSet = list(set(albumIdList))
    queriedAlbums = []
    index = 0
    while index < len(albumIdSet):
        queryIds = albumIdSet[index:index+MAX_QUERIED_ALBUMS]
        albumResults = helpers.queryForAllAlbums(queryIds)

        if albumResults is None:
            return queriedAlbums

        else:
            queriedAlbums += albumResults

        index += MAX_QUERIED_ALBUMS

def emplaceAlbumResult(albumResult, spotifyData):
    found = False
    for spotifyEntry in spotifyData:
        if 'album' in spotifyEntry['track'] and spotifyEntry['track']['album']['id'] == albumResult['id']:
            spotifyEntry['track']['album'] = albumResult
            found = True

        if 'top' in spotifyEntry:
            if 'album' in spotifyEntry['top'] and spotifyEntry['top']['album']['id'] == albumResult['id']:
                spotifyEntry['top']['album'] = albumResult
                found = True

    if not found:
        print "NO MATCH FOUND - Album"
