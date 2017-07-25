import global_helpers
import log_helpers
import json
import datetime_helpers

##########################################################################
##                                                                      ##
##                          Queries                                     ##
##                                                                      ##
##########################################################################

##
## [GET] Get a user's profile
##
def queryForUserProfile(userId):
    url = "https://api.spotify.com/v1/users/" + str(userId)
    return global_helpers.query_http(url, None, None, "Get user profile", 'GET')

##
## [GET] Given artist and song, search Spotify for top artist and song results
##
def queryForSearch(title, artist):
    url = "https://api.spotify.com/v1/search"
    searchParams = generateSearchParams(title, artist)
    requestHeader = None

    return global_helpers.query_http(url, searchParams, requestHeader, "Search query", 'GET')

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

    result = global_helpers.query_http(url, params, None, "Get my playlists query", 'GET')
    playlists = result['items']
    if 'next' in result:
        url = result['next']
    else:
        url = None

    while url is not None:
        additionalPlaylists = global_helpers.query_http(url, params, None, "Get additional my playlists", 'GET')
        playlists += additionalPlaylists['items']

        if 'next' in additionalPlaylists:
            url = additionalPlaylists['next']
        else:
            url = None

    return playlists

##
## [GET] Get specific playlist data
##
def queryForSelectedPlaylist(playlistId, userId):
    url = "https://api.spotify.com/v1/users/" + str(userId) + "/playlists/" + str(playlistId)
    playlistResult = global_helpers.query_http(url, None, None, "Get selected playlist query", 'GET')
    playlistTrackResult = playlistResult['tracks']

    while 'next' in playlistTrackResult and playlistTrackResult['next'] is not None:
        playlistTrackResult = global_helpers.query_http(playlistTrackResult['next'], None, None, "Additional playlist tracks", 'GET')
        playlistResult['tracks']['items'] += playlistTrackResult['items']

    return playlistResult

##
## [GET] Get a playlist's tracks
##
def queryForPlaylistTracks(ownerId, playlistId, fields):
    url = "https://api.spotify.com/v1/users/" + str(ownerId) + "/playlists/" + str(playlistId) + "/tracks"
    params = {'limit': 100}
    if fields is not None:
        params['fields'] = fields

    result = global_helpers.query_http(url, params, None, "Get playlist tracks query", 'GET')
    if 'next' in result:
        url = result['next']
    else:
        url = None

    while url is not None:
        additionalTracks = global_helpers.query_http(url, params, None, "Get additional playlist tracks", 'GET')
        result['items'] += additionalTracks['items']

        if 'next' in additionalTracks:
            url = additionalTracks['next']
        else:
            url = None

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

##
## [GET] Get audio features for several tracks
##
def queryForMultipleAudioFeatures(idList):
    url = "https://api.spotify.com/v1/audio-features"
    index = 0
    tieredList = []

    print str(len(idList)) + " -- length"

    while index < len(idList):
        idsToQuery = []
        for i in xrange(100):
            if (i + index) < len(idList):
                idsToQuery.append(idList[i+index])
            else:
                break

        print "Appending "

        tieredList.append(idsToQuery)
        index += 100

    audioFeaturesList = []
    for idListToQuery in tieredList:
        idListString = ','.join(str(x) for x in idListToQuery)
        params = {'ids': idListString}

        queryResult = global_helpers.query_http(url, params, None, "Get Audio Features", 'GET')
        audioFeaturesList += queryResult['audio_features']

    return audioFeaturesList

##
## [GET] Query for history, grabbing in bunches of 50 songs up to batches
##
def queryForSpotifyHistory(timestamp, batches):
    url = "https://api.spotify.com/v1/me/player/recently-played"
    params = {'limit': 50, 'before': timestamp}

    index = 0
    if batches > 20:
        return

    log_helpers.logGeneral("")

    totalResult = []
    while index < batches:
        print "Querying - " + str(url)
        print str(params)
        historyResult = global_helpers.query_http(url, params, None, "Get history", 'GET')
        totalResult += historyResult['items']

        log_helpers.logAppend(json.dumps(historyResult, indent=4))
        log_helpers.logAppend("\n\n\n\n====================\n\n\n\n\n")

        if len(historyResult['items']):
            latest = historyResult['items'][-2]['played_at']
            print "\tconverting " + str(latest)
            params['before'] = datetime_helpers.isoToEpoch(latest)

        index += 1

    return totalResult

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