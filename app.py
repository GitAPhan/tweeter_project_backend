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

# delete user

## login
# post login

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
