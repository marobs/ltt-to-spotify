from flask import *
import ltt


playlist = Blueprint('playlist', __name__, template_folder='templates')

###
### [GET] Base /playlist endpoint
###
@playlist.route("/playlists")
def playlists_route():
    userPlaylists = ltt.getUserPlaylists()
    userPlaylists = ltt.updateWithPlaylistOwnerNames(userPlaylists)
    ltt.batchFirstPlaylists(userPlaylists)

    return render_template("playlists.html", playlists=userPlaylists)

###
### [GET] Get playlist information (including full track and playlist data) for list of
###         [{'playlistId': xx, 'ownerId': yy}, ...] pairs
### JSON
###
@playlist.route("/playlists/data")
def ltt_reddit_route():
    if not helpers.checkArgs(['idPairList'], request):
        return jsonify({'Error': "Malformed playlist request"})

    idPairList = request.values['idPairList']
    playlistData = {}
    for idPair in idPairList:
        if 'playlistId' in idPair and 'ownerId' in idPair:
            playlistId = idPair['playlistId']
            ownerId = idPair['ownerId']
            playlist = ltt.getPlaylistTotalData(playlistId, ownerId)
            playlistData[playlistId] = playlist

    return jsonify(playlistData)