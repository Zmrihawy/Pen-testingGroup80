from models.database import db

def set_user(username, password, full_name, company, phone_number, 
        street_address, city, state, postal_code, country):
    """
    Register a new user in the database
        :param username: The users unique user name
        :param password: The password
        :param full_name: The users full name
        :param company: The company the user represents
        :param phone_number: The phone number of the user
        :param street_address: The street address of the user
        :param city: The city where the user lives
        :param state: The state where the user lives
        :param postal_code: The corresponding postal code
        :param country: The users country
        :type username: str
        :type password: str
        :type full_name: str
        :type company: str
        :type phone_number: str
        :type street_address: str
        :type city: str
        :type state: str
        :type postal_code: str
        :type country: str
    """
    cursor = db.cursor()
    query = ("INSERT INTO users VALUES (NULL, \"" + username + "\", \"" + 
    password + "\", \"" + full_name + "\" , \"" + company + "\", \"" + 
    phone_number + "\", \"" + street_address + "\", \"" + city + "\", \"" +
    state  + "\", \"" + postal_code + "\", \"" + country + "\")")
    cursor.execute(query)
    db.commit()
    cursor.close()
