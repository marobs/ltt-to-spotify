from flask import *
import helpers
import ltt
import requests
import json

listentothis = Blueprint('ltt', __name__, template_folder='templates')

###
### [GET] Base /ltt endpoint
###
@listentothis.route("/ltt")
def ltt_route():
    redditQuery = request.args.get('redditQuery')

    redditPosts = ltt.getRedditPosts(redditQuery)
    spotifyData = ltt.generateSpotifyData(redditPosts)
    userPlaylists = ltt.getUserPlaylists()

    selectedPlaylist = None
    if userPlaylists is not None and len(userPlaylists) > 0:
        selectedPlaylist = ltt.getSelectedPlaylist(userPlaylists[0])

    return render_template("ltt.html", songList=spotifyData, playlists=userPlaylists, selected=selectedPlaylist)

###
### [GET] Spotify entries for different reddit query
###
@listentothis.route("/ltt/redditSearch")
def ltt_reddit_route():
    if not helpers.checkArgs(['redditQuery'], request):
        return jsonify({'Error': "Malformed playlist request"})

    redditQuery = request.args['redditQuery']
    if not helpers.checkQueryType(redditQuery):
        return jsonify({'Error': "Invalid reddit query type requested: " + str(redditQuery)})

    redditPosts = ltt.getRedditPosts(redditQuery)
    spotifyData = ltt.generateSpotifyData(redditPosts)

    return jsonify(spotifyData)

###
### [GET] Get playlist data
###
@listentothis.route("/ltt/playlist")
def ltt_playlist_route():
    if not helpers.checkArgs(['playlistId', 'userId'], request):
        return jsonify({'Error': "Malformed playlist request"})

    playlistId = request.args['playlistId']
    userId = request.args['userId']
    playlist = helpers.queryForSelectedPlaylist(playlistId, userId)

    return jsonify(playlist)

###
### [POST] Add track to playlist
###
@listentothis.route("/ltt/addTrack", methods=['POST'])
def ltt_add_track_route():
    if not helpers.checkArgs(['playlistId', 'userId', 'trackURI'], request):
        return jsonify({'Error': "Malformed add track request"})

    playlistId = request.args['playlistId']
    userId = request.args['userId']
    trackURI = request.args['trackURI']

    response = helpers.postAddTrackRequest(playlistId, userId, trackURI)
    return response  # Success = {'snapshot_id': xxx} 201

###
### [DELETE] Remove track from playlist
###
@listentothis.route("/ltt/removeTrack", methods=['DELETE'])
def ltt_remove_track_route():
    if not helpers.checkArgs(['playlistId', 'userId', 'trackURI'], request):
        return jsonify({'Error': "Malformed remove track request"})

    playlistId = request.args['playlistId']
    userId = request.args['userId']
    trackURI = request.args['trackURI']

    response = helpers.deleteRemoveTrackRequest(playlistId, userId, trackURI)
    return response  # Success = {'snapshot_id': xxx} 201

###
### [PUT] Save track for user
###
@listentothis.route("/ltt/saveTrack", methods=['PUT'])
def ltt_save_track_route():
    if not helpers.checkArgs(['ids'], request):
        return jsonify({'Error': "Malformed save track request"})

    ids = request.args['ids']

    response = helpers.putSaveTrackRequest(ids)
    if response.status_code != requests.codes.ok:
        return jsonify({'Error': "Bad status code returned: " + str(response.status_code)})

    return response  # Success 203


###
### [DELETE] Remove saved track for user
###
@listentothis.route("/ltt/saveTrack", methods=['DELETE'])
def ltt_unsave_track_route():
    if not helpers.checkArgs(['ids'], request):
        return jsonify({'Error': "Malformed unsave track request"})

    ids = request.args['ids']

    response = helpers.deleteUnsaveTrackRequest(ids)
    if response.status_code != requests.codes.ok:
        return jsonify({'Error': "Bad status code returned: " + str(response.status_code)})

    return response  # Success 200


###
### [PUT] Reorder playlist tracks
###
@listentothis.route("/ltt/reorder", methods=['PUT'])
def ltt_reorder_route():
    if not helpers.checkArgs(['userId', 'playlistId', 'rangeStart', 'rangeLength', 'insertBefore'], request):
        return jsonify({'Error': 'Malformed reorder request'})

    userId = request.args['userId']
    playlistId = request.args['playlistId']
    rangeStart = request.args['rangeStart']
    rangeLength = request.args['rangeLength']
    insertBefore = request.args['insertBefore']

    response = helpers.reorderPlaylistRequest(userId, playlistId, rangeStart, rangeLength, insertBefore)
    if response.status_code != requests.codes.ok:
        return jsonify({'Error': "Bad status code returned: " + str(response.status_code)})

    return response
