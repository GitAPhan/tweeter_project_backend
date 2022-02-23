import secrets
from unittest import result
import mariadb as db
import dbcreds as c

# # Custon exceptions
#

## custom functions
# format user request output
def format_user_output(user, loginToken):
    if loginToken:
        return {
            "userId": user[0],
            "email": user[1],
            "username": user[2],
            "bio": user[3],
            "birthdate": user[4],
            "imageUrl": user[5],
            "bannerUrl": user[6],
            "loginToken": user[7],
        }
    else:
        return {
            "userId": user[0],
            "email": user[1],
            "username": user[2],
            "bio": user[3],
            "birthdate": user[4],
            "imageUrl": user[5],
            "bannerUrl": user[6],
        }


# connect to database function
def connect_db():
    conn = None
    cursor = None
    try:
        conn = db.connect(
            user=c.user,
            password=c.password,
            host=c.host,
            port=c.port,
            database=c.database,
        )
        cursor = conn.cursor()
    except db.OperationalError:
        print("something went wrong with the DB, please try again in 5 minutes")
    except Exception as e:
        print(e)
        print("Something went wrong!")
    return conn, cursor


# disconnect from database function
def disconnect_db(conn, cursor):
    try:
        cursor.close()
    except Exception:
        print(e)
        print("cursor close error: what happened?")

    try:
        conn.close()
    except Exception as e:
        print(e)
        print("connection close error")

# verify that the loginToken in valid
def verify_loginToken(loginToken):
    conn, cursor = connect_db()
    userId = None

    try:
        # couldn't get the lastrowid to work so I had to add in an additional query
        # might as well use it to authenticate the loginToken
        cursor.execute("select user_id from login where login_token = ?", [loginToken])
        userId = cursor.fetchone()[0]
    except TypeError:
        disconnect_db(conn,cursor)
        return "USER: invalid 'loginToken'", 401
    except db.OperationalError as oe:
        disconnect_db(conn,cursor)
        return "DB Error: " + str(oe), 500
    except Exception as E:
        disconnect_db(conn,cursor)
        return (E), 400
    
    disconnect_db(conn,cursor)
    return userId, True

# grab hashed_password and salt from database to be verified
def get_hashpass_salt_db(payload, type):
    conn, cursor = connect_db()
    result = None

    # modify query 
    choices = {
        "loginToken": "l.login_token",
        "username": "u.username",
        "email": "u.email"
    }
    query_selector = choices[type]
    query_statement = f"select password, salt from user u inner join login l on l.user_id = u.id where {query_selector} = ?"

    try:
        cursor.execute(query_statement, [payload])
        result = cursor.fetchone()
    except KeyError:
        pass
    
    disconnect_db(conn, cursor)

    if result == None:
        return False, "USER: invalid authentication - 'loginToken' not found"
    else:
        return result[0], result[1]

## users
# get user from db
def get_user_db(userId):
    conn, cursor = connect_db()
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

    disconnect_db(conn, cursor)

    # format response for easier readability
    for user in users:
        x = format_user_output(user, False)
        response.append(x)

    return response, status_code


# add user to database
def post_user_db(email, username, password, salt, bio, birthdate, imageUrl, bannerUrl):
    conn, cursor = connect_db()
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
    except db.IntegrityError as ie:
        # changed name of constraints in user to work with the slicing
        return "USER: Invalid value - " + str(ie)[0:-21], 400
    except db.OperationalError as oe:
        return "DB Error: " + str(oe), 500
    except db.DataError as de:
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
    except db.IntegrityError as ie:
        return "USER: Invalid value - " + str(ie)[0:-21], 400
    except db.OperationalError as oe:
        return "DB Error: " + str(oe), 500
    except Exception as E:
        return (E), 400

    disconnect_db(conn, cursor)

    try:
        if userId == None or loginToken == None:
            raise Exception
        response = format_user_output(
            [userId, email, username, bio, birthdate, imageUrl, bannerUrl, loginToken],
            True,
        )
        status_code = 201
    except Exception as e:
        return e, 400

    return response, status_code


