import web, json, os
from views.forms import two_fa_form
from views.utils import get_nav_bar, csrf, csrf_decorate, hashed_value, generate_salt
from models.google_auth import search_for_token, get_totp_token
from models.validate_account import update_token_to_null, search_for_token

# Get html templates
render = web.template.render('templates/')

# Set global token
web.template.Template.globals['csrf_token'] = csrf

class Two_FA():
    
    def GET(self):
        """
        Get the rest_password form

            :return: A page with the Change_password form
        """
        session = web.ctx.session
        nav = get_nav_bar(session)

         # get access information
        ip_addr = web.ctx["ip"]
        path = web.ctx["fullpath"]
        session.ip = ip_addr
        session.header = web.ctx.env['HTTP_USER_AGENT']

        # get toke via url
        data = web.input()
        token = data.reset_token

        #TODO search for token and return username
        username = search_for_token(token, ip_addr, path)

        #TODO verify the account and clear the token of the account
        #result = update_token_to_null(username, ip_addr, path)
        #print(result)
         # show validate account message and redirect to home page
        try:
            if session.ip == web.ctx["ip"] and session.header == web.ctx.env['HTTP_USER_AGENT']\
                and username:
                current_dir = os.getcwd()
                print("=="*8 + "\n" + current_dir)
                return render.two_fa(nav, two_fa_form, "static/picture.png", "Not validate!")
        except:
            print(exit[0])
            return web.seeother("/")

    @csrf_decorate
    def POST(self):
        """
        Handle input data and change password in database

            :return: Main page
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input(token="")
        
        two_fa = two_fa_form()
        
        # check each field is endered values.
        if not two_fa.validates():
            return render.two_fa(nav, two_fa_form, "All fields must be valid.")
        
        try:
            # log ip information
            ip_addr = web.ctx["ip"]
            accessed_path = web.ctx["fullpath"]

            # query user's name (username) and token (extra secruity)
            token = data.reset_token
            username = search_for_token(token, ip_addr, accessed_path)
            #print("-"*16)
            #print(username)
            rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname("token_img")))
            with open(os.path.join(rel, 'secrets.json'), 'r') as opened_file:
                secrets = json.load(opened_file)
            
            for label, key in sorted(list(secrets.items())):
                print("===" * 8 +"\n"+ data.token)
                print(get_totp_token(key), type(get_totp_token(key)))
                if data.token == get_totp_token(key):
                    result = update_token_to_null(label, ip_addr, accessed_path)
                    raise web.seeother("/login")
                print("{}:\t{}".format(label, get_totp_token(key)))
            
            session.ip = None
            session.header = None

            
        except Exception as e:
            print(e)
        except:
            print(exit[0])
            return render.login(nav, two_fa_form, "- Something went wrong!")