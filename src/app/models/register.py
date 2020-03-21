from models.database import db
import mysql.connector
import models.logger as logger

def set_user(username, password, full_name, company, email, 
        street_address, city, state, postal_code, country):
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
    """
    db.connect()
    cursor = db.cursor()
    sql_cmd = """INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    sql_value = (username, password, full_name, company, 
                 email, street_address, city, 
                 state, postal_code, country)
    #query = ("INSERT INTO users VALUES (NULL, \"" + username + "\", \"" + 
    #    password + "\", \"" + full_name + "\" , \"" + company + "\", \"" + 
    #    email + "\", \"" + street_address + "\", \"" + city + "\", \"" + 
    #    state  + "\", \"" + postal_code + "\", \"" + country + "\")")
    try:
        cursor.execute(sql_cmd, sql_value)
        db.commit()
    except mysql.connector.Error as err:
        logger.log_error_msg(err)
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
