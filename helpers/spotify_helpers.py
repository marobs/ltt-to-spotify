import requests
import global_helpers
import urllib

# Print track information given (full) track object
def printTrack(track, extraData=None):
    print "\tTrack (" + str(extraData) + ")"
    print "\t  Name: " + track['name']

    artistString = track['artists'][0]['name']
    for i in xrange(1, len(track['artists']) - 1):
        artistString.append("," + track['artists'][i]['name'])
    print "\t  Artist(s): " + artistString

    print "\t  Album: " + track['album']
    print "\t  Duration: " + str(track['duration'])


# Print artist information given artist object
def printArtist(artist, extraData=None):
    print "Artist (" + str(extraData) + ")"
    print "\tArtist: " + artist['name']
    print "\t  Genres: " + artist['genres']


# Given artist and song, search Spotify for top artist and song results
def queryForSearch(title, artist):
    searchParams = generateSearchParams(title, artist)
    return global_helpers.query_get("https://api.spotify.com/v1/search", searchParams, "Search query")

def generateSearchParams(title, artist):
    keyword = 'track:"' + title.encode('utf-8') + '" artist:"' + artist.encode('utf-8') + '"'
    type = "track,artist"

    return {'q': keyword,
            'type': type,
            'limit': '10'}


# Given initial Spotify data (a list of dicts including 'track' keys), get full track data for those tracks
def queryForFullTrackObjects(initialSpotifyData):
    ids = ""
    for result in initialSpotifyData:
        if 'track' in result:
            ids += result['track']['id'] + ","

    params = {'ids': ids[:-1]}
    url = "https://developer.spotify.com/web-api/get-several-tracks/"
    return global_helpers.query_get(url, params, "Full Track Query")


# Given an artist id, get full track data for that artist's top song
def queryForArtistTopSong(artistId, accessToken):
    url = "https://api.spotify.com/v1/artists/" + artistId + "/top-tracks"
    result = global_helpers.query_get(url, None, "Top tracks query")

    if 'tracks' in result and len(result['tracks']) >= 1:
        return result['tracks'][0]

    else:
        return None
