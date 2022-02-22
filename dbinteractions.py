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
    # except Exception as E:
    #     print(E)

    try:
        # generate loginToken, add login session
        loginToken = secrets.token_urlsafe(64)
        cursor.execute(
            "insert into login (user_id, login_token) values (?,?)",
            [userId, loginToken],
        )
        conn.commit()
    except db.IntegrityError:
        return "USER: value(s) entered does not meet database requirements", 400
    # except Exception as E:
    # print(E)

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