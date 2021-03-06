from flask import *
import ltt
import helpers

playlist = Blueprint('playlist', __name__, template_folder='templates')

###
### [GET] Base /playlist endpoint
### HTML
###
@playlist.route("/playlists")
def playlists_route():
    print "Hit route"
    userPlaylists = helpers.queryForUserPlaylists()
    print "Done grabbing playlists"

    # Update all user-owned playlist with user name
    userProfile = helpers.getUserProfile()
    for plist in userPlaylists:
        if plist['owner']['id'] == userProfile['id']:
            plist['owner']['name'] = userProfile['display_name']

    helpers.logGeneral(json.dumps(userPlaylists, indent=4))

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
            playlistTotalData = ltt.getSelectedPlaylistData(idPair['playlistId'], idPair['ownerId'])
            playlistData.append(playlistTotalData)

    return jsonify(playlistData)

###
### [GET] Get owner names from ownerId list
### JSON
###
@playlist.route("/playlists/owners")
def playlists_owner_route():
    if not helpers.checkArgs(['ownerIdList'], request):
        return jsonify({'Error': "Malformed owner id request"})

    ownerIdList = json.loads(request.values['ownerIdList'])
    return jsonify(ltt.getOwnerNames(ownerIdList))

###
### [GET] Get single playlist information
### HTML
###
@playlist.route("/playlist")
def playlist_route():
    if not helpers.checkArgs(['playlistId', 'ownerId'], request):
        return jsonify({'Error': "Malformed playlist request"})

    playlistId = request.values['playlistId']
    ownerId = request.values['ownerId']

    playlistData = ltt.getFullSelectedPlaylistData(playlistId, ownerId)

    return jsonify(playlistData)

###
### [GET] Get history
### JSON
###
@playlist.route("/history")
def history_route():
    historyData = helpers.queryForSpotifyHistory()
    return jsonify(historyData)
