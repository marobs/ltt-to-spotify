from flask import *
import helpers
import ltt

listentothis = Blueprint('ltt', __name__, template_folder='templates')

###
### [GET] Base /ltt endpoint
###
@listentothis.route("/ltt")
def ltt_route():
    if not helpers.checkAuthenticated():
        print "Must authenticate!"
        return redirect(helpers.getAuthorizationUrl())

    else:
        redditPosts = ltt.getRedditPosts()
        spotifyTracks = ltt.searchSpotify(redditPosts)
        userPlaylists = ltt.getUserPlaylists()

        selectedPlaylist = None
        if userPlaylists is not None and len(userPlaylists) > 0:
            selectedPlaylist = ltt.getSelectedPlaylist(userPlaylists[0])

        print "selected playlist: " + str(selectedPlaylist["tracks"]["items"][0])

        return render_template("ltt.html", songList=redditPosts, playlists=userPlaylists, selected=selectedPlaylist)

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


@listentothis.route("/ltt/addTrack", methods=['POST'])
def ltt_addtrack_route():
    if not helpers.checkArgs(['playlistId', 'userId', 'trackURI'], request):
        return jsonify({'Error': "Malformed add track request"})

    playlistId = request.args['playlistId']
    userId = request.args['userId']
    trackURI = request.args['trackURI']

    response = helpers.postAddTrackRequest(playlistId, userId, trackURI)
    return response # Success = {'snapshot_id': xxx} 201


@listentothis.route("/ltt/removeTrack", methods=['DELETE'])
def ltt_removetrack_route():
    if not helpers.checkArgs(['playlistId', 'userId', 'trackURI'], request):
        return jsonify({'Error': "Malformed remove track request"})

    playlistId = request.args['playlistId']
    userId = request.args['userId']
    trackURI = request.args['trackURI']

    response = helpers.postRemoveTrackRequest(playlistId, userId, trackURI)
    return response  # Success = {'snapshot_id': xxx} 201
