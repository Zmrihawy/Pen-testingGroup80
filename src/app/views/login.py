import web
from views.forms import login_form
import models.user
from views.utils import get_nav_bar, csrf, csrf_decorate
import os, hmac, base64, json
import hashlib, binascii
import datetime, time
from models.logger import record_user_login
# Get html templates
render = web.template.render('templates/')

# Set global token
web.template.Template.globals['csrf_token'] = csrf
count = 0
class Login():

    # Get the server secret to perform signatures
    secret = web.config.get('session_parameters')['secret_key']

    def GET(self):
        """
        Show the login page
            
            :return: The login page showing other users if logged in
        """
        session = web.ctx.session
        nav = get_nav_bar(session)

        # Log the user in if the rememberme cookie is set and valid
        self.check_rememberme()

        return render.login(nav, login_form, "")

    @csrf_decorate
    def POST(self):
        """
        Log in to the web application and register the session
            :return:  The login page showing other users if logged in
        reference: https://www.vitoshacademy.com/hashing-passwords-in-python/
        reference: https://stackoverflow.com/questions/34046634/insert-into-a-mysql-database-timestamp/34047276 
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input(username="", password="", remember=False)
        
        current_time = time.time()

        try:
            # log ip information
            ip_addr = web.ctx["ip"]
            accessed_path = web.ctx["fullpath"]

            #get user's salt and password with attempt try
            log_time_date = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
            record_user_login(data.username, ip_addr, accessed_path, log_time_date)
            #print("logged_login")
            stored_password = models.user.get_user_hashed_password(data.username, ip_addr, accessed_path)

            #check data password exits
            if data.password:
                # match with database
                # get salt value, type<str>
                salt = stored_password[:64]
                password = stored_password[64:]
                # Validate login credential
                hashed_password = hashlib.pbkdf2_hmac(
                    'sha512', #using sha 256 algorithm
                    data.password.encode('utf-8'), #endcoded with utf8
                    salt.encode('ascii'), # adding salt
                    100000# set the iteration time 10000
                    )
            
                hashed_password = binascii.hexlify(hashed_password).decode('ascii')
            
                test_password = (salt + hashed_password)
                # look for the attemptions to try count
                try_times = 0
                try_times = models.user.get_qurery_frequency(data.username, ip_addr, accessed_path)
                print(try_times)
             # If there is a matching user/password in the database the user is logged in
                if hashed_password == password:
                    user = models.user.match_user(data.username, test_password, ip_addr, accessed_path)
                    self.login(user[1], user[0], data.remember)
                    raise web.seeother("/")
                elif try_times < 3:
                    count += 1
                    return render.login(nav, login_form, "- Login Attemp {} time(s)".format(str(count)))
                else:
                    return render.login(nav, login_form, "- User authentication failed")
            else:
                return render.login(nav, login_form, "- Please provide password")
            
            #password_hash = hashlib.md5(b'TDT4237' + data.password.encode('utf-8')).hexdigest()
            
        except:
            return render.login(nav, login_form, "- Something went wrong!")


    def login(self, username, userid, remember):
        """
        Log in to the application
        """
        session = web.ctx.session
        session.username = username
        session.userid = userid
        if remember:
            rememberme = self.rememberme()
            web.setcookie('remember', rememberme , 300000000)

    def check_rememberme(self):
        """
        Validate the rememberme cookie and log in
        """
        username = ""
        sign = ""
        # If the user selected 'remember me' they log in automatically
        try:
            # Fetch the users cookies if it exists
            cookies = web.cookies()
            # Fetch the remember cookie and convert from string to bytes
            remember_hash = bytes(cookies.remember[2:][:-1], 'ascii')
            # Decode the hash
            decode = base64.b64decode(remember_hash)
            # Load the decoded hash to receive the host signature and the username
            username, sign = json.loads(decode)
        except AttributeError as e:
            # The user did not have the stored remember me cookie
            pass

        # If the users signed cookie matches the host signature then log in
        if self.sign_username(username) == sign:
            userid = models.user.get_user_id_by_name(username)
            self.login(username, userid, False)

    def rememberme(self):
        """
        Encode a base64 object consisting of the username signed with the
        host secret key and the username. Can be reassembled with the
        hosts secret key to validate user.
            :return: base64 object consisting of signed username and username
        """
        session = web.ctx.session
        creds = [ session.username, self.sign_username(session.username) ]
        return base64.b64encode(json.dumps(creds))

    @classmethod
    def sign_username(self, username):
        """
        Sign the current users name with the hosts secret key
            :return: The users signed name
        """
        secret = base64.b64decode(self.secret)
        return hmac.HMAC(secret, username.encode('ascii')).hexdigest()
 