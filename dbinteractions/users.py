import json
from flask import Response
import dbinteractions.dbinteractions as db
import secrets
import mariadb as d
import helpers.format_output as format

## users
# get user from db
def get_db(userId):
    conn, cursor = db.connect_db()
    users = None
    response = None

    try:
        # conditional for query selector
        if userId == None:
            cursor.execute(
                "Select id, email, username, bio, birthdate, imageUrl, bannerUrl from user"
            )
        else:
            cursor.execute(
                "select id, email, username, bio, birthdate, imageUrl, bannerUrl from user where id = ?",
                [userId],
            )
        users = cursor.fetchall()
    except Exception as e:
        return Response("DB Error: general GET error"+str(e), mimetype="plain/text", status=490)

    db.disconnect_db(conn, cursor)

    if users == None:
        return Response("DB Error: general GET error", mimetype="plain/text", status=491)
    else:
        response = []
        # format response for easier readability
        for user in users:
            x = format.user(user)
            response.append(x)
    
    if response != []:
        response_json = json.dumps(response, default=str)
        response = Response(response_json, mimetype="application/json", status=200)

    return response


# add user to database
def post_user_db(email, username, password, salt, bio, birthdate, imageUrl, bannerUrl):
    conn, cursor = db.connect_db()
    userId = None
    loginToken = None
    response = None

    try:
        query_keyname = "email, username, password, salt, bio, birthdate"
        query_questionmark = "?,?,?,?,?,?"
        query_keyvalue = [email, username, password, salt, bio, birthdate]
        if imageUrl != None:
            query_keyname += ", imageUrl"
            query_questionmark += ",?"
            query_keyvalue.append(imageUrl)
        else:
            imageUrl = "default image url profile"
        if bannerUrl != None:
            query_keyname += ", bannerUrl"
            query_questionmark += ",?"
            query_keyvalue.append(bannerUrl)
        else:
            bannerUrl = "default image url for banner"
        query_string = (
            f"insert into user ({query_keyname}) values ({query_questionmark})"
        )
        cursor.execute(query_string, query_keyvalue)
        conn.commit()
        userId = cursor.lastrowid
        if isinstance(userId, int) == False:
            response = Response("No user created!", mimetype="plain/text", status=490)
    except d.IntegrityError as ie:
        # changed name of constraints in user to work with the slicing
        response = Response("USER: Invalid value - " + str(ie)[0:-21], mimetype='plain/text', status=400)
    except d.OperationalError as oe:
        response = Response("DB Error: " + str(oe), mimetype='plain/text', status=500)
    except d.DataError as de:
        response = Response("USER: " + str(de), mimetype='plain/text', status=400)
    except Exception as E:
        response = Response("DB Error: general POST error" + str(E), mimetype='plain/text', status=491)

    if response == None:
        try:
            # generate loginToken, add login session
            loginToken = secrets.token_urlsafe(64)
            cursor.execute(
                "insert into login (user_id, login_token) values (?,?)",
                [userId, loginToken],
            )
            conn.commit()
        except d.IntegrityError as ie:
            response = Response("USER: Invalid value - " + str(ie)[0:-21], mimetype='plain/text', status=400)
        except d.OperationalError as oe:
            response = Response("DB Error: " + str(oe), mimetype='plain/text', status=500)
        except Exception as E:
            response = Response("DB Error: general POST error" + str(E), mimetype='plain/text', status=491)

    db.disconnect_db(conn, cursor)

    if response != None:
        return response
    if userId == None or loginToken == None:
        return Response('DB Error: general POST error', mimetype="plain/text", status=492)
    response = format.user(
        [userId, email, username, bio, birthdate, imageUrl, bannerUrl, loginToken]
    )
    response_json = json.dumps(response, default=str)
    response = Response(response_json, mimetype="application/json", status=200)

    return response


# edit existing user in db
def patch_db(userId, email, username, bio, birthdate, imageUrl, bannerUrl):
    conn, cursor = db.connect_db()
    response = None
    status_code = None

    try:
        query_keyname = ""
        query_keyvalue = [userId]
        # query_keyvalue = [userId]
        
        # modify query selector
        if email != None:
            query_keyname = " email=?," + query_keyname
            query_keyvalue.insert(0, email)
        if username != None:
            query_keyname = " username=?," + query_keyname
            query_keyvalue.insert(0, username)
        if bio != None:
            query_keyname = " bio=?," + query_keyname
            query_keyvalue.insert(0, bio)
        if birthdate != None:
            query_keyname = " birthdate=?," + query_keyname
            query_keyvalue.insert(0, birthdate)
        if imageUrl != None:
            query_keyname = " imageUrl=?," + query_keyname
            query_keyvalue.insert(0, imageUrl)
        if bannerUrl != None:
            query_keyname = " bannerUrl=?," + query_keyname
            query_keyvalue.insert(0, bannerUrl)

        # old query using inner join. Wasn't getting an value returned for lastrowid
        query_string = f"update user set {query_keyname[0:-1]} where id=?"
        # this query also didn't return userId either when using lastrowid
        # query_string = f"update user u set {query_keyname[0:-1]} where u.id = ?"

        cursor.execute(query_string, query_keyvalue)
        conn.commit()
        row_count = cursor.rowcount
        # userId = cursor.lastrowid

        if row_count == 1:
            response = get_db(userId)
        else:
            response = Response("Patch Error: nothing was updated", mimetype="plain/text", status=490)
    except d.OperationalError as oe:
        response = Response("DB Error: " + str(oe), mimetype="plain/text", status=500)
    except d.IntegrityError as ie:
        response = Response("USER: Invalid value - " + str(ie)[0:-21], mimetype="plain/text", status=400)
    except d.DataError as de:
        response = Response("USER: " + str(de), mimetype="plain/text", status=400)
    except Exception as E:
        response = Response("DB Error: general PATCH error"+str(E),mimetype="plain/text", status=400)

    db.disconnect_db(conn, cursor)

    if status_code == None or response == None:
        response = Response("DB Error: PATCH catch error", mimetype="plain/text", status=491)

    return response

# delete user from database
def delete_db(loginToken):
    conn, cursor = db.connect_db()
    status = None
    response = None

    try:
        cursor.execute("delete u from user u inner join login l on l.user_id = u.id where l.login_token = ?", [loginToken])
        conn.commit()
        status = cursor.rowcount
    except Exception as e:
        response = Response("DB Error: general DELETE error" + str(e), mimetype="plain/text", status=490)

    if status == 1:
        response = Response('user profile successfully deleted', mimetype="plain/text", status=200)
    else:
        response = Response("user profile was NOT deleted", mimetype="plain/text", status=491)
    
    return response