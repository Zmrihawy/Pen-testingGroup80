import web
from views.forms import forget_password_form
from models.password_forget import forget_password_match, update_reset_token
from views.utils import get_nav_bar, csrf, csrf_decorate, hashed_value, generate_salt, generate_token

# Get html templates
render = web.template.render('templates/')

# Set global token
web.template.Template.globals['csrf_token'] = csrf

class Forget_password():

    def GET(self):
        """
        Get the Change_password form

            :return: A page with the Change_password form
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        return render.forget_password(nav, forget_password_form, "")

    @csrf_decorate
    def POST(self):
        """
        Handle input data and change password in database

            :return: Main page
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input(username="", email="")

        forget_password = forget_password_form()
        #print("-"*16)
        #print("enter forget password")
        # check each field is endered values.
        if not forget_password.validates():
            return render.forget_password(nav, forget_password, "All fields must be valid.")
        
        try:
            # log ip information
            ip_addr = web.ctx["ip"]
            accessed_path = web.ctx["fullpath"]

            # query user's email and google token (extra secruity)
            user_email = forget_password_match(data.username, data.email, ip_addr,accessed_path)
            #print("-"*16)
            #print(user_email)
            # generate token
            user_reset_token = generate_token()

            #save token to database
            update_reset_token(data.username, user_reset_token, ip_addr, accessed_path)
            #print("-" * 8 + "updated!")
            
            # Send user email
            reset_url = "http://localhost/reset_password?reset_token=" + user_reset_token
            msg = "Please reset your password via this link.\n" + str(reset_url)

            #send mail
            #self.send_mail(user_email, msg)
            return render.forget_password(nav, forget_password_form, "- Send to mail" + msg)

        except Exception as e:
            print(e)
            return render.forget_password(nav, forget_password_form, "- Something went wrong!")
    
    def send_mail(self, mail, msg):
        smtp_server = "molde.idi.ntnu.no:25"
        web.config.smtp_server = smtp_server
        web.sendmail('beelance@ntnu.no', mail, 'Account verify from Beelance', msg)
        return