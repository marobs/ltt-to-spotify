from flask import *
import helpers
import ltt
import requests
import json

listentothis = Blueprint('ltt', __name__, template_folder='templates')

###
### [GET] Base /ltt endpoint
### HTML
###
@listentothis.route("/ltt")
def ltt_route():
    if not helpers.checkAuthenticated():
        return redirect(helpers.getAuthorizationUrl())

    redditQuery = request.values.get('redditQuery')

    redditPosts = ltt.getRedditPosts(redditQuery)
    spotifyData = ltt.generateSpotifyData(redditPosts)
    userPlaylists = ltt.getUserPlaylists()

    selectedPlaylist = None
    if userPlaylists is not None and len(userPlaylists) > 0:
        selectedPlaylist = ltt.getSelectedPlaylist(userPlaylists[0])

    return render_template("ltt.html", songList=spotifyData, playlists=userPlaylists, selected=selectedPlaylist)

###
### [GET] Spotify entries for different reddit query
### JSON
###
@listentothis.route("/ltt/redditSearch")
def ltt_reddit_route():
    if not helpers.checkArgs(['redditQuery'], request):
        return jsonify({'Error': "Malformed playlist request"})

    redditQuery = request.values['redditQuery']
    if not helpers.checkQueryType(redditQuery):
        return jsonify({'Error': "Invalid reddit query type requested: " + str(redditQuery)})

    redditPosts = ltt.getRedditPosts(redditQuery)
    spotifyData = ltt.generateSpotifyData(redditPosts)

    return jsonify(spotifyData)

###
### [GET] Get playlist data
### JSON
###
@listentothis.route("/ltt/playlist")
def ltt_playlist_route():
    if not helpers.checkArgs(['playlistId', 'userId'], request):
        return jsonify({'Error': "Malformed playlist request"})

    playlistId = request.values['playlistId']
    userId = request.values['userId']
    playlist = helpers.queryForSelectedPlaylist(playlistId, userId)

    return render_template('expandedPlaylist.html', selected=playlist)

###
### [POST] Add track to playlist
### JSON
###
@listentothis.route("/ltt/addTrack", methods=['POST'])
def ltt_add_track_route():
    if not helpers.checkArgs(['playlistId', 'trackURI'], request):
        return jsonify({'Error': "Malformed add track request"})

    playlistId = request.values['playlistId']
    userId = helpers.getUserId()
    trackURI = request.values['trackURI']
    position = request.values.get('position')

    spotifyResponse = helpers.postAddTrackRequest(playlistId, userId, trackURI, position)
    return jsonify(spotifyResponse)  # Success = {'snapshot_id': xxx} 201

###
### [DELETE] Remove track from playlist
### JSON
###
@listentothis.route("/ltt/removeTrack", methods=['DELETE'])
def ltt_remove_track_route():
    if not helpers.checkArgs(['playlistId', 'trackURI'], request):
        return jsonify({'Error': "Malformed remove track request"})

    playlistId = request.values['playlistId']
    userId = helpers.getUserId()
    trackURI = request.values['trackURI']

    response = helpers.deleteRemoveTrackRequest(playlistId, userId, trackURI)
    return jsonify(response)  # Success = {'snapshot_id': xxx} 201

###
### [PUT] Save track for user
### JSON
###
@listentothis.route("/ltt/saveTrack", methods=['PUT'])
def ltt_save_track_route():
    if not helpers.checkArgs(['ids'], request):
        return jsonify({'Error': "Malformed save track request"})

    ids = request.values['ids']

    response = helpers.putSaveTrackRequest(ids)
    if response.status_code not in helpers.okHttpStatusCodes:
        return jsonify({'Error': "Bad status code returned: " + str(response.status_code)})

    return jsonify(response)  # Success 203


###
### [DELETE] Remove saved track for user
### JSON
###
@listentothis.route("/ltt/saveTrack", methods=['DELETE'])
def ltt_unsave_track_route():
    if not helpers.checkArgs(['ids'], request):
        return jsonify({'Error': "Malformed unsave track request"})

    ids = request.values['ids']

    response = helpers.deleteUnsaveTrackRequest(ids)
    if response.status_code not in helpers.okHttpStatusCodes:
        return jsonify({'Error': "Bad status code returned: " + str(response.status_code)})

    return jsonify(response)  # Success 200


###
### [PUT] Reorder playlist tracks
### JSON
###
@listentothis.route("/ltt/reorder", methods=['PUT'])
def ltt_reorder_route():
    if not helpers.checkArgs(['playlistId', 'rangeStart', 'rangeLength', 'insertBefore'], request):
        return jsonify({'Error': 'Malformed reorder request'})

    userId = helpers.getUserId()
    playlistId = request.values['playlistId']
    rangeStart = request.values['rangeStart']
    rangeLength = request.values['rangeLength']
    insertBefore = request.values['insertBefore']

    response = helpers.reorderPlaylistRequest(userId, playlistId, rangeStart, rangeLength, insertBefore)
    if response.status_code not in helpers.okHttpStatusCodes:
        return jsonify({'Error': "Bad status code returned: " + str(response.status_code)})

    return jsonify(response)
