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
        accessToken = helpers.getAccessToken()
        songList = ltt.getRedditPosts()
        ltt.searchSpotify(songList)
        return render_template("ltt.html", songList=songList)

