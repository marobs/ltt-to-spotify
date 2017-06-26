from global_helpers import getClientId, getClientSecret
from url_helpers import *

def getAuthorizationUrl():
    clientId = getClientId()
    return composeAuthorizationUrl(clientId)

def getTokenRequestData(code):
    clientId = getClientId()
    clientSecret = getClientSecret()
    return composeTokenRequestData(code, clientId, clientSecret)

def getAccessTokenRequestData(refreshToken):
    clientId = getClientId()
    clientSecret = getClientSecret()
    return composeAccessTokenRequestData(refreshToken, clientId, clientSecret)