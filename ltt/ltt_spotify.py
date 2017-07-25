from __future__ import division
import helpers
import json


#############################################################
#                                                           #
#                   Fill spotifyData                        #
#                                                           #
#############################################################

def generateSpotifyData(postList):
    spotifyData = []
    remainingPosts, cachedEntries, notFoundIds = getCachedEntries(postList)

    for post in remainingPosts:
        spotifyEntry = searchForPost(post)
        if spotifyEntry:
            spotifyEntry['track']['redditData'] = post
            try:
                print "Found Spotify entry for -- " + str(post['rawTitle'])
            except UnicodeEncodeError:
                print "Foudn Spotify entry for -- " + post['rawTitle'].encode('utf-8')
            spotifyData.append(spotifyEntry)
        else:
            notFoundIds.add(post['redditId'])

    print "Got base spotify objects"

    if len(spotifyData):
        replaceTrackObjects(spotifyData)
        print "Replaced track objects"

        albumList, artistList = fillWithArtistTopSongs(spotifyData)
        print "Got top song data"

        if len(albumList):
            replaceAlbumObjects(spotifyData, albumList)
            print "Got album objects"

        if len(artistList):
            replaceArtistObjects(spotifyData, artistList)
            print "Got artist objects"

        collectPostGenres(spotifyData)
        print "Collected genre information"

    spotifyData += cachedEntries
    logSpotifyData(spotifyData)
    prepareAndCacheSpotifyData(spotifyData, list(notFoundIds))

    return spotifyData

def printSpotifyData(spotifyData):
    print "Printing Spotify Data"
    print json.dumps(spotifyData, indent=2)

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
## TRACKS
##
def replaceTrackObjects(spotifyData):
    trackResults = helpers.queryForFullTrackObjects(spotifyData)

    if trackResults is None:
        return None

    for trackResult in trackResults['tracks']:
        for initialResult in spotifyData:
            if 'track' in initialResult and initialResult['track']['id'] == trackResult['id']:
                redditData = initialResult['track']['redditData']
                initialResult['track'] = buildTrackObject(trackResult, redditData)

def fillWithArtistTopSongs(spotifyData):
    albumList = []
    artistList = []

    # For each track, save album and artist and query for that artist's top song
    for entry in spotifyData:
        if 'album' in entry['track']:
            albumList.append(entry['track']['album']['id'])

        # If artist exists, query for top song
        if 'artists' in entry['track'] and len(entry['track']['artists']):
            artistList.append(entry['track']['artists'][0]['id'])

            try:
                print "Querying for artist: " + str(entry['track']['artists'][0]['name']) + " -- " + str(entry['track']['artists'][0]['id'])
            except  UnicodeEncodeError:
                print "Querying for artist: " + entry['track']['artists'][0]['name'].encode('utf-8') + " -- " + entry['track']['artists'][0]['id'].encode('utf-8')

            topSong = helpers.queryForArtistTopSong(entry['track']['artists'][0]['id'])

            # If top song is different than reddit track, save to entry['top'] and save album id
            if topSong is not None:
                if topSong['id'] == entry['track']['id'] or topSong['name'] == entry['track']['name']:
                    entry['track']['top'] = None
                    entry['track']['isTop'] = True

                else:
                    entry['top'] = buildTrackObject(topSong, None)
                    entry['track']['top'] = topSong['id']
                    entry['track']['isTop'] = False
                    albumList.append(topSong['album']['id'])
                    artistList.append(topSong['artists'][0]['id'])

            else:
                print "No top song."
                entry['track']['top'] = None
                entry['track']['isTop'] = False

    return list(set(albumList)), list(set(artistList))

def buildTrackObject(trackObject, redditData):
    spotifyEntry = {}
    spotifyEntry['album'] = trackObject['album']
    spotifyEntry['artists'] = trackObject['artists']
    spotifyEntry['duration_ms'] = trackObject['duration_ms']
    spotifyEntry['explicit'] = trackObject['explicit']
    spotifyEntry['id'] = trackObject['id']
    spotifyEntry['name'] = trackObject['name']
    spotifyEntry['popularity'] = trackObject['popularity']
    spotifyEntry['preview_url'] = trackObject['preview_url']
    spotifyEntry['uri'] = trackObject['uri']

    if redditData is not None:
        spotifyEntry['redditData'] = redditData

    return spotifyEntry

