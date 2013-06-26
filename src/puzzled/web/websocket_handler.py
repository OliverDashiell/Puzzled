'''
Created on Jun 26, 2013

@author: peterb
'''
from tornado import websocket
import logging


class WebSocketHandler(websocket.WebSocketHandler):
    
    def open(self):
        self.application.add_client(self)
        logging.info("WebSocket opened")
        

    def on_message(self, message):
        self.write_message(u"You said: " + message)


    def on_close(self):
        self.application.remove_client(self)
        logging.info("WebSocket closed")