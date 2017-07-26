# acousticness:     float -- 1.0 is acoustic
# danceability:     float -- 1.0 is most danceable
# energy:           float -- 1.0 is high energy
# valence:          float -- 1.0 is happy 0.0 is sad
# instrumentalness: float -- 0.5+ is instrumental, higher is more confident
# key:              int   -- 0 is C, 1 is C#, etc.
# liveness:         float -- 0.8+ means high likelihood it was performed live
# loudness:         float -- between -60 and 0db
# mode:             int   -- 1 is major 0 is minor
# speechiness:      float -- 0.0 to 0.33 is music, 0.33 to 0.66 is rap or layered or sectioned, 0.66+ is speech
# tempo:            float -- bpm AVERAGE
# time_signature:   int   -- bars in a measure

def calculateAudioFeaturesMetrics(playlist):
    playlistAF = initializePlaylistAF()
    for track in playlist['tracks']['items']:
        for key in track['track']['audioFeatures']:
            if key in playlistAF:
                playlistAF[key].append(track['track']['audioFeatures'][key])

    for feature in playlistAF:
        playlistAF[feature] = calcAFStats(playlistAF[feature])

    return playlistAF

def initializePlaylistAF():
    return {
        'acousticness': [],
        'danceability': [],
        'energy':       [],
        'valence':      [],
        'instrumentalness': [],
        'key':          [],
        'liveness':     [],
        'loudness':     [],
        'mode':         [],
        'speechiness':  [],
        'tempo':        [],
        'time_signature': [],
    }

def calcAFStats(featureList):
    if len(featureList) <= 0:
        return None

    sortedList = sorted(featureList)
    return {
        'min': sortedList[0],
        'q1': calcQ1(sortedList),
        'median': calcMedian(sortedList),
        'q3': calcQ3(sortedList),
        'max': sortedList[-1],
        'average': calcAverage(sortedList),
        'appears': len(featureList)
    }

def calcQ1(sortedList):
    m = (len(sortedList) / 2) - 1
    return calcMedian(sortedList[0:m])

def calcMedian(sortedList):
    n = len(sortedList)
    if n % 2 == 0:
        return (sortedList[n/2] + sortedList[(n/2)-1]) / 2

    else:
        return sortedList[n/2]

def calcQ3(sortedList):
    p = (len(sortedList) / 2)
    return calcMedian(sortedList[p:])

def calcAverage(sortedList):
    sum = 0.0
    for item in sortedList:
        sum += item

    return sum / len(sortedList)