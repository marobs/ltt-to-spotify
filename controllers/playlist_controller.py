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

