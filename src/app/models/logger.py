import logging, os, logging.handlers
import getpass
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
        logger.log(logging.error, str(msg))
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