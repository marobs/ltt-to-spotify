import requests
import re

def getRedditPosts():
    response = requests.get("http://reddit.com/r/listentothis/hot.json", headers={'User-agent': 'ltts bot 0.1'})
    print "Response type: " + str(response.encoding)
    jData = response.json()

    # Not sure what kind of error checking needs to occur here
    if "data" not in jData or "children" not in jData["data"]:
        print "No children post in reddit response"
        return False

    postList = []
    for child in jData["data"]["children"]:
        if "data" not in child:
            print "No child data found"
            continue

        childData = child["data"]

        # If stickied post, not a song so continue
        if "stickied" in childData and childData["stickied"]:
            print "Stickied, continuing"
            continue

        # Otherwise, grab song data and append it to the post list
        post = {}
        if "title" in childData:
            print "TYPEOF TITLE: " + str(type(childData["title"]))
            post["rawTitle"] = childData["title"]
        else:
            print "No title in child"

        if "url" in childData:
            post["url"] = childData["url"]

        generateAndAppendSongData(post, postList)

    print "Generated all posts! List size: " + str(len(postList))
    printPostList(postList)

    return postList

def generateAndAppendSongData(post, postList):
    print "Generating song data: " + str(post)

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

    postList.append(post)

    print "\n"

def printPostList(postList):
    for post in postList:
        print str(post["rawTitle"].encode("utf-8"))

        for attribute in post:
            if attribute != "rawTitle":
                print "\t" + str(post[attribute].encode("utf-8"))

        print "\n"
