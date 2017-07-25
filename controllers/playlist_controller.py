from flask import *
import ltt
import helpers;

playlist = Blueprint('playlist', __name__, template_folder='templates')

###
### [GET] Base /playlist endpoint
###
@playlist.route("/playlists")
def playlists_route():
    userPlaylists = ltt.getUserPlaylists()

    # Grab total data for first X playlists
    for i in xrange(4):
        playlistId = userPlaylists[i]['id']
        ownerId = userPlaylists[i]['owner']['id']
        userPlaylists[i] = ltt.getSelectedPlaylistData(playlistId, ownerId)

    # Update all playlists with owner names
    userPlaylists = ltt.updateWithPlaylistOwnerNames(userPlaylists)

    return render_template("playlists.html", playlists=userPlaylists, userId=helpers.userId)

###
### [GET] Get playlist information (including full track and playlist data) for list of
###         [{'playlistId': xx, 'ownerId': yy}, ...] pairs
### JSON
###
@playlist.route("/playlists/data")
def playlists_data_route():
    if not helpers.checkArgs(['idPairList'], request):
        return jsonify({'Error': "Malformed playlist request"})

    idPairList = json.loads(request.values['idPairList'])
    playlistData = []
    for idPair in idPairList:
        if 'playlistId' in idPair and 'ownerId' in idPair:
            playlistId = idPair['playlistId']
            ownerId = idPair['ownerId']
            playlistTotalData = ltt.getSelectedPlaylistData(playlistId, ownerId)
            playlistData.append(playlistTotalData)

    return jsonify(playlistData)

###
### [GET] Get single playlist information
### HTML
###
@playlist.route("/playlist")
def playlist_route():

    print json.dumps(request.values, indent=4)

    if not helpers.checkArgs(['playlistId','ownerId'], request):
        return jsonify({'Error': "Malformed playlist request"})

    playlistId = request.values['playlistId']
    ownerId = request.values['ownerId']

    playlistData = ltt.getSelectedPlaylistData(playlistId, ownerId)

    return jsonify(playlistData)

