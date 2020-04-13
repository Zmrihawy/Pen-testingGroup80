import web
from views.forms import register_form
import models.register
import models.user
from views.utils import get_nav_bar, csrf, csrf_decorate, generate_salt, hashed_value, generate_token
import os

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
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input()

        register = register_form()

        # check user is exites or not
        if not register.validates():
            return render.register(nav, register, "All fields must be valid.")

        # Check if user exists
        if models.user.get_user_id_by_name(data.username):
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
            google_token = None
            
            # send web mail
            # Send user email
            reset_url = "http://localhost/validate_account?reset_token=" + temp_token
            msg = "Please verfiy your account via this link.\n" + str(reset_url)
           
            #send mail (currently it is currpted)
            #self.send_mail(data.email, msg)

            # write into database
            models.register.set_user(data.username, password, data.full_name, data.company, data.email, data.street_address,
            data.city, data.state, data.postal_code, data.country, ip_addr, path, temp_account, google_token, temp_token)

            # msg for notification
            return render.register(nav, register_form, "User registered and verified with email!\n" + msg)
        except Exception :
            print(Exception)
        
        except:
            print(exit[0])
            return render.register(nav, register_form, "Fail to register!")

    def send_mail(self, mail, msg):
        smtp_server = "molde.idi.ntnu.no:25"
        web.config.smtp_server = smtp_server
        web.sendmail('beelance@ntnu.no', mail, 'Account verify from Beelance', msg)
        return