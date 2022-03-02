import json
import dbinteractions.dbinteractions as c
import mariadb as db
import helpers.format_output as fo
from flask import Response

# GET tweet from database
def get_db(userId, tweetId):
    response = None
    tweets = None
    query_keyname = None
    query_keyvalue = None
    
    if tweetId != None:
        query_keyname = 't.id'
        query_keyvalue = tweetId
    if userId != None:
        query_keyname = 't.user_id'
        query_keyvalue = userId
    if query_keyvalue == None or query_keyname == None:
        return Response("DB Error: GET - general tweet error", mimetype="plain/text", status=500)

    query_base = f"SELECT t.id, t.user_id, u.username, t.content, t.created_at, u.imageUrl, t.image_url FROM tweet t INNER JOIN user u on u.id = t.user_id WHERE {query_keyname} = ?"
    
    conn, cursor = c.connect_db()

    try:
        cursor.execute(query_base, [query_keyvalue])
        tweets = cursor.fetchall()
    except Exception as E:
        return Response("DB Error: GET - tweet error"+str(E), mimetype="plain/text", status=490)
    
    c.disconnect_db(conn, cursor)

    if tweets == None:
        return Response("DB Error: GET - catch error", mimetype="plain/text", status=491)
    
    response = []
    for tweet in tweets:
        x = fo.format_tweet_output(tweet)
        response.append(x)
    response_json = json.dumps(response, default=str)
    if response == []:
        return Response(response, mimetype="application/json", status=204)
    response = Response(response_json, mimetype="application/json", status=200)

    if response == None:
        response = Response("DB Error: GET catch error", mimetype="plain/text", status=492)

    return response