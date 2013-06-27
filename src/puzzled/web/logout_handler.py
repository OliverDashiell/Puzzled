'''
Created on Apr 4, 2013

@author: peterb
'''
import tornado.web
from puzzled.web.user_mixin import UserMixin

class LogoutHandler(UserMixin, tornado.web.RequestHandler):
        
    def get(self):
        self.clear_cookie(self.cookie_name)
        self.redirect("/")