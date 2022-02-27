import imp
import json
from flask import Flask, request, Response
import dbinteractions.follows as f
import helpers.verification as v

# Get follows
def get():
    response = None

    try:
        # user input user_id
        userId = request.args["userId"]

        # db request to grab users
        response = f.get_db(userId)
    except KeyError:
        return Response(
            "ADMIN: key error - 'userId'", mimetype="plain/text", status=500
        )

    if response == None:
        response = Response(
            "Endpoint Error: General GET Error", mimetype="plain/text", status=493
        )
    # Response
    return response


# POST follows
def post():
    response = None
    userId = None
    followId = None

    try:
        # user input user
        response = Response(
            "ADMIN: key error - 'loginToken'", mimetype="plain/text", status=500
        )
        loginToken = request.json["loginToken"]

        # verify loginToken
        userId, verify_status = v.verify_loginToken(loginToken)
        if verify_status != True:
            return Response(userId, mimetype="plain/text", status=verify_status)

        response = Response(
            "ADMIN: key error = 'followId'", mimetype="plain/text", status=500
        )
        followId = request.json["followId"]

    except KeyError:
        return response

    if userId == None and followId == None:
        return Response(
            "NEW ERROR ---- !!!! WTF !!!!", mimetype="plain/text", status=409
        )
    # post to database
    response = f.post_db(userId, followId)

    if response == None:
        response = Response(
            "Endpoint Error: General POST error", mimetype="plain/text", status=493
        )

    return response


# DELETE follows
def delete():
    response = None
    user_id = None
    
    try:
        # loginToken
        response = Response(
            "ADMIN: key error - 'loginToken'", mimetype="plain/text", status=500
        )
        loginToken = request.json['loginToken']
        user_id, verify_status = v.verify_loginToken(loginToken)
        if verify_status != True:
            return Response(userId, mimetype="plain/text", status=verify_status)

