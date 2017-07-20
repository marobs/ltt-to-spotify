import global_helpers
import json

##########################################################################
##                                                                      ##
##                          Queries                                     ##
##                                                                      ##
##########################################################################

##
## [GET] Given artist and song, search Spotify for top artist and song results
##
def queryForSearch(title, artist):
    url = "https://api.spotify.com/v1/search"
    searchParams = generateSearchParams(title, artist)
    requestHeader = None

    return global_helpers.query_http(url, searchParams, requestHeader, "Search query", "GET")

##
## [GET] Given initial Spotify data (a list of dicts including 'track' keys), get full track data for those tracks
##
def queryForFullTrackObjects(initialSpotifyData):
    ids = ""
    for result in initialSpotifyData:
        if 'track' in result:
            ids += result['track']['id'] + ","

    params = {'ids': ids[:-1]}
    url = "https://api.spotify.com/v1/tracks"
    requestHeader = None

    return global_helpers.query_http(url, params, requestHeader, "Full Track Query", 'GET')

##
## [GET] Given an artist id, get full track data for that artist's top song
##
def queryForArtistTopSong(artistId):
    url = "https://api.spotify.com/v1/artists/" + artistId + "/top-tracks"
    params = {'country': 'US'}
    requestHeader = None

    result = global_helpers.query_http(url, params, requestHeader, "Top tracks query", 'GET')

    if 'tracks' in result and len(result['tracks']) >= 1:
        return result['tracks'][0]

    return None


##
## [GET] Get all albums in albumList
##
def queryForAllAlbums(albumList):
    url = "https://api.spotify.com/v1/albums/?ids="
    for album in albumList:
        url += str(album) + ','
    url = url[:-1]
    requestHeader = None

    return global_helpers.query_http(url, None, requestHeader, "All albums query", 'GET')

##
## [GET] Get all artists in artistList
##
def queryForAllArtists(artistList):
    url = "https://api.spotify.com/v1/artists/?ids="
    for artist in artistList:
        url += str(artist) + ','
    url = url[:-1]
    requestHeader = None

    return global_helpers.query_http(url, None, requestHeader, "All artists query", 'GET')

##
## [GET] Get user playlists
##
def queryForUserPlaylists():
    url = "https://api.spotify.com/v1/me/playlists"
    params = {'limit': 50}
    requestHeader = None

    result = global_helpers.query_http(url, params, requestHeader, "Get my playlists query", 'GET')
    playlists = result['items']

    iteration = 1
    while len(playlists) == 50 * iteration:
        params = {'limit': 50, 'offset': 50 * iteration}
        result = global_helpers.query_http(url, params, requestHeader, "Get my playlists query", 'GET')

        if 'items' in result:
            playlists = playlists + result['items']

        iteration += 1

    return playlists

##
## [GET] Get specific playlist data
##
def queryForSelectedPlaylist(playlistId, userId):
    url = "https://api.spotify.com/v1/users/" + str(userId) + "/playlists/" + str(playlistId)
    params = {'fields': 'name,description,id,tracks.items(track(name,href,id,album(name,href,id),artists(name,href,id)))'}
    requestHeader = None

    return global_helpers.query_http(url, params, requestHeader, "Get selected playlist query", 'GET')

##
## [GET] Get a playlist's tracks
##
def queryForPlaylistTracks(ownerId, playlistId, fields):
    url = "https://api.spotify.com/v1/users/" + str(ownerId) + "/playlists/" + str(playlistId) + "/tracks"
    params = {'limit': 100}
    if fields is not None:
        params['fields'] = fields
    requestHeader = None

    result = global_helpers.query_http(url, params, None, "Get playlist tracks query", 'GET')

    while url is not None:
        additionalTracks = global_helpers.query_http(url, params, None, "Get additional playlist tracks", 'GET')
        result['items'] += additionalTracks['items']
        if 'next' in additionalTracks:
            url = additionalTracks['next']

    return result


##
## [POST] Add track to playlist
##
def postAddTrackRequest(playlistId, userId, trackURI, position):
    url = "https://api.spotify.com/v1/users/" + str(userId) + "/playlists/" + str(playlistId) + "/tracks"
    params = {'uris': [trackURI]}
    if position is not None:
        params['position'] = position
    requestHeader = {'Content-Type': 'application/json'}

    return global_helpers.query_http(url, params, requestHeader, "Add track post", 'POST')

##
## [DELETE] Remove track from playlist
##
def deleteRemoveTrackRequest(playlistId, userId, trackURI):
    url = "https://api.spotify.com/v1/users/" + str(userId) + "/playlists/" + str(playlistId) + "/tracks"
    params = {'uris': [trackURI]}
    requestHeader = {'Content-Type': 'application/json'}

    return global_helpers.query_http(url, params, requestHeader, "Add track post", 'DELETE')

##
## [PUT] Save track
##
def putSaveTrackRequest(ids):
    url = "https://api.spotify.com/v1/me/tracks"
    params = {'ids': ids}
    requestHeader = {'Content-Type': 'application/json'}

    return global_helpers.query_http(url, params, requestHeader, "Save track put", 'PUT')

##
## [DELETE] Unsave track
##
def deleteUnsaveTrackRequest(ids):
    url = "https://api.spotify.com/v1/me/tracks"
    params = {'ids': ids}
    requestHeader = {'Content-Type': 'application/json'}

    return global_helpers.query_http(url, params, requestHeader, "Unsave track delete", 'DELETE')


##
## [PUT] Reorder playlist
##
def reorderPlaylistRequest(userId, playlistId, rangeStart, rangeLength, insertBefore):
    url = "https://api.spotify.com/v1/users/" + str(userId) + "/playlists/" + str(playlistId) + "/tracks"
    params = {'range_start': rangeStart,
              'range_length': rangeLength,
              'insert_before': insertBefore}
    requestHeader = {'Content-Type': 'application/json'}

    return global_helpers.query_http(url, params, requestHeader, "Reorder playlist", 'PUT')

##########################################################################
##                                                                      ##
##                          Miscellaneous                               ##
##                                                                      ##
##########################################################################

# Print track information given (full) track object
def printTrack(track, extraData=None):
    print "\tTrack (" + str(extraData) + ")"
    print "\t  Name: " + track['name'].encode("utf8")

    artistString = track['artists'][0]['name'].encode("utf8")
    for i in xrange(1, len(track['artists']) - 1):
        artistString = artistString + "," + track['artists'][i]['name'].encode("utf8")
    print "\t  Artist(s): " + artistString

    print "\t  Album: " + str(track['album']['name'].encode("utf8"))
    print "\t  Duration: " + str(track['duration_ms'])

# Print artist information given artist object
def printArtist(artist, extraData=None):
    print "Artist (" + str(extraData) + ")"
    print "\tArtist: " + artist['name'].encode("utf8")
    print "\t  Genres: " + artist['genres'].encode("utf8")

def generateSearchParams(title, artist):
    keyword = 'track:"' + title.encode('utf-8') + '" artist:"' + artist.encode('utf-8') + '"'
    spotifyType = "track"

    return {'q': keyword,
            'type': spotifyType,
            'limit': '4'}