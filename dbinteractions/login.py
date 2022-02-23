import secrets
import dbinteractions.dbinteractions as db

# # Login requests 
# post login session and create loginToken
def user_login_db(payload, type):
    conn, cursor = db.connect_db()
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

            response = db.format_user_output([profile[0], profile[1], profile[2], profile[3], profile[4], profile[5], profile[6], loginToken], True)
            status_code = 200
        else:
            response = "user profile was NOT logged in"
    except KeyError:
        print('error: Login error')
    
    return response, status_code

# delete login session from db
def user_logout_db(loginToken, userId):
    conn, cursor = db.connect_db()

    status = None
    response = None
    status_code = 400

    try:
        cursor.execute("delete from login where login_token = ? and user_id = ?",[loginToken, userId])
        conn.commit()
        status = cursor.rowcount

        if status == 1:
            response = "USER: You have successfully logged out"
            status_code = 200
        else:
            response = "ERROR: Looks like we weren't able to log you out, please try again in 5 minutes"

    except KeyError as ke:
        print(str(ke))
