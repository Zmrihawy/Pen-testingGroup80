import logging, os, logging.handlers

def log_error_msg (msg):

    try:
        handler = logging.handlers.WatchedFileHandler(
        os.environ.get("LOGFILE", "/var/log/project_logs.log"))
        handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
        root = logging.getLogger()
        root.setLevel(os.environ.get("LOGELVEL", "INFO"))
        root.addHandler(handler)
    except Exception:
        logging.exception("Exception in main()")
        exit(1)
    return