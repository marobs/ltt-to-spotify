from ltt_albums import *
from ltt_artists import *
import helpers

#############################################################
#                                                           #
#                   Fill spotifyData                        #
#                                                           #
#############################################################

def generateSpotifyData(postList):
    remainingPosts, cachedEntries = helpers.getCachedEntries(postList)

    spotifyData = []
    notFoundIds = set()
    for post in remainingPosts:
        spotifyEntry = searchForPost(post)
        if spotifyEntry:
            spotifyEntry['track']['redditData'] = post
            spotifyData.append(spotifyEntry)
            print "Found Spotify entry for -- " + str(post['rawTitle'].encode('utf8'))

        else:
            notFoundIds.add(post['redditId'])

    print "Got base spotify objects"

    if len(spotifyData):
        replaceTrackObjects(spotifyData)
        print "Replaced track objects"

        fillWithArtistTopSongs(spotifyData)
        print "Got top song data"

        replaceAlbumObjects(spotifyData)
        print "Got album objects"

        replaceArtistObjects(spotifyData)
        print "Got artist objects"

        collectPostGenres(spotifyData)
        print "Collected genre information"

    spotifyData += cachedEntries
    helpers.cacheSpotifyData(spotifyData, list(notFoundIds))

    return spotifyData

##
## Search
##
def searchForPost(post):
    searchResults = helpers.queryForSearch(post['title'], post['artist'])
    return getMatchingTrack(searchResults)

def getMatchingTrack(searchResults):
    tracks = None
    if 'tracks' in searchResults:
        if 'items' in searchResults['tracks']:
            tracks = searchResults['tracks']['items']

    match = {}
    if len(tracks):
        match['track'] = tracks[0]

    return match

##
## Tracks
##
def replaceTrackObjects(spotifyData):
    trackResults = helpers.queryForFullTrackObjects(spotifyData)

    if trackResults is None:
        return None

    for trackResult in trackResults['tracks']:
        for initialResult in spotifyData:
            if 'track' in initialResult and initialResult['track']['id'] == trackResult['id']:
                trackResult['redditData'] = initialResult['track']['redditData']
                initialResult['track'] = trackResult

def fillWithArtistTopSongs(spotifyData):
    for entry in spotifyData:
        # If artist exists, query for top song
        if 'artists' in entry['track'] and len(entry['track']['artists']):

            print "Querying for artist: " + str(entry['track']['artists'][0]['name']) + " -- " + str(entry['track']['artists'][0]['id'].encode('utf8'))
            topSong = helpers.queryForArtistTopSong(entry['track']['artists'][0]['id'])

            # If top song is different than reddit track, save to entry['top'] and save album id
            if topSong is not None:
                if topSong['id'] == entry['track']['id'] or topSong['name'] == entry['track']['name']:
                    entry['track']['top'] = None
                    entry['track']['isTop'] = True

                else:
                    entry['top'] = topSong
                    entry['track']['top'] = topSong['id']
                    entry['track']['isTop'] = False

            else:
                print "No top song."
                entry['track']['top'] = None
                entry['track']['isTop'] = False

##
## GENRES
##
def collectPostGenres(spotifyData):
    for spotifyEntry in spotifyData:

        # Grab artist's genres for basis of 'track' and 'top'
        spotifyGenres = set()
        if 'artist' in spotifyEntry:
            spotifyGenres.update(spotifyEntry['artist']['genres'])

        # For 'track' in entry
        if 'track' in spotifyEntry:
            spotifyEntry['track']['genres'] = set(spotifyGenres)
            spotifyEntry['track']['genres'].update(spotifyEntry['track']['artist']['genres'])
            spotifyEntry['track']['genres'].update(spotifyEntry['track']['album']['genres'])

            redditGenres = helpers.splitRedditGenres(spotifyEntry['track']['redditData']['genre'])
            spotifyEntry['track']['genres'].update(redditGenres)

            genreList = list(spotifyEntry['track']['genres'])
            spotifyEntry['track']['genres'] = helpers.categorizeGenres(genreList)

        # If different top artist song
        if 'top' in spotifyEntry:
            spotifyEntry['top']['genres'] = set(spotifyGenres)
            spotifyEntry['top']['genres'].update(spotifyEntry['top']['artist']['genres'])
            spotifyEntry['top']['genres'].update(spotifyEntry['top']['album']['genres'])

            genreList = list(spotifyEntry['top']['genres'])
            spotifyEntry['top']['genres'] = helpers.categorizeGenres(genreList)
