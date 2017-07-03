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
    requestHeader = {'Authorization': accessToken}
    searchParams = generateSearchParams(post)
    searchResults = requests.get("https://api.spotify.com/v1/search", params=searchParams, headers=requestHeader)

    if searchResults.status_code != requests.codes.ok:
        print "Error: search status code not ok! Status code: " + str(searchResults.status_code)

    return getMatchingTracks(searchResults)
    # Find matching artist and song
    # Search for artist, get genre and top song

def generateSearchParams(post):
    keyword = "track:" + post["title"].encode('utf-8') + " artist:" + post["artist"].encode('utf-8')
    keyword = urllib.quote(keyword)
    type = urllib.quote("track,artist")

    return {'q': keyword,
            'type': type,
            'limit': '10'}

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
    tracks = []
    artists = []

    for result in searchResults:
        if result['type'] == 'track':
            tracks.append(result)

        elif result['type'] == 'artist':
            artists.append(result)

        else:
            print "Error: Unknown type of result found"

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





