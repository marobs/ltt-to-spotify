import os
import requests

## Globals

clientId = "8467851f4c30445dbf7f0d4d1c0f019a";
clientSecret = None
flaskSecret = None
refreshToken = None
accessToken = None
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
	return accessToken

##
## Client Secret
##
def initializeClientSecret(basePath):
	print "Initializing Client Secret"
	global clientSecret
	with open(basePath  + "/../secrets/client_secret.txt") as f:
		clientSecret = f.read().rstrip("\n")

##
## Flask Secret
##
def getFlaskSecret():
	global flaskSecret
	return flaskSecret

def initializeFlaskSecret(basePath):
	print "Initializing Flask Secret"
	global flaskSecret
	with open(basePath + "/../secrets/flask_secret.txt") as f:
		flaskSecret = f.read().rstrip("\n")

##
## Tokens
##
def initializeRefreshToken(basePath):
	print "Initializing Refresh Token"
	global refreshToken
	
	if not os.path.isfile(basePath + "/../secrets/refresh_token.txt"):
		print "  No refresh token file found, need to query"
		# Query for tokens

	else:
		with open(basePath  + "/../secrets/refresh_token.txt") as f:
			refreshToken = f.read().rstrip("\n")
		print "  Found refresh token file. RT: " + refreshToken

def saveRefreshToken(token):
	global refreshToken 
	refreshToken = token
	with open(basePath + "/../secrets/refresh_token.txt", 'w') as f:
		f.write(token)

def initializeAccessToken():
	print "Initializing Access Token"
	refreshToken = getRefreshToken()
	queryForAccessToken(refreshToken)	

def queryForAccessToken(refreshToken):
	print "Querying for Access Token"
	return 0

##
## Initialization
##
def initializeHelpers():
	global clientSecret
	global flaskSecret
	if clientSecret != None or flaskSecret != None:
		return
	
	initializeClientSecret(basePath)
	initializeFlaskSecret(basePath)
	initializeRefreshToken(basePath)

def checkAuthenticated():
	return (refreshToken != None) or (accessToken != None)
	 

