import hashlib
import secrets
import string
import mariadb as db
import dbcreds as c

# create salt, add to password, hash
def hash_the_salted_password(password):
    salt = secrets.token_urlsafe(10)
    password = password + salt
    hash_result = hashlib.sha512(password.encode()).hexdigest()
    return hash_result, salt

# Grab the hashed salty password and the salt to add to the password, hash and verify
def verify_hashed_salty_password(hashed_salty_password, salt, password):
    password = password + salt
    verify_hsp = hashlib.sha512(password.encode()).hexdigest()
    # verify
    if hashed_salty_password == verify_hsp:
        return True
    else:
        return False

# connect to database function
def connect_db():
    conn = None
    cursor = None
    try:
        conn = db.connect(user=c.user,
                          password=c.password,
                          host=c.host,
                          port=c.port,
                          database=c.database)
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
            cursor.execute("Select id, email, username, bio, birthdate, imageUrl, bannerUrl from user")
        else:
            cursor.execute("select id, email, username, bio, birthdate, imageUrl, bannerUrl from user where id = ?", [userId])
        users = cursor.fetchall()

        status_code = 200
    except Exception as e:
        return e, status_code
    
    disconnect_db(conn, cursor)

    # format response for easier readability
    for user in users:
        x = {
            "userId": user[0],
            "email": user[1],
            "username": user[2],
            "bio": user[3],
            "birthdate": user[4],
            "imageUrl": user[5],
            "bannerUrl": user[6]
        }
        response.append(x)
    
    return response, status_code

# add user to database
def post_user_db(email, username, password, bio, birthdate, imageUrl, bannerUrl):
    conn, cursor = connect_db()
    status_code = 400

    try:
        cursor.execute("insert into user (email, username, password, bio, birthdate, imageUrl, bannerUrl) values (?,?,?,?,?,?,?)", [email, username, password, bio, birthdate, imageUrl, bannerUrl])
        conn.commit()
        userId = cursor.lastrowid
    except:
        pass

    try:
        # generate loginToken, add login session
        loginToken = secrets.token_urlsafe(100)
        cursor.execute('insert into login (user_id, login_token) values (?,?)', [userId, loginToken])
        conn.commit()
    except:
        pass

    response = {
        "userId": userId,
        "email": email,
        "username": username,
        "bio": bio,
        "birthdate": birthdate,
        "imageUrl": imageUrl,
        "bannerUrl": bannerUrl,
        "loginToken": loginToken,
    }

    return response, status_code