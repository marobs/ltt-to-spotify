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

def fillWithArtistTopSongs(spotifyData):
    albumList = []

    # For each track, save album to albumList and query for the corresponding artist's top song
    for entry in spotifyData:
        if 'track' in entry:
            if 'album' in entry['track']:
                albumList.append(entry['track']['album']['id'])

            # If artist exists, query for top song
            if 'artists' in entry['track'] and len(entry['track']['artists']):
                topSong = helpers.queryForArtistTopSong(entry['track']['artists'][0]['id'])

                # If top song is different than reddit track, save to entry['top'] and save album id
                if topSong is not None and topSong['id'] != entry['track']['id']:
                    entry['top'] = topSong

                    if 'album' in topSong and topSong['album']['id'] not in albumList:
                        albumList.append(topSong['album']['id'])

    return albumList

# Given a list of albums in spotifyData, replace spotifyData album objects with corresponding full album objects
def replaceAlbumObjects(spotifyData, albumList):
    index = 0
    while (index + 20) < len(albumList):
        queryIds = albumList[index:index+20]
        albumResults = helpers.queryForAllAlbums(queryIds)
        if albumResults is None:
            continue

        for albumResult in albumResults:
            emplaceAlbumResult(albumResult, spotifyData)

        index += 20

# Given a full album object, replace the corresponding simple album object in the spotifyData
def emplaceAlbumResult(albumResult, spotifyData):
    for spotifyObj in spotifyData:

        # Check if album corresponds to reddit suggestion
        if 'track' in spotifyObj:
            if 'album' in spotifyObj['track'] and spotifyObj['track']['album']['id'] == albumResult['id']:
                spotifyObj['track']['album'] = albumResult
                continue

        # Check if labum corresponds to artist top song
        if 'top' in spotifyObj:
            if 'album' in spotifyObj['top'] and spotifyObj['top']['album']['id'] == albumResult['id']:
                spotifyObj['top']['album'] = albumResult

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


#############################################################
#                                                           #
#                      Trim Data                            #
#                                                           #
#############################################################
def trimLTTObjects(spotifyTracks, userPlaylists, selectedPlaylist):
    for spotifyObj in spotifyTracks:
        if 'track' in spotifyObj:
            trimTrackObject(spotifyObj['track'])

        if 'top' in spotifyObj:
            trimTrackObject(spotifyObj['top'])

    for playlist in userPlaylists:
        del (playlist['external_urls'])

def trimTrackObject(trackObj):
    del (trackObj['album']['available_markets'])
    del (trackObj['album']['copyrights'])
    del (trackObj['album']['external_ids'])
    del (trackObj['album']['external_urls'])
    del (trackObj['album']['tracks'])
    del (trackObj['album']['type'])
    del (trackObj['available_markets'])
    del (trackObj['external_ids'])
    del (trackObj['external_urls'])
    del (trackObj['linked_from'])

