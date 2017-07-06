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
    albumList = fillWithArtistTopSongs(spotifyData)
    replaceAlbumObjects(spotifyData, albumList)


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
        return None

    # TODO: Horrible runtime, improve if motivated
    for trackResult in trackResults['tracks']:
        for initialResult in initialResults:
            if 'track' in initialResult and initialResult['track']['id'] == trackResult['id']:
                initialResult['track'] = trackResult
                continue

def replaceAlbumObjects(spotifyData, albumList):
    index = 0
    while (index + 20) < len(albumList):
        queryIds = albumList[index:index+20]
        albumResults = helpers.queryForAllAlbums(queryIds)
        if albumResults is None:
            continue

        for albumResult in albumResults:
            for spotifyObj in spotifyData:
                if 'track' in spotifyObj:
                    if 'album' in spotifyObj['track'] and spotifyObj['track']['album']['id'] == albumResult['id']:
                        spotifyObj['track']['album'] = albumResult
                        continue

                if 'top' in spotifyObj:
                    if 'album' in spotifyObj['top'] and spotifyObj['top']['album']['id'] == albumResult['id']:
                        spotifyObj['top']['album'] = albumResult

        index += 20

def fillWithArtistTopSongs(spotifyData):
    albumList = []

    for entry in spotifyData:
        if 'track' in entry:
            if 'album' in entry['track']:
                albumList.append(entry['track']['album']['id'])

            if 'artists' in entry['track'] and len(entry['track']['artists']):
                topSong = helpers.queryForArtistTopSong(entry['track']['artists'][0]['id'])
                if topSong is not None and topSong['id'] != entry['track']['id']:
                    entry['top'] = topSong

                    if 'album' in topSong and topSong['album']['id'] not in albumList:
                        albumList.append(topSong['album']['id'])

    return albumList

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
