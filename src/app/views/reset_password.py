import web
from views.forms import reset_password_form
from models.reset_password import search_for_user, update_token_to_null
from views.utils import get_nav_bar, csrf, csrf_decorate, hashed_value, generate_salt
from models.user import update_user_password

# Get html templates
render = web.template.render('templates/')

# Set global token
web.template.Template.globals['csrf_token'] = csrf

class Reset_password():
    
    def GET(self):
        """
        Get the rest_password form

            :return: A page with the Change_password form
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        self.token = web.input().reset_token
        return render.reset_password(nav, reset_password_form, "")

    @csrf_decorate
    def POST(self):
        """
        Handle input data and change password in database

            :return: Main page
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input(reset_token = "", new_password="")
        
        reset_password_colum = reset_password_form()
        
        # check each field is endered values.
        if not reset_password_colum.validates():
            return render.reset_password(nav, reset_password_form, "All fields must be valid.")
        
        try:
            # log ip information
            ip_addr = web.ctx["ip"]
            accessed_path = web.ctx["fullpath"]

            # query user's name (username) and token (extra secruity)
            token = data.reset_token
            username = search_for_user(token, ip_addr, accessed_path)
            #print("-"*16)
            #print(username)
           
            #update token to null database
            result_update_token = update_token_to_null(username, token, ip_addr, accessed_path)
            print("-" * 16 + "updated!")

            # generate new password
            new_salt = generate_salt()
            hashed_password = hashed_value(data.new_password, new_salt)
            hashed_password = new_salt + hashed_password

            # update password 
            result_update_password = update_user_password(username, hashed_password, ip_addr, accessed_path )
            raise web.seeother("/")
        except Exception as e:
            print(e)
        except:
            print(exit[0])
            return render.login(nav, reset_password_form, "- Something went wrong!")