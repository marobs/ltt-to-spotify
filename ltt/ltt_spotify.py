import requests
import urllib
import helpers

def searchSpotify(postList, accessToken):
    spotifyData = []
    for post in postList:
        spotifyData.append(searchForPost(post, accessToken))

    replaceTrackObjects(spotifyData, accessToken)
    fillWithArtistTopSongs(spotifyData, accessToken)

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


def searchForPost(post, accessToken):
    searchResults = helpers.queryForSearch(post['title'], post['artist'])

    print "SEARCH RESULTS: "
    print str(searchResults)

    return getMatchingTracks(searchResults)


def getMatchingTracks(searchResults):
    tracks, artists = splitTracksAndArtists(searchResults)

    matches = {}
    if len(tracks):
        matches['track'] = tracks[0]

        for artist in artists:
            if artist['id'] == tracks[0]['artists'][0]['id']:
                matches['matchingArtist'] = tracks[0]['artists'][0]['id']
                matches['matchingArtist']

    if len(artists):
        # All results artists or no matching artists found for track
        if 'track' in matches:
            if 'matchingArtist' in matches:
                if artists[0]['id'] == matches['matchingArtist']:
                    return matches

        matches['otherArtist'] = artists[0]

def splitTracksAndArtists(searchResults):
    tracks = searchResults['tracks']['items']
    artists = searchResults['artists']['items']

    return tracks, artists


def replaceTrackObjects(initialResults, accessToken):
    trackResults = helpers.queryForFullTrackObjects(initialResults, accessToken)
    if trackResults is None:
        return

    # TODO: Horrible runtime, improve if motivated
    for trackResult in trackResults:
        for initialResult in initialResults:
            if 'track' in initialResult and initialResult['track']['id'] == trackResult['id']:
                initialResult['track'] = trackResult


def fillWithArtistTopSongs(initialResults, accessToken):
    for result in initialResults:
        if 'matchingArtist' in result:
            result['matchingTrack'] = helpers.queryForArtistTopSong(result['matchingArtist']['id'], accessToken)

        if 'otherArtist' in result:
            result['otherTrack'] = helpers.queryForArtistTopSong(result['otherArtist']['id'], accessToken)





