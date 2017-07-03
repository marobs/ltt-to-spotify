import requests

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


# Given initial Spotify data (a list of dicts including 'track' keys), get full track data for those tracks
def queryForFullTrackObjects(initialSpotifyData, accessToken):
    ids = ""
    for result in initialSpotifyData:
        if 'track' in result:
            ids += result['track']['id'] + ","

    params = {'ids': ids[:-1]}
    requestHeader = {'Authorization': accessToken}
    trackResults = requests.get("https://developer.spotify.com/web-api/get-several-tracks/",
                                params=params,
                                headers=requestHeader)

    if trackResults.status_code != requests.codes.ok:
        print "Error: track search code not ok! Status code: " + str(trackResults.status_code)
        return None

    return trackResults

# Given an artist id, get full track data for that artist's top song
def queryForArtistTopSong(artistId, accessToken):
    requestHeader = {'Authorization': accessToken}
    url = "https://api.spotify.com/v1/artists/" + artistId + "/top-tracks"
    result = requests.get(url, headers=requestHeader)

    if result.status_code != requests.codes.ok:
        print "Error: top tracks request status code not ok! Status code:" + str(result.status_code)
        return None

    else:
        if 'tracks' in result and len(result['tracks']) >= 1:
            return result['tracks'][0]

