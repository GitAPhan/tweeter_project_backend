import secrets
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
            query_keyname += ', imageUrl'
            query_questionmark += ',?'
            query_keyvalue.append(imageUrl)
        else:
            imageUrl = "default image url profile"
        if bannerUrl != None:
            query_keyname += ", bannerUrl"
            query_questionmark += ',?'
            query_keyvalue.append(bannerUrl)
        else:
            bannerUrl = "default image url for banner"
        query_string = f"insert into user ({query_keyname}) values ({query_questionmark})"
        cursor.execute(query_string, query_keyvalue)
        conn.commit()
        userId = cursor.lastrowid
    except db.IntegrityError:
        return "USER: value(s) entered does not meet database requirements", 400
    except db.DataError as de:
        return ("USER: "+str(de)), 400
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
    except db.IntegrityError:
        return "USER: Login error", 400
    except Exception as E:
        return (E), 400
    
    disconnect_db(conn, cursor)

    try:
        if userId == None or loginToken == None:
            raise Exception
        response = format_user_output(
            [userId, email, username, bio, birthdate, imageUrl, bannerUrl, loginToken], True
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

    try:
        query_keyname = ""
        query_keyvalue = [loginToken]
        # modify query selector
        if  email != None:
            query_keyname = ' email=?,' + query_keyname
            query_keyvalue.insert(0, email)
        if  username != None:
            query_keyname = ' username=?,' + query_keyname
            query_keyvalue.insert(0, username)
        if  bio != None:
            query_keyname = ' bio=?,' + query_keyname
            query_keyvalue.insert(0, bio)
        if  birthdate != None:
            query_keyname = ' birthdate=?,' + query_keyname
            query_keyvalue.insert(0, birthdate)
        if  imageUrl != None:
            query_keyname = ' imageUrl=?,' + query_keyname
            query_keyvalue.insert(0, imageUrl)
        if  bannerUrl != None:
            query_keyname = ' bannerUrl=?,' + query_keyname
            query_keyvalue.insert(0, bannerUrl)
        
        query_string = f"update user u inner join login l on u.id = l.user_id set {query_keyname[0:-1]} where l.login_token = ?"

        cursor.execute(query_string, query_keyvalue)
        conn.commit()
        userId = cursor.lastrowid

        if cursor.rowcount == 1:
            disconnect_db(conn, cursor)
            response, status_code = get_user_db(userId)
        else:
            disconnect_db(conn, cursor)
            return 'Patch Error: nothing was updated', 400

    except KeyError:
        print('random error')
    

    return response, status_code

test = {
    "loginToken": "dI1K41mAMTFBcNbjQ2Fc1hzZMWX4Vhbg4OfZXmdha7QT6VXc5JDslpC_u_ERcPqSmzB0kQ9hHNKv6q88KAIi2Q",
    "username": "editPostmanUsr"
}
print(patch_user_db(test["loginToken"],None,test["username"],None,None,None,None))