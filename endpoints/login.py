from flask import request, Response
import dbinteractions.dbinteractions as db
import dbinteractions.login as u
import helpers.verification as v

# post login
def post():
    hashpass = None
    salt = None

    response = None

    #user input email and password
    try:
        keyname_verify = Response("ADMIN: Key Error - 'email'", mimetype="plain/text", status=500)
        email = request.json['email']
        hashpass, salt = db.get_hashpass_salt_db(email, "email")

        if hashpass == None or hashpass == False:
            return salt

        keyname_verify = Response("ADMIN: Key Error - 'password'", mimetype="plain/text", status=500)
        password = request.json['password']
        
        if v.verify_hashed_salty_password(hashpass, salt, password):
            response = u.user_login_db(email, "email")
        else:
            return Response("USER: Invalid 'password', please check you credentials and try again!", mimetype="plain/text", status=401)
    except KeyError:
        return keyname_verify

    if response == None:
        response = Response("Endpoint Error: POST login - catch error", mimetype="plain/text", status=493)

    return response

# delete login
def delete():
    userId = None
    verify_status = None

    response = None

    # user input of loginToken
    try:
        loginToken = request.json['loginToken']
        userId, verify_status = v.verify_loginToken(loginToken)

        if verify_status == False or userId == None:
            return Response("USER: loginToken was not valid", mimetype="plain/text", status=401)
    except KeyError:
        return Response("ADMIN: keyname 'loginToken' error", mimetype="plain/text", status=500)
    
    response = u.user_logout_db(loginToken, userId)
    
    if response == None:
        response = Response("Endpoint Error: DELETE logout - catch error", mimetype="plain/text", status=492)
    return response
