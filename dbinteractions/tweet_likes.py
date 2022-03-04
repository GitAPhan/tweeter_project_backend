import json
import dbinteractions.dbinteractions as c
import mariadb as db
import helpers.format_output as fo
from flask import Response

# GET tweet_like from database
def get_db(tweetId):
    response = None
    likes = None

    conn, cursor = c.connect_db()

    # query request to database
    try:
        cursor.execute("SELECT tl.tweet_id, tl.user_id, u.username FROM tweet_like tl INNER JOIN user u ON u.id = tl.user_id WHERE tl.tweet_id =?", [tweetId])
        likes = cursor.fetchall()
    except Exception as E:
        response = Response("DB Error: GET tweet_like -"+str(E), mimetype="plain/text", status=490)
    
    c.disconnect_db(conn, cursor)

    # return any value in response that is not None
    if response != None:
        return response
    elif likes == None:
        return Response("DB Error: GET tweet_like - general error", mimetype="plain/text", status=491)
    else:
        # format response
        response = []
        for like in likes:
            x = fo.format_tweet_like_output(like)
            response.append(x)
        response_json = json.dumps(response, default=str)
        response = Response(response_json, mimetype="application/json", status=200)

    # None check - catch
    if response == None:
        response = Response("DB Error: GET tweet_like - catch error", mimetype="plain/text", status=491)
    
    return response

# POST tweet_like to database
def post_db(userId, tweetId):
    response = None
    status = None

    conn, cursor = c.connect_db()
    
    # query request to insert event into database
    try:
        cursor.execute("INSERT INTO tweet_like (user_id, tweet_id) VALUES (?,?)", [userId, tweetId])
        conn.commit()
        status = cursor.rowcount

        # status check
        if status != 1:
            response = Response("DB Error: POST tweet_like - general error", mimetype="plain/text", status=400)
    except Exception as E:
        response = Response("DB Error: POST tweet_like -"+str(E), mimetype="plain/text", status=400)
    
    c.disconnect_db(conn, cursor)

    # return any value in response other than None 
    if response != None:
        return response
    else:
        response = Response("tweet has been successfully liked", mimetype="plain/text", status=201)

    # None check - catch
    if response == None:
        response = Response("DB Error: POST tweet_like - catch error", mimetype="plain/text", status=400)
    
    return response

# DELETE tweet_like from database
def delete_db(userId, tweetId):
    response = None
    
    conn, cursor = c.connect_db()

    try:
        # query to delete from database
        cursor.execute("DELETE FROM tweet_like WHERE user_id = ? and tweet_id = ?", [userId, tweetId])
        conn.commit()
        status = cursor.rowcount

        if status == 1:
            response = Response("tweet has been successfully unliked", mimetype="plain/text", status=200)
        else:
            response = Response("no changes have been made", mimetype="plain/text", status=400)
    except Exception as E:
        response = Response("DB Error: DELETE tweet_like - "+str(E), mimetype="plain/text", status=499)

    c.disconnect_db(conn, cursor)

    # None check - catch
    if response == None:
        response = Response("DB Error: DELETE tweet_like - catch error", mimetype="plain/text", status=499)
    
    return response