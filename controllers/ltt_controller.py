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

