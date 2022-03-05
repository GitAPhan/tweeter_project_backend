import json
import dbinteractions.dbinteractions as c
import mariadb as db
import helpers.format_output as format
from flask import Response

# GET tweet from database
def get_db(userId, tweetId):
    response = None
    tweets = None
    query_keyname = ""
    query_keyvalue = None

    if tweetId != None:
        query_keyname = "WHERE t.id = ?"
        query_keyvalue = tweetId
    if userId != None:
        query_keyname = "WHERE t.user_id = ?"
        query_keyvalue = userId
    # if query_keyvalue == None or query_keyname == None:
    #     return Response(
    #         "DB Error: GET - general tweet error", mimetype="plain/text", status=500
    #     )

    query_base = f"SELECT t.id, t.user_id, u.username, t.content, t.created_at, u.imageUrl, t.image_url FROM tweet t INNER JOIN user u on u.id = t.user_id{query_keyname}"

    conn, cursor = c.connect_db()

    try:
        if query_keyvalue == None:
            cursor.execute(query_base)
        else:
            cursor.execute(query_base, [query_keyvalue])
        tweets = cursor.fetchall()
    except KeyError as E:
        return Response(
            "DB Error: GET - tweet error" + str(E), mimetype="plain/text", status=490
        )

    c.disconnect_db(conn, cursor)

    if tweets == None:
        return Response(
            "DB Error: GET - catch error", mimetype="plain/text", status=491
        )

    response = []
    for tweet in tweets:
        x = format.tweet(tweet)
        response.append(x)
    response_json = json.dumps(response, default=str)
    if response == []:
        return Response(response, mimetype="application/json", status=204)
    response = Response(response_json, mimetype="application/json", status=200)

    if response == None:
        response = Response(
            "DB Error: GET catch error", mimetype="plain/text", status=492
        )

    return response


# POST tweet to database
def post_db(userId, content, imageUrl):
    response = None
    tweetId = None

    query_keyname = ""
    query_qmark = ""
    query_keyvalue = [userId, content]
    if imageUrl != None:
        query_keyname = ", image_url"
        query_qmark = ",?"
        query_keyvalue.append(imageUrl)
    query_string = f"INSERT INTO tweet (user_id, content{query_keyname}) VALUE (?,?{query_qmark})"

    conn, cursor = c.connect_db()

    try:
        cursor.execute(query_string, query_keyvalue)
        conn.commit()
        tweetId = cursor.lastrowid
    except Exception as E:
        response = Response("DB Error: POST tweet -"+str(E), mimetype="plain/text", status=490)

    c.disconnect_db(conn, cursor)

    if tweetId == None:
        return Response("DB Error: POST tweet - general error", mimetype="plain/text", status=490)
    
    response = get_db(None, tweetId)

    if response == None:
        response = Response("DB Error: POST tweet - catch error", mimetype="plain/text", status=491)
    
    return response
        
# PATCH tweet to database
def patch_db(userId, tweetId, content, imageUrl):
    response = None
    status = None

    query_keyname = ""
    query_keyvalue = [userId, tweetId]
    if content != None:
        query_keyname += "content=?,"
        query_keyvalue.insert(0, content)
    if imageUrl != None:
        query_keyname += "image_url=?,"
        query_keyvalue.insert(0, imageUrl)
    query_string = f"UPDATE tweet SET {query_keyname[0:1]} WHERE user_id=? and id=?"
    
    conn, cursor = c.connect_db()

    try:
        cursor.execute(query_string, query_keyvalue)
        conn.commit()
        status = cursor.rowcount
    except Exception as E:
        response = Response("DB Error: PATCH tweet -"+str(E), mimetype="plain/text", status=490)
    
    c.disconnect_db(conn, cursor)

    if response != None:
        return response
    if status == None:
        return Response("DB Error: PATCH tweet - general error", mimetype="plain/text", status=491)
    if status == 0:
        return Response("DB Error: PATCH tweet - no changes were made", mimetype="plain/text", status=491)
    else:
        array = [tweetId, content]
        if imageUrl != None:
            array.append(imageUrl)
        response = format.tweet(array)
        
        response_json = json.dumps(response, default=str)
        response = Response(response_json, mimetype="application/json", status=200)
    
    if response == None:
        response = Response("DB Error: PATCH tweet - catch error", mimetype="plain/text", status=492)
    
    return response

# DELETE tweet from database
def delete_db(userId, tweetId):
    response = None
    status = None

    conn, cursor = c.connect_db()

    try:
        cursor.execute("DELETE FROM tweet WHERE user_id = ? and id = ?",[userId, tweetId])
        conn.commit()
        status = cursor.rowcount
    except Exception as E:
        response = Response("DB Error: DELETE tweet -"+str(E), mimetype="plain/text", status=491)
    
    c.disconnect_db(conn, cursor)

    if response != None:
        return response
    elif status == None:
        return Response("DB Error: DELETE tweet - general error", mimetype="plain/text", status=490)
    elif status == 0:
        return Response("DB Error: DELETE tweet - no changes were made", mimetype="plain/text", status=491)
    else:
        response = Response("tweet successfully deleted", mimetype="plain/text", status=200)
    
    if response == None:
        response = Response("DB Error: DELETE tweet - catch error", mimetype="plain/text", status=490)
    
    return response