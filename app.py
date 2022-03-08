from flask import Flask
import sys
import endpoints.users as users
import endpoints.login as login
import endpoints.follows as follows
import endpoints.tweets as tweets
import endpoints.tweet_likes as tlikes
import endpoints.comments as comments
import endpoints.comment_likes as clikes


app = Flask(__name__)

## users
# get user
@app.get("/api/users")
def get_users():
    return users.get()


# post user
@app.post("/api/users")
def post_user():
    return users.post()


# patch user
@app.patch("/api/users")
def patch_user():
    return users.patch()   

# # delete user
@app.delete('/api/users')
def delete_user():
    return users.delete()
        

## login
# post login
@app.post('/api/login')
def user_login():
    return login.post()


# delete login
@app.delete('/api/login')
def user_logout():
    return login.delete()


## follows
# get follow
@app.get('/api/follows')
def get_follow():
    return follows.get()

# post follow
@app.post('/api/follows')
def post_follow():
    return follows.post()

# delete follow
@app.delete('/api/follows')
def delete_follow():
    return follows.delete()

## followers
# get follower
@app.get('/api/followers')
def get_follower():
    return follows.get_follower()

## tweets
# get tweet
@app.get('/api/tweets')
def get_tweet():
    return tweets.get()
# get tweets for discover
@app.get('/api/discover')
def get_tweet_discover():
    return tweets.discover()
# get tweets for feed (followed)
@app.get('/api/feed')
def get_tweet_feed():
    return tweets.feed()

# post tweet
@app.post('/api/tweets')
def post_tweet():
    return tweets.post()

# patch tweet
@app.patch('/api/tweets')
def patch_tweet():
    return tweets.patch()

# delete tweet
@app.delete('/api/tweets')
def delete_tweet():
    return tweets.delete()

## tweet likes
# get tweet like
@app.get('/api/tweet_likes')
def get_tweet_like():
    return tlikes.get()

# post tweet like
@app.post('/api/tweet_likes')
def post_tweet_like():
    return tlikes.post()

# delete tweet like
@app.delete('/api/tweet_likes')
def delete_tweet_like():
    return tlikes.delete()

## comments
# get commment
@app.get('/api/comments')
def get_comment():
    return comments.get()

# post comment
@app.post('/api/comments')
def post_comment():
    return comments.post()

# patch comment
@app.patch('/api/comments')
def patch_comment():
    return comments.patch()

# delete comment
@app.delete('/api/comments')
def delete_comment():
    return comments.delete()

## comment likes
# get comment likes
@app.get('/api/comment_likes')
def get_comment_like():
    return clikes.get()

# post comment likes
@app.post('/api/comment_likes')
def post_comment_like():
    return clikes.post()

# delete comment likes
@app.delete('/api/comment_likes')
def delete_comment_likes():
    return clikes.delete()


# ## RUN MODE SETTINGS ##
# mode check
if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    print(
        "You must pass a mode to run this python script. Either 'testing' or 'production'"
    )
    exit()

# testing/production mode code
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
