import logging, os, logging.handlers
import getpass
from models.database import db
import mysql.connector
# Reference
# http://yhhuang1966.blogspot.com/2018/04/python-logging_24.html
# https://cuiqingcai.com/6080.html 

def log_error_msg (msg):
    user = getpass.getuser() #knowing whose using
    logger = logging.getLogger(user) # enter username
    logger.setLevel(logging.DEBUG) #set debug level
    #set the recording form
    record_format = '%(asctime)s - %(levelname)s -%(name)s : %(message)s' 
    load_seted_format = logging.Formatter(record_format) # read format
    #handler_stream = logging.StreamHandler().setFormatter(load_seted_format) # call the StreamHandler obj
    #logger.addHandler(handler_stream) # put handler into work

    try:
        location_logfile = "mysql_error.txt"
        handler_file = logging.FileHandler(location_logfile)
        #formatted obj
        handler_file.setFormatter(load_seted_format) 
        #assign one handler
        logger.addHandler(handler_file)
        logger.log(logging.ERROR, str(msg))
        """
        handler = logging.handlers.WatchedFileHandler(
        os.environ.get("LOGFILE", "/var/log/mysql.log"))
        handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
        root = logging.getLogger()
        root.setLevel(os.environ.get("LOGELVEL", "INFO"))
        root.addHandler(handler)
        """
    except Exception:
        logging.exception("Exception in main()")
        exit(1)
    return

def log_input_msg (msg):
    user = getpass.getuser() #knowing whose using
    logger = logging.getLogger(user) # enter username
    logger.setLevel(logging.DEBUG) #set debug level
    #set the recording form
    record_format = '%(asctime)s - %(levelname)s -%(name)s : %(message)s' 
    load_seted_format = logging.Formatter(record_format) # read format
    #handler_stream = logging.StreamHandler().setFormatter(load_seted_format) # call the StreamHandler obj
    #logger.addHandler(handler_stream) # put handler into work

    try:
        location_logfile = "mysql_input_query.txt"
        #wrtie file with stated format obj
        handler_file = logging.FileHandler(location_logfile)
        #formatted obj
        handler_file.setFormatter(load_seted_format) 
        #assign one handler
        logger.addHandler(handler_file)
        logger.log(logging.WARNING, str(msg))
    except Exception:
        logging.exception("Exception in main()")
        exit(1)
    return

def record_user_login(username, ip, fullpath, access_time):
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
    #print("enter logger!")
    # log the request
    sql_cmd_log = """INSERT INTO user_access_time VALUES (NULL, %s, %s, %s)"""
    #print (sql_cmd_log)
    msg = "A user attempt:IP:{}-{}".format(ip, fullpath)
    #print(len(msg))
    sql_value_log = (username, msg, access_time,)

    try:
        cursor.execute(sql_cmd_log, sql_value_log)
        log_input_msg("A user attempt in IP record_user_login:{}-{}-{}".format(ip, fullpath, sql_value_log))
        db.commit()
    except mysql.connector.Error as err:
        log_error_msg("Failed executing query record_user_login: {}".format(err))
        print("Failed executing query record_user_login: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return