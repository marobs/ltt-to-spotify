from __future__ import division
import helpers
import json

def getSelectedPlaylistData(playlistId, ownerId):
    playlist = helpers.queryForSelectedPlaylist(playlistId, ownerId)
    playlist['totalLength'] = calcTotalPlaylistLength(playlist['tracks']['items'])

    return playlist

def getFullSelectedPlaylistData(playlistId, ownerId):
    playlist = getSelectedPlaylistData(playlistId, ownerId)
    playlist['totalLength'] = calcTotalPlaylistLength(playlist['tracks']['items'])
    playlist['tracks']['items'] = getTracksAudioFeatures(playlist['tracks']['items'])
    playlist = calculatePlaylistTrackMetrics(playlist)

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

def getOwnerNames(ownerIdList):
    ownerDict = {}
    for ownerId in ownerIdList:
        cachedId = helpers.getFromIDCache(ownerId)
        if cachedId is None or cachedId == helpers.VALUE_NOT_FOUND:
            queriedOwner = helpers.queryForUserProfile(ownerId)
            ownerDict[ownerId] = queriedOwner['display_name']
            helpers.saveToIDCache(ownerId, queriedOwner['display_name'])

        else:
            ownerDict[ownerId] = cachedId

    helpers.flushIDCache()
    return ownerDict

def calculatePlaylistTrackMetrics(playlist):
    helpers.logGeneral(json.dumps(playlist, indent=4))
    playlist['audioFeatures'] = helpers.calculateAudioFeaturesMetrics(playlist)

    return playlist