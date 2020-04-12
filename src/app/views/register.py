import web
from views.forms import register_form
import models.register
import models.user
from views.utils import get_nav_bar, csrf, csrf_decorate, generate_salt, hashed_value
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
            
            # write into database
            models.register.set_user(data.username, password, data.full_name, data.company, data.email, data.street_address,
            data.city, data.state, data.postal_code, data.country, ip_addr, path)
            return render.register(nav, register_form, "User registered!")
        except:
            print(exit[0])
            return render.register(nav, register_form, "Fail to register!")
        #finally:
            #return render.register(nav, register_form, "Activity Recorded.")
