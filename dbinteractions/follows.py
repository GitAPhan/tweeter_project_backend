import json
import dbinteractions.dbinteractions as c
import mariadb as db
import helpers.format_output as fo
from flask import Response


# GET follows
def get_db(userId):
    conn, cursor = c.connect_db()

    users = None
    response = None

    try:
        cursor.execute(
            "SELECT u.id, u.email, u.username, u.bio, u.birthdate, u.imageUrl FROM user u INNER JOIN follow f ON f.follow_id = u.id WHERE f.user_id = ?",
            [userId],
        )
        users = cursor.fetchall()
        if users != None:
            response = []
            # format response output
            for user in users:
                response.append(fo.format_user_output(user))
            # RESPONSE
            if response == []:
                return Response("YOU FOLLOW NO ONE", mimetype="plain/text", status=204)
            response_json = json.dumps(response, default=str)
            response = Response(
                response_json, mimetype="application/json", status="200"
            )
    except Exception as e:
        response = Response("DB ERROR:" + str(e), mimetype="plain/text", status=490)

    c.disconnect_db(conn, cursor)

    if response == None:
        response = Response(
            "DB ERROR: generic database error", mimetype="plain/text", status=491
        )

    return response


# POST follows
def post_db(userId, followId):
    conn, cursor = c.connect_db()

    response = None
    status_code = None

    try:
        # insert request to db
        cursor.execute(
            "INSERT INTO follow (follow_id, user_id) values (?,?)", [userId, followId]
        )
        conn.commit()
        status_code = cursor.rowcount

        if status_code == 1:
            response = Response(
                "Good response from DB", mimetype="plain/text", status=290
            )  # good response
        else:
            response = Response(
                "BAD response from DB", mimetype="plain/text", status=490
            )  # BAD response
    except db.IntegrityError as IE:
        c.disconnect_db(conn, cursor)
        return Response(
            "db.IntergrityError: " + str(IE), mimetype="plain/text", status=499
        )
        # response = "INVALID  follow request, incorrect followId"

    c.disconnect_db(conn, cursor)

    # if none check
    if response == None or status_code == None:
        response = Response("ALL HELL BROKE LOOSE", mimetype="plain/text", status=491)
    return response
