import requests
import urllib
import helpers

def searchSpotify(postList):
    spotifyData = []
    for post in postList:
        spotifyData.append(searchForPost(post))

    replaceTrackObjects(spotifyData)
    fillWithArtistTopSongs(spotifyData)

    printSpotifyData(spotifyData)


def printSpotifyData(spotifyData):

    print "Printing Spotify Data"

    for data in spotifyData:
        if 'track' in data:
            helpers.printTrack(data['track'], 'track')

        if 'top' in data:
            helpers.printTrack(data['top'], 'top')

        print "\n"

def searchForPost(post):
    searchResults = helpers.queryForSearch(post['title'], post['artist'])
    return getMatchingTracks(searchResults)


def getMatchingTracks(searchResults):
    tracks = None
    if 'tracks' in searchResults:
        if 'items' in searchResults['tracks']:
            tracks = searchResults['tracks']['items']

    match = {}
    if len(tracks):
        match['track'] = tracks[0]

    return match

def replaceTrackObjects(initialResults):
    trackResults = helpers.queryForFullTrackObjects(initialResults)
    if trackResults is None:
        return

    # TODO: Horrible runtime, improve if motivated
    for trackResult in trackResults['tracks']:
        for initialResult in initialResults:
            if 'track' in initialResult and initialResult['track']['id'] == trackResult['id']:
                initialResult['track'] = trackResult


def fillWithArtistTopSongs(initialResults):
    for result in initialResults:
        if 'track' in result:
            if 'artists' in result['track'] and len(result['track']['artists']):
                topSong = helpers.queryForArtistTopSong(result['track']['artists'][0]['id'])
                if topSong['id'] != result['track']['id']:
                    result['top'] = topSong
