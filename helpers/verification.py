import hashlib
import re
import secrets
import mariadb as db
from dbinteractions.dbinteractions import connect_db as connect_db
from dbinteractions.dbinteractions import disconnect_db as disconnect_db

# verify that the password is not weak
def verify_password(password):
    if len(password) < 8:
        return False
    # regex validation: needs to contain upper, lower, numeric, and a special character
    if re.fullmatch(r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W])(?!.*[\s]).{8,64})', password):
        return True
    else:
        return False

# verify that user input username is valid
def verify_username(username):
    # username cannot contain a whitespace and between 8-64 characters
    if re.fullmatch(r'((?!.*[\s]).{8,64})', username):
        return True
    else:
        return False

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