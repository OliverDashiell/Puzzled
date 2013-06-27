'''
Created on Jun 26, 2013

@author: peterb
'''
import tornado.web
from puzzled.web.user_mixin import UserMixin


class IndexHandler(UserMixin, tornado.web.RequestHandler):
    
    def get(self):
        self.render("index.html")
