from models.database import db
import mysql.connector
import models.logger as logger

def get_users():
    """
    Retreive all registrered users from the database
        :return: users
    """
    db.connect()
    cursor = db.cursor(prepared=True)
    query = ("SELECT userid, username from users")
    try:
        cursor.execute(query)
        #logger.log_input_msg("get_users: {}".format(query))
        users = cursor.fetchall()
    except mysql.connector.Error as err:
        logger.log_error_msg("Failed executing query get_users: {}".format(err))
        print("Failed executing query: {}".format(err))
        users = []
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return users

def get_user_id_by_name(username):
    """
    Get the id of the unique username
        :param username: Name of the user
        :return: The id of the user
    """
    db.connect()
    cursor = db.cursor(prepared=True)
    sql_cmd = """SELECT userid from users WHERE username = %s"""
    sql_value = (username,)
    #query = ("SELECT userid from users WHERE username =\"" + username + "\"")
    userid = None

    try:
        cursor.execute(sql_cmd, sql_value)
        logger.log_input_msg("get_user_id_by_name:{}".format(sql_value))
        users = cursor.fetchall()
        if(len(users)):
            userid = users[0][0]
    except mysql.connector.Error as err:
        logger.log_error_msg("Failed executing query get_user_id_by_name: {}".format(err))
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return userid

def get_user_name_by_id(userid):
    """
    Get username from user id
        :param userid: The id of the user
        :return: The name of the user
    """
    db.connect()
    cursor = db.cursor(prepared=True)
    sql_cmd = """SELECT username from users WHERE userid = %s"""
    sql_value = (userid,)
    #query = ("SELECT username from users WHERE userid =\"" + userid + "\"")
    username = None
    try:
        cursor.execute(sql_cmd, sql_value)
        logger.log_input_msg("get_user_name_by_id: {}".format(sql_value))
        users = cursor.fetchall()
        if len(users):
            username = users[0][0]
    except mysql.connector.Error as err:
        logger.log_error_msg("Failed executing query get_user_name_by_id: {}".format(err))
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return username

def match_user(username, password, ip, fullpath):
    """
    Check if user credentials are correct, return if exists

        :param username: The user attempting to authenticate
        :param password: The corresponding password
        :type username: str
        :type password: str
        :return: user
    """
    db.connect()
    cursor = db.cursor(prepared=True)
     
    sql_cmd = """SELECT userid, username from users where username = %s AND password = %s"""
    sql_value = (username, password,)
    #query = ("SELECT userid, username from users where username = \"" + username + 
    #        "\" and password = \"" + password + "\"")
    user = None
    try:
        cursor.execute(sql_cmd, sql_value)
        logger.log_input_msg("A user success log in-match_user:{}-{}-{}".format(ip, fullpath, sql_value))
        users = cursor.fetchall()
        if len(users):
            user = users[0]
    except mysql.connector.Error as err:
        logger.log_error_msg("Failed executing query match_user: {}".format(err))
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return user

def get_user_hashed_password(username, ip, fullpath):
    """
    Check if user hashed password is match with database
    Need to retreive salt value
        :param username, ip, fullpath: The user attempting to authenticate
        :type username: str
        :return: salt (byte)
    """

    db.connect()
    cursor = db.cursor(prepared=True)
    # query the username
    sql_cmd = """SELECT password FROM users WHERE username = %s"""
    sql_value = (username,)
    
    try:
        cursor.execute(sql_cmd, sql_value)
        logger.log_input_msg("A user attempt in IP get_user_hashed_password:{}-{}-{}".format(ip, fullpath, sql_value))
        password = cursor.fetchall()
        if len(password):
            password_return = password[0][0]
    except mysql.connector.Error as err:
        logger.log_error_msg("Failed executing query get_user_hashed_password: {}".format(err))
        print("Failed executing query get_user_hashed_password: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return password_return

def get_qurery_frequency(username, ip, fullpath):
    """
    Create a lock out function.

        :param username: The user attempting to authenticate
        :type username: str
        :param ip: The user's ip
        :type username: str
        :param fullpath: The user access path
        :type username: str
        :return: times of query
        reference: https://stackoverflow.com/questions/19966123/get-time-interval-in-mysql
    """
    db.connect()
    cursor = db.cursor(prepared=True)
     
    sql_cmd = """SELECT * from user_access_time AS t where username = %s \
        AND t.access_time BETWEEN DATE_ADD(NOW(), INTERVAL -30 MINUTE) AND NOW()"""
    sql_value = (username,)

    try:
        logger.log_input_msg("A attemp to access a user account-get_qurery_frequency:{}-{}-{}".format(ip, fullpath, sql_value))
        cursor.execute(sql_cmd, sql_value)
        result = cursor.fetchall()
        #print("query_result: {}".format(result))
        count_access_time = int(len(result))
    except mysql.connector.Error as err:
        logger.log_error_msg("Failed executing query get_qurery_frequency: {}".format(err))
        print("Failed executing query get_qurery_frequency: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return count_access_time