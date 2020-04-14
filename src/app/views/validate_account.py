import web
from views.utils import get_nav_bar, csrf, csrf_decorate
from models.validate_account import search_for_token, update_token_to_null
from models.logger import log_error_msg
import time
## NOT IN USE
# Get html templates
render = web.template.render('templates/')

# Set global token
web.template.Template.globals['csrf_token'] = csrf

class Validate_account():

    def GET(self):
        """
        Get the Validate_account form

            :return: A page with the Validate_account form
        """

        session = web.ctx.session
        nav = get_nav_bar(session)
        try:

            # get access information
            ip_addr = web.ctx["ip"]
            path = web.ctx["fullpath"]
            session.ip = ip_addr
            session.header = web.ctx.env['HTTP_USER_AGENT']

            # get toke via url
            data = web.input()
            token = data.reset_token

            print(token)
            #TODO search for token and return username
            username = search_for_token(token, ip_addr, path)

            print(username)
            #TODO verify the account and clear the token of the account
            #result = update_token_to_null(username, ip_addr, path)
            #print(result)
            # show validate account message and redirect to home page
            render.validate_account(nav, "Your acount: {} has been verified!".format(username))
            
            raise web.seeother("/two_fa")

        except Exception as e:
            print(e)
        except:
            render.validate_account(nav, "An internal error occur")