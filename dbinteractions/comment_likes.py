import json
import dbinteractions.dbinteractions as c
import mariadb as db
import helpers.format_output as format
from flask import Response

# GET comment_like from database
def get_db(commentId):
    response = None
    comment_likes = None

    conn, cursor = c.connect_db()

    try:
        # query to select comment likes relating to commentId
        cursor.execute("SELECT c.comment_id, c.user_id, u.username FROM comment_like WHERE comment_id=?",[commentId])
        comment_likes = cursor.fetchall()
    except Exception as E:
        response = Response("DB Error: GET comment_like -"+str(E), mimetype="plain/text", status=499)

    c.disconnect_db(conn, cursor)

    # return any value in response other than None
    if response != None:
        return response

    # format output
    if comment_likes != None:
        response = []
        for comment_like in comment_likes:
            x = format.comment_like(comment_like)
            response.append(x)
    
    # None check - catch
    if response == None:
        response = Response("DB Error: GET comment_like - catch error", mimetype="plain/text", status=499)
    
    return response

# POST comment_like to database
def post_db(user, commentId):
    response = None

    conn, cursor = c.connect_db()

    try:
        # query to insert comment_like into database
        cursor.execute("INSERT INTO comment_like (user_id, comment_id) VALUE (?,?)", [user['id'], commentId])
        conn.commit()
        status = cursor.rowcount

        # status check
        if status != 1:
            response = Response("DB Error: POST comment_like - no changes were made", mimetype="plain/text", status=499)
    except Exception as E:
        response = Response("DB Error: POST comment_like -"+str(E), mimetype="plain/text", status=499)
    
    c.disconnect_db(conn, cursor)

    # return any value in response that is not None
    if response != None:
        return response
    
    response = format.comment_like([commentId, user['id'], user['name']])

    if response == None:
        response = Response("DB Error: POST comment_like - catch error", mimetype="plain/text", status=499)

    return response    