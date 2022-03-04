import json
import dbinteractions.dbinteractions as c
import mariadb as db
import helpers.format_output as format
from flask import Response
import datetime

# GET comment from database
def get_db(tweetId):
    response = None
    comments = None

    conn, cursor = c.connect_db()
    
    try:
        # query request to grab all comments relating to tweetId
        cursor.execute('SELECT c.id, c.tweet_id, c.user_id, u.username, c.content, c.created_at FROM comment c INNER JOIN user u ON u.id = c.user_id WHERE c.tweet_id =?', [tweetId])
        comments = cursor.fetchall()
    except Exception as E:
        response = Response("DB Error: GET comments -"+str(E), mimetype="plain/text", status=499)
    
    c.disconnect_db(conn, cursor)

    # return any value for response other than None
    if response != None:
        return response
    
    # None check - comments
    if comments == None:
        return Response("DB Error: GET comments - query did not run properly", mimetype="plain/text", status=499)
    
    # format response output
    response = []
    for comment in comments:
        x = format.comment(comment)
        response.append(x)
    response_json = json.dumps(response, default=str)
    response = Response(response_json, mimetype="application/json", status=200)

    # None check - catch
    if response == None:
        response = Response("DB Error: GET comments - catch error", mimetype="plain/text", status=400)
    
    return response

# POST comment to database
def post_db(user, tweetId, content):
    response = None
    commentId = None

    conn, cursor = c.connect_db()

    try:
        # query request to create new comment in database
        cursor.execute("INSERT INTO comment (content, tweet_id, user_id) VALUE (?,?,?)",[content, tweetId, user_id])
        conn.commit()
        commentId = cursor.lastrowid
    except KeyError as E:
        response = Response("DB Error: POST comments -"+str(E), mimetype="plain/text", status=499)

    c.disconnect_db(conn, cursor)

    # return any value for response other than None
    if response != None:
        return response
    
    # None check - did query run
    if commentId == None:
        return Response("DB Error: POST comments - query request didn't run", mimetype="plain/text", status=499)
    
    created_at = datetime.datetime.now()
    response = format.comment([commentId, tweetId, user['id'], user['name'], content, created_at])

    # None check - catch
    if response == None:
        response = Response("DB Error: POST comments - catch error", mimetype="plain/text", status=499)
    
    return response

# DELETE comment from database
def delete_db(userId, commentId):
    response = None
    status = None

    conn, cursor = c.connect_db()

    try:
        # query request to delete comment from database
        cursor.execute("DELETE FROM comment where user_id =? and id =?", [userId, commentId])
        conn.commit()
        status = cursor.rowcount

        if status == 1:
            response = Response("comment successfully deleted", mimetype="plain/text", status=200)
    except Exception as E:
        response = Response("DB Error: DELETE comment -"+str(E), mimetype="plain/text", status=499)
    
    c.disconnect_db(conn, cursor)

    # return any value for response that is not None
    if response != None:
        return response
    
    # catch error message
    return Response("DB Error: DELETE comment - catch error", mimetype="plain/text", status=499)