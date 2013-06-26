'''
Created on Jun 26, 2013

@author: peterb
'''
import tornado.web


class Application(tornado.web.Application):
    
    def __init__(self, *args, **kwargs):
        tornado.web.Application.__init__(self, *args, **kwargs)
        self.clients = []
        
    
    def add_client(self, client):
        self.clients.append(client)
        
    
    def remove_client(self, client):
        self.clients.remove(client)