from flask import *
import ltt
import helpers;

playlist = Blueprint('playlist', __name__, template_folder='templates')

###
### [GET] Base /playlist endpoint
###
@playlist.route("/playlists")
def playlists_route():
    print "Hit route"
    userPlaylists = ltt.getUserPlaylists()
    print "Done grabbing playlists"

    # Update all user-owned playlist with user name
    for plist in userPlaylists:
        if plist['owner']['id'] == helpers.userId:
            plist['owner']['name'] = helpers.userProfile['display_name']

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
### [GET] Get owner names from ownerid list
### JSON
###
@playlist.route("/playlists/owners")
def playlists_owner_route():

    print json.dumps(request.values, indent=4)

    if not helpers.checkArgs(['ownerIdList'], request):
        return jsonify({'Error': "Malformed owner id request"})

    ownerIdList = request.values['ownerIdList']

    return jsonify(ltt.getOwnerNames(ownerIdList))

###
### [GET] Get single playlist information
### HTML
###
@playlist.route("/playlist")
def playlist_route():
    if not helpers.checkArgs(['playlistId','ownerId'], request):
        return jsonify({'Error': "Malformed playlist request"})

    playlistId = request.values['playlistId']
    ownerId = request.values['ownerId']

    playlistData = ltt.getFullSelectedPlaylistData(playlistId, ownerId)

    return jsonify(playlistData)

###
### [GET] Get history
###
@playlist.route("/history")
def history_route():
    historyData = helpers.queryForSpotifyHistory()
    return jsonify(historyData)
