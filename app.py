from flask import Flask, request, Response
import dbinteractions as db
import json
import sys

app = Flask(__name__)

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
        email = request.json['email']
        key_error_message = "ADMIN: Key Error - 'username'"
        username = request.json['username']
        key_error_message = "ADMIN: Key Error - 'password'"
        password = request.json['password']
        key_error_message = "ADMIN: Key Error - 'bio'"
        bio = request.json['bio']
        key_error_message = "ADMIN: Key Error - 'birthdate'"
        birthdate = request.json['birthdate']
    except KeyError:
        return Response(key_error_message, mimetype="plain/text", status=500)

    # user input optional variables
    try:
        x = 0
        imageUrl = request.json['imageUrl']
        x = 1
        bannerUrl = request.json['bannerUrl']
    except KeyError:
        if x == 0:
            imageUrl, bannerUrl = None, None
        else:
            bannerUrl = None
    
    # gather response from database
    response, status_code = db.post_user_db(email, username, password, bio, birthdate, imageUrl, bannerUrl)
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
