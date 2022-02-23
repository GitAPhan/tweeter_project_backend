from flask import Flask, request, Response
import dbinteractions as db
import verification as v
import json
import sys

app = Flask(__name__)

# # Custom exceptions
class InvalidValueEntered(Exception):
    pass

## users
# get user
@app.get("/api/users")
def get_user():
    response = []
    status_code = 500

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
        return Response("USER: server error - please try again in 5 minutes ")

    response, status_code = db.get_user_db(userId)
    response_json = json.dumps(response, default=str)

    return Response(response_json, mimetype="application/json", status=status_code)


# post user
@app.post("/api/users")
def post_user():
    response = []
    status_code = 500

    # user input key variables
    try:
        key_error_message = "ADMIN: Key Error - 'email'"
        email = request.json["email"]
        key_error_message = "ADMIN: Key Error - 'bio'"
        bio = request.json["bio"]
        key_error_message = "ADMIN: Key Error - 'birthdate'"
        birthdate = request.json["birthdate"]
    except KeyError:
        return Response(key_error_message, mimetype="plain/text", status=500)
    # user input password
    try:
        key_error_message = "ADMIN: Key Error - 'username'"
        if v.verify_username(request.json['username']):
            username = request.json["username"]
        else:
            status_code = 400
            verify_error = "USER: 'username' cannot contain a space and has to be between 8 - 64 characters"
            raise InvalidValueEntered
        key_error_message = "ADMIN: Key Error - 'password'"
        # check to make sure password is valid
        if v.verify_password(request.json["password"]):
            password, salt = v.hash_the_salted_password(request.json["password"])
        else:
            status_code = 400
            verify_error = "USER: Please enter a valid password that is 8-64 characters long and contains a mix of uppercase and lowercase characters, a numeric and a special character"
            raise InvalidValueEntered
    except KeyError:
        return Response(key_error_message, mimetype="plain/text", status=status_code)
    except InvalidValueEntered:
        return Response(verify_error, mimetype="plain/text", status=status_code)
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
    response, status_code = db.post_user_db(
        email, username, password, salt, bio, birthdate, imageUrl, bannerUrl
    )
    response_json = json.dumps(response, default=str)

    return Response(response_json, mimetype="application/json", status=status_code)


# patch user
@app.patch("/api/users")
def patch_user():
    response: []
    status_code: 500

    # user input key variables
    try:
        loginToken = request.json['loginToken']
    except KeyError:
        return Response("ADMIN: Key error - 'loginToken'", mimetype="plain/text", status=status_code)
    except Exception as e:
        print(e)

    # set value of key variables to None if keyname was not present in request
    try:
        email = request.json['email']
    except KeyError:
        email = None
        print('"email" keyname not present')

    try:
        username = request.json['username']
    except KeyError:
        username = None
        print('"username" keyname not present')

    try:
        bio = request.json['bio']
    except KeyError:
        bio = None
        print('"bio" keyname not present')

    try:
        birthdate = request.json['birthdate']
    except KeyError:
        birthdate = None
        print('"birthdate" keyname not present')

    try:
        imageUrl = request.json['imageUrl']
    except KeyError:
        imageUrl = None
        print('"imageUrl" keyname not present')

    try:
        bannerUrl = request.json['bannerUrl']
    except KeyError:
        bannerUrl = None
        print('"bannerUrl" keyname not present')

    # response from database
    response, status_code = db.patch_user_db(loginToken, email, username, bio, birthdate, imageUrl, bannerUrl)
    response_json = json.dumps(response, default=str)

    return Response(response_json, mimetype="application/json", status=status_code)        

# # delete user
@app.delete('/api/users')
def delete_user():
    hashpass = None
    salt = "USER: Looks like we ran into some problems verifying your request, please check you credentials and try again!"
    response = []
    status_code = 400

    # user input password and loginToken
    try:
        key_error_message = "ADMIN: Key Error - 'loginToken'"
        loginToken = request.json['loginToken']
        hashpass, salt = db.get_hashpass_salt_db(loginToken, "loginToken")

        if hashpass == None or hashpass == False:
            return Response(salt, mimetype="plain/text", status=401)

        key_error_message = "ADMIN: Key Error - 'password'"
        password = request.json['password']

        if v.verify_hashed_salty_password(hashpass, salt, password):
            response, status_code = db.delete_user_db(loginToken)
        else:
            return Response("USER: Invalid 'password', please check you credentials and try again!", mimetype="plain/text", status=401)
    except KeyError:
        return Response(key_error_message, mimetype="plain/text", status=500)

    # final return
    return Response(response, mimetype="plain/text", status=status_code)
        

## login
# post login
@app.post('/api/login')
def user_login():
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
            response, status_code = db.user_login_db(email, "email")
        else:
            return Response("USER: Invalid 'password', please check you credentials and try again!", mimetype="plain/text", status=401)
    except KeyError:
        return Response(key_error_message, mimetype="plain/text", status=500)

    response_json = json.dumps(response, default=str)

    return Response(response_json, mimetype="application/json", status=status_code)


# delete login

## follows
# get follow

# post follow

# delete follow

## followers
# get follower

## tweets
# get tweet

# post tweet

# patch tweet

# delete tweet

## tweet likes
# get tweet like

# post tweet like

# delete tweet like

## comments
# get commment

# post comment

# patch comment

# delete comment

## comment likes
# get comment likes

# post comment likes

# delete comment likes


# testing/production mode code
if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    print(
        "You must pass a mode to run this python script. Either 'testing' or 'production'"
    )
    exit()

if mode == "testing":
    from flask_cors import CORS

    CORS(app)
    print("running in testing mode")
    app.run(debug=True)
elif mode == "production":
    print("running in production mode")
    import bjoern  # type: ignore

    bjoern.run(app, "0.0.0.0", 5005)
else:
    print("Invalid mode: Please run using either 'testing' or 'production'")
    exit()
