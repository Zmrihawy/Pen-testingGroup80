from models.database import db
import mysql.connector
import models.logger as logger

def forget_password_match(username, email, ip, fullpath):
    """
    Update user's password
        :param username: The user attempting to authenticate
        :param email: The user's corresponding email
        :param ip: user's ip address
        :param fullpath: user's accessed file path
        :timestamp: user's accessed time stamp
        :type username: str
        :type email: str
        :param ip: str
        :param fullpath: str
        :timestamp: str
        :return: email
    """

    db.connect()
    cursor = db.cursor(prepared=True)
    
    sql_cmd = """SELECT email FROM users WHERE username = %s AND email=%s"""
    sql_value = (username, email,)
    
    try:
        cursor.execute(sql_cmd, sql_value)
        logger.log_input_msg("A user success forget_password_match:{}-{}-{}".format(ip, fullpath, sql_value))
        query_result = cursor.fetchall()
        if len(query_result):
            email = query_result[0][0]
    except mysql.connector.Error as err:
        logger.log_error_msg("Failed executing query forget_password_match: {}".format(err))
        print("Failed executing query forget_password_match: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return email

def update_reset_token(username, token, ip, fullpath):
    """
    Update user's forget token
        :param username: The user attempting to authenticate
        :param email: The user's corresponding email
        :param ip: user's ip address
        :param fullpath: user's accessed file path
        :timestamp: user's accessed time stamp
        :type username: str
        :type email: str
        :param ip: str
        :param fullpath: str
        :timestamp: str
        :return: email
    """

    db.connect()
    cursor = db.cursor(prepared=True)
    
    sql_cmd = """UPDATE users SET verify_token = %s WHERE username = %s"""
    sql_value = (token, username,)
    
    try:
        cursor.execute(sql_cmd, sql_value)
        logger.log_input_msg("A user success update_reset_token:{}-{}-{}".format(ip, fullpath, sql_value))
        db.commit()
    except mysql.connector.Error as err:
        logger.log_error_msg("Failed executing query update_reset_token: {}".format(err))
        print("Failed executing query update_reset_token: {}".format(err))
        cursor.fetchall()
        exit(1)
    except Exception as e:
        print("An exception occur during execute update_reset_token {}".format(e))
    finally:
        cursor.close()
        db.close()
    return