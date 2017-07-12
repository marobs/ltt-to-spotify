import requests
import re
import helpers.cache_helpers

def getRedditPosts(redditQuery):
    if redditQuery is None or not helpers.checkQueryType(redditQuery):
        redditQuery = "top"

    # Check if the data is cached
    cachedData = helpers.getFromRCache(redditQuery)
    if cachedData is not None:
        print "Found and returning cached reddit data"
        return cachedData

    # Grab actual reddit data
    response = queryForRedditData(redditQuery)

    # Not sure what kind of error checking needs to occur here
    if "data" not in response or "children" not in response["data"]:
        print "No children post in reddit response"
        return None

    postList = []
    for child in response["data"]["children"]:
        if 'data' not in child or 'stickied' in child['data'] and child['data']['stickied']:
            continue

        post = {}
        if 'title' in child['data'] and 'url' in child['data'] and 'id' in child['data']:
            post = fillPostData(post, child)
            if post is not None:
                postList.append(post)

    # Save to cache
    print "Saving to cache: "
    printPostList(postList)
    helpers.saveToRCache(postList, redditQuery)
    return postList


# Query for reddit data based on redditQuery type
def queryForRedditData(redditQuery):
    url = "http://reddit.com/r/listentothis/" + str(redditQuery) + ".json"
    requestHeader = {'User-agent': 'ltts bot 0.1'}
    response = requests.get(url, headers=requestHeader)
    return response.json()


# Use regex to pull out title, artist, genre, and year
def fillPostData(post, child):
    post['rawTitle'] = child['data']['title']
    post['url'] = child['data']['url']
    post['redditId'] = child['data']['id']

    regexGroups = re.search("^(.*) -{1,2} (.*) \[(.*)\].*(\d\d\d\d)", post["rawTitle"])
    if regexGroups is None:
        regexGroups = re.search("^(.*) -{1,2} (.*) \[(.*)\]", post["rawTitle"])

    if regexGroups is None:
        print "Malformed title: " + post["rawTitle"].encode("utf-8") + " -- Moving on."
        return

    regexGroups = regexGroups.groups()
    if len(regexGroups) != 3 and len(regexGroups) != 4:
        print "Three groups not found in regex match! Moving on."
        return

    post["artist"] = regexGroups[0]
    post["title"] = regexGroups[1]
    post["genre"] = regexGroups[2]
    if len(regexGroups) == 4:
        post["year"] = regexGroups[3]

    return post


# Pretty printer
def printPostList(postList):
    for post in postList:
        print str(post["rawTitle"].encode("utf-8"))

        for attribute in post:
            if attribute != "rawTitle":
                print "\t" + str(post[attribute].encode("utf-8"))