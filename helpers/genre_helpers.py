from global_helpers import basePath

genreDict = None

def initializeGenreDict():
    global genreDict
    initDict = {}

    with open(basePath + "/../static/genres.txt", "r") as genreFile:
        lines = genreFile.readlines()
        lines = [x.strip().lower().replace('-', '') for x in lines]

        i = 0
        while i < len(lines):
            category = lines[i]

            while i < len(lines) and lines[i] != '':
                subgenre = lines[i]
                initDict[subgenre] = category
                i += 1

            i += 1  # Skip blank line

    genreDict = initDict

def categorizeGenres(genreList):
    categorizedGenres = []
    for genre in genreList:
        categorizedGenres.append({'genre': genre, 'class': getGenreClass(genre)})

    return categorizedGenres

def getGenreClass(genre):
    global genreDict

    # All inputs have no dashes and are lowercase
    genre.replace('-', '')
    genre = genre.lower()

    if genre in genreDict:
        return genreDict[genre]

    else:
        return 'unclassified'

def splitRedditGenres(genreString):
    if genreString is None:
        return set()

    splitChar = ' '
    if '/' in genreString:
        splitChar = '/'

    genres = genreString.split(splitChar)
    genres = [x.strip() for x in genres]
    return set(genres)
