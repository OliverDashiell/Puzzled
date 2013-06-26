'''
Created on Jun 26, 2013

@author: peterb
'''
import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("index.html")
