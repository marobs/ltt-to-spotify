import requests
import urllib
import helpers

#############################################################
#                                                           #
#                   Track Data                              #
#                                                           #
#############################################################

def searchSpotify(postList):
    spotifyData = []
    for post in postList:
        spotifyData.append(searchForPost(post))

    replaceTrackObjects(spotifyData)
    fillWithArtistTopSongs(spotifyData)

    return spotifyData

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
                if topSong is not None and topSong['id'] != result['track']['id']:
                    result['top'] = topSong

#############################################################
#                                                           #
#                   Playlist Data                           #
#                                                           #
#############################################################

def getUserPlaylists():
    return helpers.queryForUserPlaylists()


def printUserPlaylists(playlists):
    for playlist in playlists:
        if 'name' in playlist:
            print "   " + playlist['name'].encode('utf8')

        if 'tracks' in playlist:
            print "   " + str(playlist['tracks'])

        print "\n"


def getSelectedPlaylist(playlist):
    if 'id' in playlist and 'owner' in playlist and 'id' in playlist['owner']:
        playlistId = playlist['id']
        userId = playlist['owner']['id']
        return helpers.queryForSelectedPlaylist(playlistId, userId)

    return None
