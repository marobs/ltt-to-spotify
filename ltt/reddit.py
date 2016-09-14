import requests

def getRedditPosts():
	response = requests.get("http://reddit.com/r/listentothis/hot.json")
	