# edit existing user in db
def patch_user_db(loginToken, email, username, bio, birthdate, imageUrl, bannerUrl):
    conn, cursor = connect_db()
    response = "Patch Error: general error"
    status_code = 400
    userId = None

    # check to see if loginToken is valid and catch invalid token exception
    try:
        userId, status_code = verify_loginToken(loginToken)
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
            disconnect_db(conn, cursor)
            return "Patch Error: nothing was updated", 400
    except db.OperationalError as oe:
        return "DB Error: " + str(oe), 500
    except db.IntegrityError as ie:
        return "USER: Invalid value - " + str(ie)[0:-21], 400
    except db.DataError as de:
        return ("USER: " + str(de)), 400
    except Exception as E:
        return (E), 400

    disconnect_db(conn, cursor)

    return response, status_code

# delete user from database
def delete_user_db(loginToken):
    conn, cursor = connect_db()
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

# # Login requests 
# post login session and create loginToken
def user_login_db(payload, type):
    conn, cursor = connect_db()
    status = 0
    response = None
    status_code = 400
    loginToken = secrets.token_urlsafe(64)
    choices = {
        "email": "email",
        "username": "username"
    }
    query_keyname = choices[type]

    try:
        cursor.execute(f"insert into login (login_token, user_id) values (?,(select id from user where {query_keyname} = ?))",[loginToken, payload])
        conn.commit()
        status = cursor.rowcount
    except KeyError as ke:
        print(str(ke))

    try:
        if status == 1:
            cursor.execute(f"Select id, email, username, bio, birthdate, imageUrl, bannerUrl from user where {query_keyname} = ?",[payload])
            profile = cursor.fetchone()

            response = format_user_output([profile[0], profile[1], profile[2], profile[3], profile[4], profile[5], profile[6], loginToken], True)
            status_code = 200
        else:
            response = "user profile was NOT logged in"
    except KeyError:
        print('error: Login error')
    
    return response, status_code




# test = {
#     "loginToken": "dI1K41mAMTFBcNbjQ2Fc1hzZMWX4Vhbg4OfZXmdha7QT6VXc5JDslpC_u_ERcPqSmzB0kQ9hHNKv6q88KAIi2Q",
#     "username": "editPostmanusr",
#     "email": "newEmailTest@remailhub.com"
# }
# print(patch_user_db(test["loginToken"],test["email"],test["username"],"Lets change the bio as well to make sure everything is working",None,None,None))

# test for loginToken verification
# loginToken = "dI1K41mAMTFBcNbjQ2Fc1hzZMWX4Vhbg4OfZXmdha7QT6VXc5JDslpC_u_ERcPqSmzB0kQ9hHNKv6q88KAIi2Q"
# x, y = get_hashpass_salt_db(loginToken)
# print(x)
# print(y)
# print("")
# print("")

# loginToken = "Sl57g0K7TGt-1HKyQKj6t3am13H3rJzKdfWCzM7NFUJYMHdt4UkFIo_ljLONrNRk5roUaoYMgrCmt5u0HeWRaA"
# x, y = verify_loginToken(loginToken)
# print(x)
# print(y)
# print("")
# print("")

# loginToken = "momZgXMgp2eTG4V_YTpZZcVI9vGa3WhY8iPgo2AYDxQ_X3hsceavMDteWg1P5VvdA1yD6001B4HVSbD3YDc6Qw"
# x, y = verify_loginToken(loginToken)
# print(x)
# print(y)
# print("")
# print("")

# loginToken = "rcNwsXhGBeredzwtewFiHqrDdnG4GDsXmWeXvYTOocInGl--DHY3t523fl_JGyM8hkwohO7mWrPvDh-Yxs-aOg"
# x, y = verify_loginToken(loginToken)
# print(x)
# print(y)
# print("")
# print("")

# loginToken = "1XMdnkTR1J9ONiexFLmN5eu6U_s9zXpdy8oQUeAPFYiQ9Iv4YBlbiu8Am8o4z4S52XYPdPVVmr9KCiCdr2wbnQ"
# x, y = verify_loginToken(loginToken)
# print(x)
# print(y)
# print("")
# print("")
