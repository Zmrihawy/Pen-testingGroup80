from models.database import db
import mysql.connector
import models.logger as logger

def search_for_token(token, ip, fullpath):
    """
    search for user's token
        :param token: The user's token
        :param ip: user's ip address
        :param fullpath: user's accessed file path
        :timestamp: user's accessed time stamp

        :type username: str
        :type email: str
        :param ip: str
        :param fullpath: str

        :return: email
    """

    db.connect()
    cursor = db.cursor(prepared=True)
    
    sql_cmd = """SELECT username FROM users WHERE verify_token = %s """
    sql_value = (token,)
    
    try:
        cursor.execute(sql_cmd, sql_value)
        logger.log_input_msg("A user success search_for_token:{}-{}-{}".format(ip, fullpath, sql_value))
        token_queries = cursor.fetchall()
        if len(token_queries):
            token_query = token_queries[0][0]
    except mysql.connector.Error as err:
        logger.log_error_msg("Failed executing query search_for_token: {}".format(err))
        print("Failed executing query search_for_token: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return token_query

def update_token_to_null(username, ip, fullpath):
    """
    search for user's token
        :param username: The user's name
        :param ip: user's ip address
        :param fullpath: user's accessed file path
        :timestamp: user's accessed time stamp

        :type username: str
        :type email: str
        :param ip: str
        :param fullpath: str

        :return: email
    """

    db.connect()
    cursor = db.cursor(prepared=True)
    
    sql_cmd = """UPDATE users SET verify_token = Null, temp = 0 WHERE username = %s """
    sql_value = (username,)
    
    try:
        cursor.execute(sql_cmd, sql_value)
        logger.log_input_msg("A user success update_token_to_null:{}-{}-{}".format(ip, fullpath, sql_value))
        actions = db.commit()
    except mysql.connector.Error as err:
        logger.log_error_msg("Failed executing query update_token_to_null: {}".format(err))
        print("Failed executing query update_token_to_null: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return actions