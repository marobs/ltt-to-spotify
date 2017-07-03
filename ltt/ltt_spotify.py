import requests
import urllib
import helpers

def searchSpotify(postList, accessToken):
    spotifyData = []
    for post in postList:
        spotifyData.append(searchForPost(post))


    print "SpotifyData:"
    for data in spotifyData:
        print "Item: "
        for i in data:
            print "\t" + i + ":"
            for j in data[i]:
                print "\t\t" + j + ": " + str(data[i][j])


    replaceTrackObjects(spotifyData)
    fillWithArtistTopSongs(spotifyData)

    printSpotifyData(spotifyData)


def printSpotifyData(spotifyData):
    for data in spotifyData:
        if 'track' in data:
            helpers.printTrack(data['track'], 'track')

        if 'matchingAritst' in data:
            helpers.printArtist(data['matchingArtist'], 'matchingArtist')

        if 'matchingTrack' in data:
            helpers.printTrack(data['matchingTrack'], 'matchingTrack')

        if 'otherArtist' in data:
            helpers.printArist(data['otherArtist'], 'otherArtist')

        if 'otherTrack' in data:
            helpers.printTrack(data['otherTrack'], 'otherTrack')


def searchForPost(post):
    searchResults = helpers.queryForSearch(post['title'], post['artist'])
    return getMatchingTracks(searchResults)


def getMatchingTracks(searchResults):
    tracks = None
    if 'tracks' in searchResults:
        if 'items' in searchResults['tracks']:
            tracks = searchResults['tracks']['items']

    print "Tracks: " + str(tracks)

    match = {}
    if len(tracks):
        match['track'] = tracks[0]

    return match

def replaceTrackObjects(initialResults):
    trackResults = helpers.queryForFullTrackObjects(initialResults)
    if trackResults is None:
        return

    # TODO: Horrible runtime, improve if motivated
    for trackResult in trackResults:
        for initialResult in initialResults:
            if 'track' in initialResult and initialResult['track']['id'] == trackResult['id']:
                initialResult['track'] = trackResult


def fillWithArtistTopSongs(initialResults):
    for result in initialResults:
        if 'track' in result:
            if 'artists' in result['track'] and len(result['track']['artists']):
                result['top'] = helpers.queryForArtistTopSong(result['track']['artists'][0]['id'])
