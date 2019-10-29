import web
from forms import login_form, register_form, guestbook_form
import model
from utils import get_nav_bar
from guestbook import Guestbook
from login import Login
from logout import Logout
from register import Register

# Define application routes
urls = (
    '/', 'Index',
    '/login', 'Login',
    '/logout', 'Logout',
    '/register', 'Register',
    '/guestbook', 'Guestbook',
)
                              
# Initialize application using the web py framework
app = web.application(urls, globals())

# Get html templates
render = web.template.render('templates/')

# Workaround to use sessions with reloader (debugger) http://webpy.org/cookbook/session_with_reloader
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={"username": None})
    web.config._session = session
else:
    session = web.config._session

# Add session to global variables
render._add_global(session, 'session')

def session_hook():
    web.ctx.session = session
    web.template.Template.globals['session'] = session

app.add_processor(web.loadhook(session_hook))

class Index:
    
    # Get main page
    def GET(self):
        nav = get_nav_bar(session)
        return render.index(nav)

class Admin:

    def GET(self):
        session = web.ctx.session
