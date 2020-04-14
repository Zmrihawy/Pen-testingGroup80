import web, pyqrcode, os, json, png
from views.forms import register_form
from models.register import set_user
from models.user import get_user_id_by_name
from views.utils import get_nav_bar, csrf, csrf_decorate, generate_salt, hashed_value, generate_token, generate_google_token
from models.google_auth import get_totp_token

# Get html templates
render = web.template.render('templates/')

# Set global token
web.template.Template.globals['csrf_token'] = csrf

class Register:

    def GET(self):
        """
        Get the registration form

            :return: A page with the registration form
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        return render.register(nav, register_form, "")

    @csrf_decorate
    def POST(self):
        """
        Handle input data and register new user in database

            :return: Main page
        """
        # get session information
        session = web.ctx.session        
        nav = get_nav_bar(session)
        data = web.input()

        register = register_form()

        # check user is exites or not
        if not register.validates():
            return render.register(nav, register, "All fields must be valid.")

        # Check if user exists
        if get_user_id_by_name(data.username):
            return render.register(nav, register, "Invalid user, already exists.")
        
        try:
            """
            Using salt to protect user's password
            And write in database.
            """
            ip_addr = web.ctx["ip"]
            path = web.ctx["fullpath"]
            # generate salt value
            salt = generate_salt()
            # protect password with sha 256
            hashed_password = hashed_value(data.password, salt)

            # generate salted password string
            password = (salt+hashed_password)

            # set this account as unverified
            temp_account = True

            # generate a save url token
            temp_token = generate_token()

            #TODO: generate a google token
            google_token_raw = generate_google_token()
            google_token = self.get_google_auth_token(data.username, google_token_raw)
            
            try:
                # send web mail
                # Send user email
                reset_url = "http://molde.idi.ntnu.no:80/two_fa?reset_token=" + temp_token
                # for school
                # reset_url = "http://molde.idi.ntnu.no:80" + temp_token
                msg = "Please verfiy your account via this link.\n" + str(reset_url)

                print( "======" * 8 +"Ready to send mail!")
                #send_mail (currently it is currpted)
                #self.send_mail(data.email, msg)
            except:
                pass
            
            # write into database
            set_user(data.username, password, data.full_name, data.company, data.email, data.street_address,
            data.city, data.state, data.postal_code, data.country, ip_addr, path, temp_account, google_token, temp_token)

            # msg for notification
            return render.register(nav, register_form, "User registered and verified with email!\n" + reset_url)
        except:
            print(exit[0])
            return render.register(nav, register_form, "Fail to register!")

    def send_mail(self, mail, msg):
        smtp_server = "molde.idi.ntnu.no:25"
        web.config.smtp_server = smtp_server
        web.sendmail('beelance@ntnu.no', mail, 'Account verify from Beelance', msg)
        return
    
    def get_google_auth_token(self, username, google_token):
        #access current folder
        rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname("token_img")))
        #print("-" * 16)
        #print(str(rel))

        try:
            # generate token imaage
            token_url_str = "otpauth://totp/Beelance:" + username +"?secret=" + google_token + "&issuer=Beelance"
            
            qrcoe_img = pyqrcode.create(token_url_str)
            #print("-" * 16)
            #print("image created!")
            qrcoe_img.png(rel+"/static/picture.png")
        
            # generate json
            data = {}
            data.update({
                username:google_token,
            })
            # save json file
            with open(os.path.join(rel, 'secrets.json'), 'w') as opened_file:
                json.dump(data, opened_file)
            print("-" * 16 +"\n saved file to json")
            return google_token
        except:
            print(exit[0])