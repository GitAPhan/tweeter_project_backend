from flask import request, Response
import dbinteractions.tweet_like as t
import helpers.verification as v

# GET request for tweet like
def get():
    response = None
    tweetId = None

    # input request of tweetId
    try:
        tweetId = int(request.json['tweetId'])
    except KeyError:
        return Response("'tweetId' keyname not present", mimetype="plain/text", status=500)
    except Exception as E:
        return Response("Endpoint Error: GET tweet_like -"+str(E), mimetype="plain/text", status=400)
    
    # None check for tweetId before request to db
    if tweetId == None:
        return Response("Endpoint Error: GET tweet_like - general error", mimetype="plain/text", status=492)
    else:
        response = t.get_db(tweetId)

    # None check on response
    if response == None:
        response = Response("Endpoint Error: GET tweet_like - catch error", mimetype="plain/text", status=493)
    
    return response

# POST request for tweet like
def post():
    response = None
    tweetId = None
    status = None
    userId = None

    # input request for loginToken, verify that user's login session is active
    try:
        loginToken = request.json['loginToken']
        userId, status = v.verify_loginToken(loginToken)

        if status != True:
            return Response("Unauthorized: we ran into a problem verifying this token", mimetype="plain/text", status=403)
    except KeyError:
        return Response("Endpoint Error: 'loginToken' keyname not present", mimetype="plain/text", status=500)
    except Exception as E:
        return Response("Endpoint Error: POST tweet_like -"+str(E), mimetype="plain/text", status=400)

    # input request for tweetId
    try:
        tweetId = int(request.json['tweetId'])
    except KeyError:
        return Response("Endpoint Error: 'tweetId' keyname not present", mimetype="plain/text", status=500)
    except ValueError:
        return Response("Endpoint Error: Invalid value entered", mimetype="plain/text", status=400)
    except Exception as E:
        return Response("Endpoint Error: POST tweet_like -"+str(E), mimetype="plain/text", status=400)

    if userId == None or tweetId == None:
        return Response("Endpoint Error: POST tweet_like - general error", mimetype="plain/text", status=400)
    else:
        response = t.post_db(userId, tweetId)

    if response == None:
        response = Response("Endpoint Error: POST tweet_like - catch error", mimetype="plain/text", status=400)
    
    return response