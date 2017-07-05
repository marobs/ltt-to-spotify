import global_helpers
import json

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


# Given artist and song, search Spotify for top artist and song results
def queryForSearch(title, artist):
    searchParams = generateSearchParams(title, artist)
    return global_helpers.query_get("https://api.spotify.com/v1/search", searchParams, "Search query")

def generateSearchParams(title, artist):
    keyword = 'track:"' + title.encode('utf-8') + '" artist:"' + artist.encode('utf-8') + '"'
    spotifyType = "track"

    return {'q': keyword,
            'type': spotifyType,
            'limit': '10'}

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
    return global_helpers.query_get(url, params, "Full Track Query")


##
## [GET] Given an artist id, get full track data for that artist's top song
##
def queryForArtistTopSong(artistId):
    url = "https://api.spotify.com/v1/artists/" + artistId + "/top-tracks"
    params = {'country': 'US'}
    result = global_helpers.query_get(url, params, "Top tracks query")

    if 'tracks' in result and len(result['tracks']) >= 1:
        return result['tracks'][0]

    return None


##
## [GET] Get user playlists
##
def queryForUserPlaylists():
    url = "https://api.spotify.com/v1/me/playlists"
    params = {'limit': 50}
    result = global_helpers.query_get(url, params, "Get my playlists query")
    playlists = result['items']

    iteration = 1
    while len(playlists) == 50 * iteration:
        params = {'limit': 50, 'offset': 50 * iteration}
        result = global_helpers.query_get(url, params, "Get my playlists query")

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
    result = global_helpers.query_get(url, params, "Get selected playlist query")

    return result

##
## [POST] Add track to playlist
##
def postAddTrackRequest(playlistId, userId, trackURI):
    url = "https://api.spotify.com/v1/users/" + str(userId) + "/playlists/" + str(playlistId) + "/tracks"
    params = {'uris': [trackURI]}
    requestHeader = {'Content-Type': 'application/json'}

    result = global_helpers.query_post(url, params, requestHeader, "Add track post")
    return result

##
## [DELETE] Remove track from playlist
##
def deleteRemoveTrackRequest(playlistId, userId, trackURI):
    url = "https://api.spotify.com/v1/users/" + str(userId) + "/playlists/" + str(playlistId) + "/tracks"
    params = {'uris': [trackURI]}
    requestHeader = {'Content-Type': 'application/json'}

    result = global_helpers.query_delete(url, params, requestHeader, "Add track post")
    return result
