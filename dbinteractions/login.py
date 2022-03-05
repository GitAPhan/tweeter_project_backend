import json
from flask import Response
import secrets
import dbinteractions.dbinteractions as db
import helpers.format_output as format

# # Login requests 
# post login session and create loginToken
def user_login_db(payload, type):
    status = None
    response = None
    profile = None
    loginToken = secrets.token_urlsafe(64)
    choices = {
        "email": "email",
        "username": "username"
    }
    query_keyname = choices[type]
    conn, cursor = db.connect_db()

    try:
        cursor.execute(f"insert into login (login_token, user_id) values (?,(select id from user where {query_keyname} = ?))",[loginToken, payload])
        conn.commit()
        status = cursor.rowcount
    except KeyError as ke:
        print(str(ke))

    try:
        if status == 1:
            cursor.execute(f"Select id, email, username, bio, birthdate, imageUrl, bannerUrl from user where {query_keyname} = ?",[payload])
            output = cursor.fetchone()
            profile = list(output)
            profile.append(loginToken)
        else:
            response = Response("user profile was NOT logged in", mimetype="plain/text", status=490)
    except Exception as E:
        response = Response("Login Attempt Error:"+str(E), mimetype="plain/text", status=403)
    
    db.disconnect_db(conn, cursor)

    if profile == None:
        response = Response("DB Error: Login general error", mimetype="plain/text", status=403)
    else:
        response = format.user(profile)
        response_json = json.dumps(response, default=str)
        response = Response(response_json, mimetype="application/json", status=200)

    if response == None:
        response = Response("DB Error: Login catch error", mimetype="plain/text", status=403)   

    return response

# delete login session from db
def user_logout_db(loginToken, userId):
    conn, cursor = db.connect_db()

    status = None
    response = None

    try:
        cursor.execute("delete from login where login_token = ? and user_id = ?",[loginToken, userId])
        conn.commit()
        status = cursor.rowcount

        if status == 1:
            response = Response("USER: You have successfully logged out", mimetype="plain/text", status=200)
        else:
            response = Response("ERROR: Looks like we weren't able to log you out, please try again in 5 minutes", mimetype="plain/text", status=491)

    except Exception as E:
        response = Response("DB Error: DELETE logout -"+str(E), mimetype="plain/text", status=491)

    db.disconnect_db(conn, cursor)

    if response == None:
        response = Response("DB Error: DELETE logout - catch error", mimetype="plain/text", status=490)

    return response