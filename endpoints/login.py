from flask import Flask, request, Response
import json
import dbinteractions.dbinteractions as db
import dbinteractions.login as u
import helpers.verification as v

# post login
def post():
    hashpass = None
    salt = None

    response = None
    status_code = 400

    #user input email and password
    try:
        key_error_message = "ADMIN: Key Error - 'email'"
        email = request.json['email']
        hashpass, salt = db.get_hashpass_salt_db(email, "email")

        if hashpass == None or hashpass == False:
            return Response("USER: Authentication error - invalid 'email'", mimetype="plain/text", status=401)

        key_error_message = "ADMIN: Key Error - 'password'"
        password = request.json['password']
        
        if v.verify_hashed_salty_password(hashpass, salt, password):
            response, status_code = u.user_login_db(email, "email")
        else:
            return Response("USER: Invalid 'password', please check you credentials and try again!", mimetype="plain/text", status=401)
    except KeyError:
        return Response(key_error_message, mimetype="plain/text", status=500)

    response_json = json.dumps(response, default=str)

    return Response(response_json, mimetype="application/json", status=status_code)

# delete login
def delete():
    userId = None
    verify_status = False

    response = None
    status_code = 400

    # user input of loginToken
    try:
        loginToken = request.json['loginToken']
        userId, verify_status = v.verify_loginToken(loginToken)

        if verify_status == True:
            response, status_code = u.user_logout_db(loginToken, userId)
        else:
            return Response("USER: loginToken was not valid", mimetype="plain/text", status=401)
    except KeyError:
        return Response("ADMIN: keyname 'loginToken' error", mimetype="plain/text", status=500)
    
    response_json = json.dumps(response, default=str)
    return Response(response_json, mimetype="application/json", status=status_code)
