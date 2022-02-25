import dbinteractions.dbinteractions as c
import helpers.format_output as fo


# Get follows
def get_db(userId):
    conn, cursor = c.connect_db()

    users = None
    response = []
    status_code = 400

    try:
        cursor.execute("SELECT u.id, u.email, u.username, u.bio, u.birthdate, u.imageUrl FROM user u INNER JOIN follow f ON f.follow_id = u.id WHERE f.user_id = ?", [userId])
        users = cursor.fetchall()
        status_code = 200
        # I am okay with it returning nothing
    except Exception as e:
        response = "DB ERROR:"+str(e)

    c.disconnect_db(conn,cursor)

    if users != None:
        # format response output
        for user in users:
            response.append(fo.format_user_output(user))
        
    return response, status_code

def post_db(userId, followId):
    conn, cursor = c.connect_db()

    response = None
    status_code = 400

    try:
        # insert request to db
        cursor.execute('INSERT INTO follow (follow_id')
    except:
        pass