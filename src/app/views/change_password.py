import web
from views.forms import change_password_form
import models.user
from views.utils import get_nav_bar, csrf, csrf_decorate, hashed_value, generate_salt
import os, datetime, time

# Get html templates
render = web.template.render('templates/')

# Set global token
web.template.Template.globals['csrf_token'] = csrf

class Change_password():

    def GET(self):
        """
        Get the Change_password form

            :return: A page with the Change_password form
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        return render.change_password(nav, change_password_form, "")

    @csrf_decorate
    def POST(self):
        """
        Handle input data and change password in database

            :return: Main page
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input(old_password="", new_password="", comfirm_new_password="")

        change_password = change_password_form()

        # get current time
        current_time = time.time()

        # check each field is endered values.
        if not change_password.validates():
            return render.change_password(nav, change_password, "All fields must be valid.")
        
        try:
            # log ip information
            ip_addr = web.ctx["ip"]
            accessed_path = web.ctx["fullpath"]

            #get user's salt and password with attempt try
            log_time_date = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
            
            # return old password in database
            stored_password = models.user.get_user_hashed_password(session.username, ip_addr, accessed_path)

            #check data password exits
            if data.comfirm_new_password:
                # match with database
                # get salt value, type<str>
                salt = stored_password[:64]

                # password from database, type <str>
                password = stored_password[64:]

                # old password to validate is right or not
                hashed_old_password = hashed_value(data.old_password, salt)

                if password == hashed_old_password and data.new_password == data.comfirm_new_password:
                    # get new slat value
                    new_salt = generate_salt()
                    
                    hashed_new_password = hashed_value(data.comfirm_new_password, new_salt)
                    new_password = (new_salt + hashed_new_password)
                    #update new hased value to database
                    #print(hashed_new_password, session.username)
                    models.user.update_user_password(session.username, new_password, ip_addr, accessed_path)
                    #print("updated password!")
                    # after update, return to index
                    raise web.seeother("/")
                # validate value for password
                elif password != data.hashed_old_password:
                    return render.login(nav, change_password_form, "- Please check old password again!")
                # check the new password is same or not             
                elif data.old_password == data.new_password:
                    return render.login(nav, change_password_form, "- Same password")
                # other sictuation
                else:
                    return render.login(nav, change_password_form, "- The new password and comfirm new password are not match!")
            else:
                return render.login(nav, change_password_form, "- Please provide password")
            
            #password_hash = hashlib.md5(b'TDT4237' + data.password.encode('utf-8')).hexdigest()
            
        except:
            return render.login(nav, change_password_form, "- Something went wrong!")