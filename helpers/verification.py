import hashlib
import re
import secrets
from flask import Response
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
    verify_status = None

    try:
        # query to select userId and username of user related to the loginToken
        cursor.execute("SELECT u.id, u.username FROM login l INNER JOIN user u ON u.id = l.user_id WHERE l.login_token = ?", [loginToken])
        response = cursor.fetchall()[0]
        userId = {
            'id': response[0],
            'name': response[1]
        }
        
        if isinstance(userId["userId"], int):
            verify_status = True

    except TypeError:
        userId = Response("USER: invalid 'loginToken'", mimetype="plain/text", status=401)
        verify_status = False
    except db.OperationalError as oe:
        userId = Response("DB Error: " + str(oe), mimetype="plain/text", status=500)
        verify_status = False
    except Exception as E:
        userId = Response("Verify Error: general 'loginToken' error"+str(E), mimetype="plain/text", status=498)
        verify_status = False
    
    disconnect_db(conn,cursor)
    return userId, verify_status