import secrets
import mariadb as db
import dbinteractions.dbcreds as c


## custom functions


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

