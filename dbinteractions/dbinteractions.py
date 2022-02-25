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
