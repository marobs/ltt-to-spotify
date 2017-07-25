import helpers
import json

def getSpotifyHistory():
    timestamp = helpers.datetimeToEpochMs(helpers.getNow())

    history = helpers.queryForSpotifyHistory(timestamp, 20)
    helpers.logGeneral(json.dumps(history, indent=4))