##
## ALBUMS
##
def replaceAlbumObjects(spotifyData, albumSet):
    index = 0

    albumSet = list(set(albumSet))
    while index < len(albumSet):
        queryIds = albumSet[index:index+20]
        albumResults = helpers.queryForAllAlbums(queryIds)

        if albumResults is None:
            continue

        for albumResult in albumResults['albums']:
            emplaceAlbumResult(albumResult, spotifyData)

        index += 20

def emplaceAlbumResult(albumResult, spotifyData):
    found = False
    for spotifyObj in spotifyData:

        # Check if album corresponds to reddit suggestion
        if 'track' in spotifyObj:
            if 'album' in spotifyObj['track'] and spotifyObj['track']['album']['id'] == albumResult['id']:
                spotifyObj['track']['album'] = buildAlbumObject(albumResult)
                found = True

        # Check if album corresponds to artist top song
        if 'top' in spotifyObj:
            if 'album' in spotifyObj['top'] and spotifyObj['top']['album']['id'] == albumResult['id']:
                spotifyObj['top']['album'] = buildAlbumObject(albumResult)
                found = True

    if not found:
        print "NO MATCH FOUND - Album"

def buildAlbumObject(albumObject):
    spotifyEntry = {}
    spotifyEntry['genres'] = albumObject['genres']
    spotifyEntry['id'] = albumObject['id']
    spotifyEntry['images'] = albumObject['images']
    spotifyEntry['name'] = albumObject['name']
    spotifyEntry['popularity'] = albumObject['popularity']
    spotifyEntry['release_date'] = albumObject['release_date']
    spotifyEntry['release_date_precision'] = albumObject['release_date_precision']

    return spotifyEntry

##
## ARTISTS
##
def replaceArtistObjects(spotifyData, artistSet):
    artistResults = helpers.queryForAllArtists(artistSet)

    if artistResults is not None:
        for result in artistResults['artists']:

            found = False
            for entry in spotifyData:
                if 'artists' in entry['track'] and result['id'] == entry['track']['artists'][0]['id']:
                    entry['track']['artist'] = buildArtistObject(result)
                    del entry['track']['artists']
                    found = True

                if 'top' in entry and 'artists' in entry['top'] and result['id'] == entry['top']['artists'][0]['id']:
                    entry['top']['artist'] = buildArtistObject(result)
                    del entry['top']['artists']
                    found = True

            if not found:
                print "NO MATCH FOUND - Artist"

def buildArtistObject(artistObject):
    spotifyEntry = {}
    spotifyEntry['genres'] = artistObject['genres']
    spotifyEntry['id'] = artistObject['id']
    spotifyEntry['images'] = artistObject['images']
    spotifyEntry['name'] = artistObject['name']
    spotifyEntry['popularity'] = artistObject['popularity']

    return spotifyEntry

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

            redditGenres = splitRedditGenres(spotifyEntry['track']['redditData']['genre'])
            spotifyEntry['track']['genres'].update(redditGenres)

            spotifyEntry['track']['genres'] = list(spotifyEntry['track']['genres'])

        # If different top artist song
        if 'top' in spotifyEntry:
            spotifyEntry['top']['genres'] = set(spotifyGenres)
            spotifyEntry['top']['genres'].update(spotifyEntry['top']['artist']['genres'])
            spotifyEntry['top']['genres'].update(spotifyEntry['top']['album']['genres'])
            spotifyEntry['top']['genres'] = list(spotifyEntry['top']['genres'])

def splitRedditGenres(genreString):
    if genreString is None:
        return set()

    splitChar = ' '
    if '/' in genreString:
        splitChar = '/'

    genres = genreString.split(splitChar)
    genres = [x.strip() for x in genres]
    return set(genres)

def categorizeGenres(spotifyData):
    for spotifyEntry in spotifyData:
        if 'track' in spotifyEntry and 'genres' in spotifyEntry['track']:
            genres = []
            for genre in spotifyEntry['track']['genres']:
                genres.append({'genre': genre, 'class': helpers.getGenreClass(genre)})

            spotifyEntry['genres'] = genres

        if 'top' in spotifyEntry and 'genres' in spotifyEntry['top']:
            genres = []
            for genre in spotifyEntry['track']['genres']:
                genres.append({'genre': genre, 'class': helpers.getGenreClass(genre)})

            spotifyEntry['genres'] = genres

