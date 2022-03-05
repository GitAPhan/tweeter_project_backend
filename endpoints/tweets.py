from flask import request, Response
import dbinteractions.tweets as t
import helpers.verification as v

# GET tweet
def get():
    response = None
    
    userId = None
    tweetId = None
    try:
        userId = int(request.args['userId'])
    except KeyError:
        userId = None
        print('"userID" keyname not present') #testing 
    except ValueError:
        return Response("Endpoint Error: Invalid value entered for userId", mimetype="plain/text", status=400)
    
    try:
        tweetId = request.args['tweetId']
    except KeyError:
        tweetId = None
        print('"tweetId" keyname not present') #testing only
    except ValueError:
        return Response("Endpoint Error: Invalid value entered for tweetId", mimetype="plain/text", status=400)
    
    if userId == None and tweetId == None:
        # get all tweets

        print('NONE ')

    response = t.get_db(userId, tweetId)

    if response == None:
        response = Response("Endpoint Error: GET catch error", mimetype="plain/text", status="493")
    
    return response

# POST tweet
def post():
    response = None
    status = None
    user = None
    content = None
    imageUrl = None

    try:
        loginToken = request.json['loginToken']
        user, status = v.verify_loginToken(loginToken)

        if status == False:
            return user
    except KeyError:
        return Response("'loginToken' keyname not present", mimetype="plain/text", status=500)
    except Exception as E:
        return Response("Endpoint Error: POST tweet - "+str(E), mimetype="plain/text", status=492)

    try:
        content = request.json['content']
        if len(content) > 200:
            return Response("'content' has a character limit of 200", mimetype="plain/text", status=406)
    except KeyError:
        return Response("'content' keyname not present", mimetype="plain/text", status=500)
    except Exception as E:
        return Response("Endpoint Error: POST tweet - "+str(E), mimetype="plain/text", status=492)

    try:
        imageUrl = request.json['imageUrl']
    except KeyError:
        imageUrl = None
    except Exception as E:
        return Response("Endpoint Error: POST tweet - "+str(E), mimetype="plain/text", status=492)

    if user == None or content == None:
        return Response("Endpoint Error: POST tweet - general error", mimetype="plain/text", status=493)

    response = t.post_db(user['id'], content, imageUrl)

    if response == None:
        response = Response("Endpoint Error: POST tweet - catch error", mimetype="plain/text", status=494)

    return response

# PATCH tweet
def patch():
    response = None
    status = None
    user = None
    content = None
    tweetId = None
    imageUrl = None

    try:
        loginToken = request.json['loginToken']
        user, status = v.verify_loginToken(loginToken)

        if status == False:
            return user
    except KeyError:
        return Response("'loginToken' keyname not present", mimetype="plain/text", status=500)
    except Exception as E:
        return Response("Endpoint Error: POST tweet - "+str(E), mimetype="plain/text", status=492)

    try:
        keyname_verify = Response("'tweetId' keyname not present", mimetype="plain/text", status=500)
        tweetId = request.json['tweetId']
        keyname_verify = Response("'content' keyname not present", mimetype="plain/text", status=500)
        content = request.json['content']
        if len(content) > 200:
            return Response("'content' has a character limit of 200", mimetype="plain/text", status=406)
    except KeyError:
        return keyname_verify
    except Exception as E:
        return Response("Endpoint Error: PATCH tweet - "+str(E), mimetype="plain/text", status=492)

    try:
        imageUrl = request.json['imageUrl']
    except KeyError:
        imageUrl = None
    except Exception as E:
        return Response("Endpoint Error: PATCH tweet - "+str(E), mimetype="plain/text", status=492)

    if user == None or content == None or tweetId == None:
        return Response("Endpoint Error: PATCH tweet - general error", mimetype="plain/text", status=493)

    response = t.patch_db(user['id'], tweetId, content, imageUrl)

    if response == None:
        response = Response("Endpoint Error: PATCH tweet - catch error", mimetype="plain/text", status=494)

    return response


# DELETE tweet
def delete():
    response = None
    status = None
    user = None

    try:
        loginToken = request.json['loginToken']
        user, status = v.verify_loginToken(loginToken)

        if status == False:
            return user
    except KeyError:
        return Response("'loginToken' keyname not present", mimetype="plain/text", status=500)
    except Exception as E:
        return Response("Endpoint Error: DELETE tweet -"+str(E), mimetype="plain/text", status=493)
    
    try:
        tweetId = request.json['tweetId']
    except KeyError:
        return Response("'tweetId' keyname not present", mimetype="plain/text", status=500)

    if user == None or status == None:
        return Response("Endpoint Error: DELETE tweet - general error", mimetype="plain/text", status=493)
    
    response = t.delete_db(user['id'], tweetId)

    return response