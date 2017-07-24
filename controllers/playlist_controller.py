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

    # Grab total data for first X playlists
    for i in xrange(4):
        playlistId = userPlaylists[i]['id']
        ownerId = userPlaylists[i]['owner']['id']
        userPlaylists[i] = ltt.getSelectedPlaylistData(playlistId, ownerId)

    print json.dumps(userPlaylists[0], indent=4)

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
            playlistTotalData = ltt.getSelectedPlaylistData(playlistId, ownerId)
            playlistData[playlistId] = playlistTotalData

    return jsonify(playlistData)
