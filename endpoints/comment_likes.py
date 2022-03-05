from flask import request, Response
import dbinteractions.comment_likes as c
import helpers.verification as v

# GET comment_like request
def get():
    response = None

    try:
        # input request for commentId
        commentId = int(request.args['commentId'])
        # db request
        response = c.get_db(commentId)
    except ValueError:
        return Response("Endpoint Error: invalid value entered for commentId", mimetype="plain/text", status=400)
    
    # None check - catch
    if response == None:
        response = Response("Endpoint Error: GET comment_likes - catch error", mimetype="plain/text", status=499)
    
    return response

# POST comment_like request
def post():
    response = None
    user = None

    try:
        # input request and verification of loginToken
        loginToken = request.json['loginToken']
        user, status = v.verify_loginToken(loginToken)
        # status check
        if status != True:
            return Response('Invalid Credentials: loginToken was not valid', mimetype="plain/text", status=403)
    except KeyError:
        return Response("Endpoint Error: 'loginToken' keyname not present", mimetype="plain/text", status=500)
    
    try:
        # input request for commentId
        commentId = int(request.json['commentId'])
        # db request
        if user != None:
            response = c.post_db(user, commentId)
    except KeyError:
        return Response("Endpoint Error: 'commentId' keyname not present", mimetype="plain/text", status=500)
    
    # None check - catch
    if response == None:
        response = Response("Endpoint Error: POST comment_like - catch error", mimetype="plain/text", status=499)

    return response

# DELETE comment_like request
def delete():
    response = None
    user = None

    try:
        # input request and verification of loginToken
        loginToken = request.json['loginToken']
        user, status = v.verify_loginToken(loginToken)
        # status check
        if status != True:
            return Response('Invalid Credentials: loginToken was not valid', mimetype="plain/text", status=403)
    except KeyError:
        return Response("Endpoint Error: 'loginToken' keyname not present", mimetype="plain/text", status=500)
    
    try:
        # input request for commentId
        commentId = int(request.json['commentId'])
        # db request
        if user != None:
            response = c.delete_db(user, commentId)
    except KeyError:
        return Response("Endpoint Error: 'commentId' keyname not present", mimetype="plain/text", status=500)
    
    # None check - catch
    if response == None:
        response = Response("Endpoint Error: DELETE comment_like - catch error", mimetype="plain/text", status=499)

    return response