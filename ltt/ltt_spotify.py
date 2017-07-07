import requests
import urllib
import helpers

#############################################################
#                                                           #
#                   Fill spotifyData                        #
#                                                           #
#############################################################

def searchSpotify(postList):
    spotifyData = []
    for post in postList:
        spotifyEntry = searchForPost(post)
        if 'track' in spotifyEntry:
            spotifyEntry['track']['redditGenres'] = post['genre']

        spotifyData.append(spotifyEntry)

    replaceTrackObjects(spotifyData)
    albumList, artistList = fillWithArtistTopSongs(spotifyData)
    replaceAlbumObjects(spotifyData, albumList)
    addArtistObjects(spotifyData, artistList)
    collectPostGenres(spotifyData)

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
    artistList = []

    # For each track, save album and artist and query for that artist's top song
    for entry in spotifyData:
        if 'track' in entry:
            if 'album' in entry['track']:
                albumList.append(entry['track']['album']['id'])

            # If artist exists, query for top song
            if 'artists' in entry['track'] and len(entry['track']['artists']):
                artistList.append(entry['track']['artists'][0]['id'])
                topSong = helpers.queryForArtistTopSong(entry['track']['artists'][0]['id'])

                # If top song is different than reddit track, save to entry['top'] and save album id
                if topSong is not None and topSong['id'] != entry['track']['id']:
                    entry['top'] = topSong

                    if 'album' in topSong and topSong['album']['id'] not in albumList:
                        albumList.append(topSong['album']['id'])

    return albumList, artistList

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

# Add artist data to each spotify post
def addArtistObjects(spotifyData, artistList):
    artistResults = helpers.queryforAllArtists(artistList)

    if artistResults is not None:
        for result in artistResults:
            for entry in spotifyData:
                if 'track' in entry and 'artists' in entry['track'] and len(entry['track']['artists']):
                    if result['id'] == entry['track']['artists'][0]['id']:
                        entry['artist'] = result

def collectPostGenres(spotifyData):
    for post in spotifyData:
        if 'track' in post and 'album' in post['track']:
            post['track']['genres'] = post['track']['album']['genres']
            post['genres'] += splitRedditGenres(post['track']['redditGenres'])

def splitRedditGenres(genreString):
    if genreString is None:
        return ["hi"]


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

def trimLTTObjects(spotifyTracks, userPlaylists):
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

