import dbinteractions.dbinteractions as db
import secrets
import mariadb as d
import helpers.format_output as fo

## users
# get user from db
def get_user_db(userId):
    conn, cursor = db.connect_db()
    users = []
    response = []
    status_code = 400

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

        status_code = 200
    except Exception as e:
        return e, status_code

    db.disconnect_db(conn, cursor)

    # format response for easier readability
    for user in users:
        x = fo.format_user_output(user)
        response.append(x)

    return response, status_code


# add user to database
def post_user_db(email, username, password, salt, bio, birthdate, imageUrl, bannerUrl):
    conn, cursor = db.connect_db()
    status_code = 400
    userId = None
    loginToken = None

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
    except d.IntegrityError as ie:
        # changed name of constraints in user to work with the slicing
        return "USER: Invalid value - " + str(ie)[0:-21], 400
    except d.OperationalError as oe:
        return "DB Error: " + str(oe), 500
    except d.DataError as de:
        return ("USER: " + str(de)), 400
    except Exception as E:
        return (E), 400

    try:
        # generate loginToken, add login session
        loginToken = secrets.token_urlsafe(64)
        cursor.execute(
            "insert into login (user_id, login_token) values (?,?)",
            [userId, loginToken],
        )
        conn.commit()
    except d.IntegrityError as ie:
        return "USER: Invalid value - " + str(ie)[0:-21], 400
    except d.OperationalError as oe:
        return "DB Error: " + str(oe), 500
    except Exception as E:
        return (E), 400

    db.disconnect_db(conn, cursor)

    try:
        if userId == None or loginToken == None:
            raise Exception
        response = fo.format_user_output(
            [userId, email, username, bio, birthdate, imageUrl, bannerUrl, loginToken]
        )
        status_code = 201
    except Exception as e:
        return e, 400

    return response, status_code


# edit existing user in db
def patch_user_db(loginToken, email, username, bio, birthdate, imageUrl, bannerUrl):
    conn, cursor = db.connect_db()
    response = "Patch Error: general error"
    status_code = 400
    userId = None

    # check to see if loginToken is valid and catch invalid token exception
    try:
        userId, status_code = db.verify_loginToken(loginToken)
        # conditional to check to see if token was valid
        if status_code == True:
            status_code = 400
        else:
            raise Exception
    except Exception as e:
        return userId, status_code


    try:
        query_keyname = ""
        query_keyvalue = [loginToken]
        # query_keyvalue = [userId]
        
        # modify query selector
        if email != None:
            query_keyname = " u.email=?," + query_keyname
            query_keyvalue.insert(0, email)
        if username != None:
            query_keyname = " u.username=?," + query_keyname
            query_keyvalue.insert(0, username)
        if bio != None:
            query_keyname = " u.bio=?," + query_keyname
            query_keyvalue.insert(0, bio)
        if birthdate != None:
            query_keyname = " u.birthdate=?," + query_keyname
            query_keyvalue.insert(0, birthdate)
        if imageUrl != None:
            query_keyname = " u.imageUrl=?," + query_keyname
            query_keyvalue.insert(0, imageUrl)
        if bannerUrl != None:
            query_keyname = " u.bannerUrl=?," + query_keyname
            query_keyvalue.insert(0, bannerUrl)

        # old query using inner join. Wasn't getting an value returned for lastrowid
        query_string = f"update user u inner join login l on u.id = l.user_id set {query_keyname[0:-1]} where l.login_token = ?"
        # this query also didn't return userId either when using lastrowid
        # query_string = f"update user u set {query_keyname[0:-1]} where u.id = ?"

        cursor.execute(query_string, query_keyvalue)
        conn.commit()
        row_count = cursor.rowcount
        # userId = cursor.lastrowid

        if row_count == 1:
            response, status_code = get_user_db(userId)
        else:
            db.disconnect_db(conn, cursor)
            return "Patch Error: nothing was updated", 400
    except d.OperationalError as oe:
        return "DB Error: " + str(oe), 500
    except d.IntegrityError as ie:
        return "USER: Invalid value - " + str(ie)[0:-21], 400
    except d.DataError as de:
        return ("USER: " + str(de)), 400
    except Exception as E:
        return (E), 400

    db.disconnect_db(conn, cursor)

    return response, status_code

# delete user from database
def delete_user_db(loginToken):
    conn, cursor = db.connect_db()
    status = None
    response = None
    status_code = 400

    try:
        cursor.execute("delete u from user u inner join login l on l.user_id = u.id where l.login_token = ?", [loginToken])
        conn.commit()
        status = cursor.rowcount
    except KeyError as ke:
        print(str(ke))

    if status == 1:
        response = 'user profile successfully deleted'
        status_code = 200
    else:
        response = "user profile was NOT deleted"
    
    return response, status_code