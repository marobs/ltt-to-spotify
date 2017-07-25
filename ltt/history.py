import helpers
import json

def getSpotifyHistory():
    history = helpers.queryForSpotifyHistory(20)
    helpers.logGeneral(json.dumps(history, indent=4))