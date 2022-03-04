from flask import request, Response
import dbinteractions.comments as c
import helpers.verification as v


# GET request for comment
def get():
    response = None

    try:
        # input request for tweetId
        tweetId = request.args['tweetId']
        # DB request
        response = c.get_db(tweetId)
    except KeyError:
        return Response("Endpoint Error: 'tweetId' keyname not present", mimetype="plain/text", status=500)
    except Exception as E:
        return Response("Endpoint Error: GET comments -"+str(E), mimetype="plain/text", status=499)
    
    # None check - catch
    if response == None:
        response = Response("Endpoint Error: GET comments - catch error", mimetype="plain/text", status=499)

    return response

# POST request for comments
def post():
    response = None
    user = None

    try:
        # input request and verification of loginToken
        loginToken = request.json['loginToken']
        user, status = v.verify_loginToken(loginToken)

        # check to see if token was valid
        if status != True:
            return user
    except KeyError:
        return Response("Endpoint Error: 'loginToken' keyname not present", mimetype="plain/text", status=500)
    except Exception as E:
        return Response("Endpoint Error: POST comment -"+str(E), mimetype="plain/text", status=499)

    try:
        # input request for tweetId and content
        keyname_verify = Response("Endpoint Error: 'tweetId' keyname not present", mimetype="plain/text", status=500)
        tweetId = int(request.json['tweetId'])
        keyname_verify = Response("Endpoint Error: 'content' keyname not present", mimetype="plain/text", status=500)
        content = request.json['content']
        if len(content) > 150:
            return Response("comment has exceeded the 150 character limit", mimetype="plain/text", status=400)
        # DB request
        if user == None:
            return Response("DB Error: POST comments - verify loginToken did not run", mimetype="plain/text", status=499)
        response = c.post_db(user, tweetId, content)
    except KeyError:
        return keyname_verify
    except ValueError:
        return Response("Endpoint Error: invalid value entered for keyname 'tweetId'", mimetype="plain/text", status=400)
    except Exception as E:
        return Response("Endpoint Error: POST comments -"+str(E), mimetype="plain/text", status=499)

    # None check - catch
    if response == None:
        response = Response("Endpoint Error: POST comments - catch error", mimetype='plain/text', status=499)

    return response

# DELETE request for comments
def delete():
    response = None
    user = None

    try:
        # input request and verification of loginToken
        loginToken = request.json['loginToken']
        user, status = v.verify_loginToken(loginToken)

        if status != True:
            return user
    except KeyError:
        return Response("Endpoint Error: 'loginToken' keyname not present", mimetype="plain/text", status=500)
    except Exception as E:
        return Response("Endpoint Error: DELETE comment -"+str(E), mimetype="plain/text", status=499)
    
    try:
        # input request for commentId
        commentId = int(request.json['commentId'])
        # db request
        if user != None:
            response = c.delete_db(user['id'], commentId)
    except Exception as E:
        return Response("Endpoint Error: DELETE comments -"+str(E), mimetype="plain/text", status=499)
    
    # None check - catch
    if response == None:
        response = Response("Endpoint Error: DELETE comments - catch error", mimetype="plain/text", status=499)
    
    return response