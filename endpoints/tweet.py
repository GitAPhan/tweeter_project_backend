import json
from flask import Flask, request, Response
import dbinteractions.tweet as t
import helpers.verification as v

# GET tweet
def get():
    response = None
    
    # userId = None
    # tweetId = None
    try:
        userId = request.args['userId']
    except KeyError:
        userId = None
        print('"userID" keyname not present') #testing only
    
    try:
        tweetId = request.args['tweetId']
    except KeyError:
        tweetId = None
        print('"tweetId" keyname not present') #testing only
    
    if userId == None and tweetId == None:
        return Response("Endpoint Error: GET - tweet 'keyname' error", mimetype="plain/text", status=500)

    response = t.get_db(userId, tweetId)

    if response == None:
        response = Response("Endpoint Error: GET catch error", mimetype="plain/text", status="493")
    
    return response