##
## PLAYLISTS
##
def getUserPlaylists():
    return helpers.queryForUserPlaylists()

def getSelectedPlaylistData(playlistId, ownerId):
    playlist = helpers.queryForSelectedPlaylist(playlistId, ownerId)
    playlist['totalLength'] = calcTotalPlaylistLength(playlist['tracks']['items'])

    return playlist

def getFullSelectedPlaylistData(playlistId, ownerId):
    playlist = getSelectedPlaylistData(playlistId, ownerId)
    playlist['totalLength'] = calcTotalPlaylistLength(playlist['tracks']['items'])
    playlist['tracks']['items'] = getTracksAudioFeatures(playlist['tracks']['items'])

    return playlist

def getTracksAudioFeatures(trackList):
    trackIds = []
    for track in trackList:
        trackIds.append(track['track']['id'])

    audioFeatures = helpers.queryForMultipleAudioFeatures(trackIds)

    for i in xrange(len(audioFeatures)):
        trackList[i]['track']['audioFeatures'] = audioFeatures[i]

    return trackList

def calcTotalPlaylistLength(tracks):
    ms = 0
    for track in tracks:
        ms += track['track']['duration_ms']

    hours = int(ms/(1000*60*60))
    remainder = ms % (1000*60*60)
    minutes = int(remainder/(1000*60))

    return str(hours) + " hr " + str(minutes) + " min"

def updateWithPlaylistOwnerNames(userPlaylists):
    owners = {}
    for playlist in userPlaylists:
        if playlist['owner']['id'] == helpers.userId:
            playlist['owner']['name'] = helpers.userProfile['display_name']

        else:
            nonUserId = str(playlist['owner']['id'])
            if nonUserId in owners:
                owners[nonUserId].append(playlist['owner'])
            else:
                owners[nonUserId] = [playlist['owner']]

    for ownerId in owners:
        queriedOwner = helpers.queryForUserProfile(ownerId)
        for ownerObj in owners[ownerId]:
            ownerObj['name'] = queriedOwner['display_name']

    return userPlaylists


#############################################################
#                                                           #
#                      Cached Data                          #
#                                                           #
#############################################################

def getCachedEntries(postList):
    cachedEntries = []
    cachedNotFoundIds = set()
    cachedIds = set()
    postIds = set()
    for post in postList:
        postIds.add(post['redditId'])

        cachedTrack = helpers.getFromSCache(post['redditId'])
        if cachedTrack is not None:
            if 'top' in cachedTrack:  # Processed by me
                if cachedTrack['top'] is not None:  # This is only track (not top)
                    cachedTop = helpers.getFromSCache(cachedTrack['top'])
                    if cachedTop is not None:
                        cachedSpotifyEntry = {'track': cachedTrack, 'top': cachedTop}
                        cachedEntries.append(cachedSpotifyEntry)
                        cachedIds.add(post['redditId'])

                else:  # This is track and top
                    cachedSpotifyEntry = {'track': cachedTrack}
                    cachedEntries.append(cachedSpotifyEntry)
                    cachedIds.add(post['redditId'])

            elif cachedTrack == helpers.notFoundValue:
                cachedNotFoundIds.add(post['redditId'])

    remainingIds = list((postIds - cachedIds) - cachedNotFoundIds)
    remainingPosts = []
    for remainingId in remainingIds:
        for post in postList:
            if post['redditId'] == remainingId:
                remainingPosts.append(post)

    print "Found " + str(len(cachedEntries) + len(cachedNotFoundIds)) + " cached entries."
    print "Remaining entries: " + str(len(remainingPosts)) + " of total " + str(len(postList))

    return remainingPosts, cachedEntries, cachedNotFoundIds

def prepareAndCacheSpotifyData(spotifyData, notFoundPosts):
    for entry in spotifyData:
        trackKeyList = [entry['track']['id'], entry['track']['redditData']['redditId']]
        helpers.saveToSCacheByKeyList(entry['track'], trackKeyList)

        if 'top' in entry:
            helpers.saveToSCacheByKeyList(entry['top'], [entry['top']['id']])

    for postId in notFoundPosts:
        helpers.saveToSCacheByKeyList(None, [postId])

    # Make permanent by flushing to disk
    helpers.flushSCache()
