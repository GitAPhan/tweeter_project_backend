import imp
import json
from flask import Flask, request, Response
import dbinteractions.follows as f
import helpers.verification as v

# Get follows
def get():
    response = None
    status_code = 400

    try:
        # user input user_id 
        userId = request.args['userId']
    except KeyError:
        return Response("ADMIN: key error - 'userId'", mimetype="plain/text", status=500)

    # db request to grab users
    response, status_code = f.get_db(userId)

    # Response
    response_json = json.dumps(response, default=str)
    return Response(response_json, mimetype="application/json", status=status_code)

# POST folows
def post():
    response = None
    status_code = 400

    userId = None
    followId = None

    try:
        key_error_message = "ADMIN: key error - 'loginToken'"
        # user input user
        loginToken = request.json['loginToken']

        # verify loginToken
        userId, verify_status = v.verify_loginToken(loginToken)

        if verify_status == False:
            return Response(response, mimetype="plain/text", status=401)

        key_error_message = "ADMIN: key error = 'followId'"
        followId = request.json['followId']
    except KeyError:
        return Response(key_error_message, mimetype="plain/text", status=500)

    if userId == None and followId == None:
        return Response('NEW ERROR ---- !!!! WTF !!!!')

    # post to database 
    response, status_code = f.post_db(userId, followId)
    
    return Response(response, mimetype="application/json", status=status_code)