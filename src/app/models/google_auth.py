#!/usr/bin/python
import hmac, base64, struct, hashlib, time, json, os
from models.database import db
import mysql.connector
import models.logger as logger

def get_hotp_token(secret, intervals_no):
	"""This is where the magic happens."""
	key = base64.b32decode(normalize(secret), True) # True is to fold lower into uppercase
	msg = struct.pack(">Q", intervals_no)
	h = bytearray(hmac.new(key, msg, hashlib.sha1).digest())
	o = h[19] & 15
	h = str((struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000)
	return prefix0(h)


def get_totp_token(secret):
	"""The TOTP token is just a HOTP token seeded with every 30 seconds."""
	return get_hotp_token(secret, intervals_no=int(time.time())//30)


def normalize(key):
	"""Normalizes secret by removing spaces and padding with = to a multiple of 8"""
	k2 = key.strip().replace(' ','')
	# k2 = k2.upper()	# skipped b/c b32decode has a foldcase argument
	if len(k2)%8 != 0:
		k2 += '='*(8-len(k2)%8)
	return k2


def prefix0(h):
	"""Prefixes code with leading zeros if missing."""
	if len(h) < 6:
		h = '0'*(6-len(h)) + h
	return h

'''
def main():
	rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	with open(os.path.join(rel,'secrets.json'), 'r') as f:
		secrets = json.load(f)
	for label, key in sorted(list(secrets.items())):
		print("{}:\t{}".format(label, get_totp_token(key)))


if __name__ == "__main__":
    main()
'''

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
    
    sql_cmd = """SELECT username FROM users WHERE google_token = %s """
    sql_value = (token,)
    
    try:
        cursor.execute(sql_cmd, sql_value)
        logger.log_input_msg("A user success search_for_google_token:{}-{}-{}".format(ip, fullpath, sql_value))
        token_queries = cursor.fetchall()
        if len(token_queries):
            token_query = token_queries[0][0]
    except mysql.connector.Error as err:
        logger.log_error_msg("Failed executing query search_for_google_token: {}".format(err))
        print("Failed executing query search_for_google_token: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return token_query