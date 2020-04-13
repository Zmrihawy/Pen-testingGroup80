from models.database import db
import mysql.connector
import models.logger as logger
import datetime

def set_user(username, password, full_name, company, email, 
        street_address, city, state, postal_code, country, ip, path, temp, google_token, temp_token):
    """
    Register a new user in the database
        :param username: The users unique user name
        :param password: The password
        :param full_name: The users full name
        :param company: The company the user represents
        :param email: The users email address
        :param street_address: The street address of the user
        :param city: The city where the user lives
        :param state: The state where the user lives
        :param postal_code: The corresponding postal code
        :param country: The users country
        :param ip: The user's ip address
        :param path: The user's access path
        :param temp: The user's account is temporary or not
        :param google_token: The user's google token
        :param temp_token: The user's access token

        :type username: str
        :type password: str
        :type full_name: str
        :type company: str
        :type email: str
        :type street_address: str
        :type city: str
        :type state: str
        :type postal_code: str
        :type country: str
        :type ip: num
        :type path: str
        :type temp: boolean
        :type google_token: str 
        :type temp_token: str
    """
    db.connect()
    cursor = db.cursor(prepared=True)
    # get register date
    current_time = datetime.datetime.today().strftime('%Y-%m-%d')
    #genereate sql command
    sql_cmd = """INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    sql_value = (username, password, full_name, company,
                 email, street_address, city,
                 state, postal_code, country,current_time,
                 temp, google_token, temp_token)
    #query = ("INSERT INTO users VALUES (NULL, \"" + username + "\", \"" + 
    #    password + "\", \"" + full_name + "\" , \"" + company + "\", \"" + 
    #    email + "\", \"" + street_address + "\", \"" + city + "\", \"" + 
    #    state  + "\", \"" + postal_code + "\", \"" + country + "\")")
    try:
        cursor.execute(sql_cmd, sql_value)
        logger.log_input_msg("register:IP:{}-{}-{}".format(ip, path, sql_value))
        db.commit()
    except mysql.connector.Error as err:
        logger.log_error_msg(err)
        print("Failed executing query register-set_user: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
