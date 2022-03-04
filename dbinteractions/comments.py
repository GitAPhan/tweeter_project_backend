from dis import disco
import json
import dbinteractions.dbinteractions as c
import mariadb as db
import helpers.format_output as format
from flask import Response
import datetime

# GET comment from database
def get_db(tweetId, commentId):
    response = None
    comments = None

    # query builder
    query_keyname = None
    query_keyvalue = None
    if tweetId != None and commentId == None:
        # if tweetId was input
        query_keyname = "c.tweet_id"
        query_keyvalue = [tweetId]
    
    elif commentId != None and tweetId == None:
        # if commentId was input
        query_keyname = "c.id"
        query_keyvalue = [commentId]
    query_request = f'SELECT c.id, c.tweet_id, c.user_id, u.username, c.content, c.created_at FROM comment c INNER JOIN user u ON u.id = c.user_id WHERE {query_keyname} =?'
    # None check
    if query_keyvalue == None or query_keyname == None:
        return Response("DB Error: GET comments - only one key:value can be submitted", mimetype="plain/text", status=406)

    conn, cursor = c.connect_db()
    
    try:
        # query request to grab all comments relating to tweetId
        cursor.execute(query_request, query_keyvalue)
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

# PATCH comment in database
def patch_db(user, commentId, content):
    response = None
    status = None

    conn, cursor = c.connect_db()

    try:
        #  query request to update comment in database
        cursor.execute("UPDATE comment SET content=? WHERE id=? and user_id=?", [content, commentId, user['id']])
        conn.commit()
        status = cursor.rowcount

        if status != 1:
            response = Response("DB Error: PATCH comments - nothing was updated", mimetype="plain/text", status=499)
    except Exception as E:
        response = Response("DB Error: PATCH comments -"+str(E), mimetype="plain/text", status=499)
    
    c.disconnect_db(conn, cursor)

    # return any value of response that is not None
    if response != None:
        return response
    
    response = get_db(None, commentId)

    # None check - catch
    if response == None:
        response = Response("DB Error: PATCH comments - catch error", mimetype="plain/text", status=499)

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