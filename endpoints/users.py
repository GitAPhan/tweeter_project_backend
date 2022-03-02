from flask import request, Response
import dbinteractions.users as db
import dbinteractions.dbinteractions as f
import helpers.verification as v

# get user
def get():
    response = None

    # user input
    try:
        userId = int(request.args["userId"])
    except KeyError:
        userId = None
    except ValueError:
        return Response(
            "USER: input error - please enter a valid userId",
            mimetype="plain/text",
            status=400,
        )
    except:
        return Response("USER: server error - please try again in 5 minutes", mimetype="plain/text", status=500)

    response = db.get_user_db(userId)

    if response == None:
        response = Response("Endpoint Error: GET request was not completed", mimetype="plain/text", status=500)

    return response

# post user
def post():
    response = None

    # user input key variables
    try:
        keyname_verify = Response("ADMIN: Key Error - 'email'", mimetype="plain/text", status=500)
        email = request.json["email"]
        keyname_verify = Response("ADMIN: Key Error - 'bio'", mimetype="plain/text", status=500)
        bio = request.json["bio"]
        keyname_verify = Response("ADMIN: Key Error - 'birthdate'", mimetype="plain/text", status=500)
        birthdate = request.json["birthdate"]
    except KeyError:
        return keyname_verify
    except Exception as E:
        return Response("Endpoint Error: POST -" + str(E), mimetype="plain/text", status=493)

    # user input password
    try:
        keyname_verify = Response("ADMIN: Key Error - 'username'", mimetype="plain/text", status=500) 
        if v.verify_username(request.json['username']):
            username = request.json["username"]
        else:
            return Response("USER: 'username' cannot contain a space and has to be between 8 - 64 characters", mimetype="plain/text", status=400)
        keyname_verify = Response("ADMIN: Key Error - 'password'", mimetype="plain/text", status=500)
        # check to make sure password is valid
        if v.verify_password(request.json["password"]):
            password, salt = v.hash_the_salted_password(request.json["password"])
        else:
            return Response("USER: Please enter a valid password that is 8-64 characters long and contains a mix of uppercase and lowercase characters, a numeric and a special character", mimetype="plain/text", status=400)
    except KeyError:
        return keyname_verify
    except Exception as E:
        return Response("Endpoint Error: POST -" + str, mimetype="plain/text", status=400)
    # user input optional variables
    try:
        imageUrl = request.json["imageUrl"]
    except KeyError:
        imageUrl = None
    try:
        bannerUrl = request.json["bannerUrl"]
    except KeyError:
        bannerUrl = None

    # gather response from database
    response = db.post_user_db(
        email, username, password, salt, bio, birthdate, imageUrl, bannerUrl
    )
    if response == None:
        response = Response('Endpoint Error: POST - catch error', mimetype="plain/text", status=493)

    return response

# patch user
def patch():
    response = None

    # user input key variables
    try:
        loginToken = request.json['loginToken']
    except KeyError:
        return Response("ADMIN: Key error - 'loginToken'", mimetype="plain/text", status=500)
    except Exception as e:
        return Response("Endpoint Error: PATCH - " + str(e), mimetype="plain/text", status=400)

    # set value of key variables to None if keyname was not present in request
    try:
        email = request.json['email']
    except KeyError:
        email = None
        print('"email" keyname not present') #testing only

    try:
        username = request.json['username']
    except KeyError:
        username = None
        print('"username" keyname not present') #testing only

    try:
        bio = request.json['bio']
    except KeyError:
        bio = None
        print('"bio" keyname not present') #testing only

    try:
        birthdate = request.json['birthdate']
    except KeyError:
        birthdate = None
        print('"birthdate" keyname not present') #testing only

    try:
        imageUrl = request.json['imageUrl']
    except KeyError:
        imageUrl = None
        print('"imageUrl" keyname not present') #testing only

    try:
        bannerUrl = request.json['bannerUrl']
    except KeyError:
        bannerUrl = None
        print('"bannerUrl" keyname not present') #testing only

    # response from database
    response = db.patch_user_db(loginToken, email, username, bio, birthdate, imageUrl, bannerUrl)

    if response == None:
        response = Response("Endpoint Error: PATCH - catch error", mimetype="plain/text", status=493)

    return response

# delete user
def delete():
    hashpass = None
    salt = None
    response = None

    # user input password and loginToken
    try:
        keyname_verify = Response("ADMIN: Key Error - 'loginToken'", mimetype="plain/text", status=500)
        loginToken = request.json['loginToken']
        hashpass, salt = f.get_hashpass_salt_db(loginToken, "loginToken")

        if hashpass == False:
            return salt
        elif hashpass == None:
            return Response("DB Auth Error: Endpoint DELETE - user", mimetype="plain/text", status=400)

        keyname_verify = Response("ADMIN: Key Error - 'password'", mimetype="plain/text", status=500)
        password = request.json['password']

        if v.verify_hashed_salty_password(hashpass, salt, password):
            response = db.delete_user_db(loginToken)
        else:
            return Response("Invalid Credentials: wrong password!", mimetype="plain/text", status=401)
    except KeyError:
        return keyname_verify
    except Exception as E:
        return Response("Endpoint Error: DELETE -"+str(E), mimetype="plain/text", status=493)

    # final return
    return response