from binascii import hexlify, unhexlify
from hashlib import pbkdf2_hmac
import os
import web
import random, string

SHA = 'sha256'
SHA_VALUE = 100000

def get_nav_bar(session):
    """
    Generates the page nav bar

        :return: The navigation bar HTML markup
    """
    result = '<nav>'
    result += ' <ul>'
    result += '    <li><h1 id="title">Beelance2</h1></li>'
    result += '    <li><a href="/">Home</a></li>'
    if session.username:
        result += '    <li><a href="logout">Logout</a></li>'
        result += '    <li><a href="new_project">New</a></li>'
    else:
        result += '    <li><a href="register">Register</a></li>'
        result += '    <li><a href="login">Login</a></li>'
    result += '    <li><a href="open_projects">Projects</a></li>'
    result += ' </ul>'
    result += '</nav>'
    return result
           
def get_element_count(data, element):
    """
    Determine the number of tasks created by removing 
    the four other elements from count and divide by the 
    number of variables in one task.
     
        :param data: The data object from web.input
        :return: The number of tasks opened by the client
    """
    task_count = 0
    while True:
        try:
            data[element+str(task_count)]
            task_count += 1
        except:
            break
    return task_count

def csrf():
    session = web.ctx.session
    if not session.has_key('csrf_token'):
        from uuid import uuid4
        session.csrf_token = uuid4().hex
    return session.csrf_token

def csrf_decorate(f):
    def csrf_base(*a, **k):
        session = web.ctx.session
        input = web.input()
        if not (session.has_key('csrf_token') and input.csrf_token == session.pop('csrf_token', None)):
            raise web.HTTPError("400 Bad request", {'content-type':'text/html'}, 'Request forgery!')
        return f(*a,**k)
    return csrf_base