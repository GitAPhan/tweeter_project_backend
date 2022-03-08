from flask import request, Response
import dbinteractions.dbinteractions as db
import dbinteractions.login as u
import helpers.verification as v

# post login
def post():
    hashpass = None
    salt = None

    response = None

    try:
        # user input for email
        email = request.json['email']
        hashpass, salt = db.get_hashpass_salt_db(email, "email")
        # verify
        if hashpass == False:
            return salt
    except KeyError:
        email = None

    try:
        # user input for username
        username = request.json['username']
        hashpass, salt = db.get_hashpass_salt_db(username, "username")
        # verify
        if hashpass == False:
            return salt
    except KeyError:
        username = None

    
    try:
        if hashpass == None:
            return Response("Endpoint Error: POST login - we ran into a problem verifying your login credentials", mimetype="plain/text", status=401)

        #user input password
        password = request.json['password']
        
        if v.verify_hashed_salty_password(hashpass, salt, password):
            if email != None:
                response = u.user_login_db(email, "email")
            elif username != None:
                response = u.user_login_db(username, "username")
            else:
                return Response("Endpoint Error: POST login - we ran into a problem running your request", mimetype="plain/text", status=401)
        else:
            return Response("USER: Invalid 'password', please check you credentials and try again!", mimetype="plain/text", status=401)
    except KeyError:
        return Response("ADMIN: Key Error - 'password'", mimetype="plain/text", status=500)

    if response == None:
        response = Response("Endpoint Error: POST login - catch error", mimetype="plain/text", status=493)

    return response

# delete login
def delete():
    user = None
    verify_status = None

    response = None

    # user input of loginToken
    try:
        loginToken = request.json['loginToken']
        user, verify_status = v.verify_loginToken(loginToken)

        if verify_status == False or user == None:
            return Response("USER: loginToken was not valid", mimetype="plain/text", status=401)
    except KeyError:
        return Response("ADMIN: keyname 'loginToken' error", mimetype="plain/text", status=500)
    
    response = u.user_logout_db(loginToken, user['id'])
    
    if response == None:
        response = Response("Endpoint Error: DELETE logout - catch error", mimetype="plain/text", status=492)
    return response
