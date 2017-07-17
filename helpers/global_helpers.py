import os
import requests
from url_helpers import *
import json

#############################################################################
#                                                                           #
#                           Authentication                                  #
#                                                                           #
#############################################################################

## Globals

clientId = "8467851f4c30445dbf7f0d4d1c0f019a";
clientSecret = None
flaskSecret = None
refreshToken = None
accessToken = None
userId = None
basePath = os.path.dirname(os.path.realpath(__file__))

##
## Getters
##
def getClientId():
    global clientId
    return clientId

def getClientSecret():
    global clientSecret
    return clientSecret

def getFlaskSecret():
    global flaskSecret
    return flaskSecret

def getRefreshToken():
    global refreshToken
    return refreshToken

def getAccessToken():
    global accessToken
    if accessToken is None:
        return queryForAccessToken()

    return accessToken

def getUserId():
    global userId
    return userId

##
## Client Secret
##
def initializeClientSecret(bPath):
    print "Initializing Client Secret"
    global clientSecret
    with open(bPath + "/../secrets/client_secret.txt") as f:
        clientSecret = f.read().rstrip("\n")

    if clientSecret is None:
        print "Tried to initialize clientSecret but still None"

##
## Flask Secret
##
def getFlaskSecret():
    global flaskSecret
    return flaskSecret

def initializeFlaskSecret(bPath):
    print "Initializing Flask Secret"
    global flaskSecret
    with open(bPath + "/../secrets/flask_secret.txt") as f:
        flaskSecret = f.read().rstrip("\n")

    if flaskSecret is None:
        print "Tried to initialize flaskSecret but still None"

##
## Tokens
##
def initializeRefreshToken(bPath):
    print "Initializing Refresh Token"
    global refreshToken
    
    if not os.path.isfile(basePath + "/../secrets/refresh_token.txt"):
        print "  No refresh token file found, need to query"
        # Query for tokens

    else:
        with open(bPath + "/../secrets/refresh_token.txt") as f:
            refreshToken = f.read().rstrip("\n")

        print "Found refresh token file. refreshToken"

def saveRefreshToken(token):
    if token is None:
        return

    global refreshToken 
    refreshToken = token

    print "Saving refresh token: " + token
    with open(basePath + "/../secrets/refresh_token.txt", 'w') as f:
        f.write(token)

def initializeAccessToken():
    print "Initializing Access Token"
    if accessToken is not None:
        print "Already initialized!"
        return

    refresh = getRefreshToken()
    queryForAccessToken(refresh)

def queryForAccessToken(refreshToken):
    print "Querying for Access Token"
    if refreshToken is None:
        print "Can't query for access token because refresh token is None"
        return None

    global clientId
    global clientSecret
    postData = composeAccessTokenRequestData(refreshToken, clientId, clientSecret)
    response = requests.post("https://accounts.spotify.com/api/token", data=postData)
    setAccessToken(response.json().get("access_token"))

def setAccessToken(token):
    if token is None:
        print "Tried to set access token but received None"
        return 

    global accessToken
    print "Setting access token"
    accessToken = token

##
## UserId
##
def initializeUserId():
    global userId
    url = "https://api.spotify.com/v1/me"
    userProfile = query_http(url, None, None, "Get user profile", 'GET')

    print json.dumps(userProfile, indent=4)

    if 'id' in userProfile:
        userId = userProfile['id']
        print "Set userid: " + str(userId)

    else:
        print "ERROR: User id couldn't be found in userProfile"


##
## Initialization
##
def initializeHelpers():
    print "Initializing helpers"

    global clientSecret
    global flaskSecret
    if clientSecret is not None or flaskSecret is not None:
        print "Already initialized clientSecret or flaskSecret"
        return
    
    initializeClientSecret(basePath)
    initializeFlaskSecret(basePath)
    initializeRefreshToken(basePath)
    initializeAccessToken()
    initializeUserId()

def checkAuthenticated():
    print "Checking authenticated"
    return refreshToken is not None


#############################################################################
#                                                                           #
#                               Queries                                     #
#                                                                           #
#############################################################################

##
## [GET/POST/PUT/DELETE] Queries
##
def query_http(url, parameters, requestHeader, reqType, httpType):
    global accessToken
    global refreshToken

    if requestHeader is None:
        requestHeader = {}
    requestHeader['Authorization'] = "Bearer " + str(accessToken)

    # Send DELETE query
    response = sendQuery(url, parameters, requestHeader, reqType, httpType)

    # Check status code; if not ok, try refreshing access token
    if response.status_code != requests.codes.ok:
        print "Invalid access token found. Refreshing!"
        queryForAccessToken(refreshToken)
        requestHeader['Authorization'] = "Bearer " + accessToken
        response = sendQuery(url, parameters, requestHeader, reqType, httpType)

    # If still not ok, print error and return
    if response.status_code != requests.codes.ok:
        print "Error: <" + reqType + "> of http type <" + str(httpType) + "> code not ok! Status code: " + str(response.status_code)
        searchResults = response.json()
        for key in searchResults:
            print "  " + str(key) + ": " + str(searchResults[key])

        return None

    # Return json response
    return response.json()


## Send actual request
def sendQuery(url, parameters, requestHeader, reqType, httpType):
    if httpType == 'GET':
        return requests.get(url, params=parameters, headers=requestHeader)
    elif httpType == 'POST':
        return requests.post(url, params=parameters, headers=requestHeader)
    elif httpType == 'PUT':
        return requests.put(url, params=parameters, headers=requestHeader)
    elif httpType == 'DELETE':
        return requests.delete(url, params=parameters, headers=requestHeader)
    else:
        print "Unknown HTTP request type found: <" + str(httpType) + ">"

    return None
