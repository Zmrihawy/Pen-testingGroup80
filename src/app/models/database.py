import mysql.connector
from dotenv import load_dotenv
import os

groupid = os.getenv("groupid").lstrip("0")

"""
Connect the webserver to the database using the python mysql connecter. 
Change the host address depending on where the mysql server is running. To connect to the 
preconfigured docker container address use the Docker address. The default port is 3306.
"""

# using the latest mysql-python
# therefore reference: https://stackoverflow.com/questions/50557234/authentication-plugin-caching-sha2-password-is-not-supported

db = mysql.connector.connect(
    user='root', 
    password='root',
    host='10.' + groupid + '.0.5',   # Docker address
    #host='0.0.0.0',    # Local address
    database='db',
    charset = 'utf8',
    auth_plugin='mysql_native_password'
)
    
