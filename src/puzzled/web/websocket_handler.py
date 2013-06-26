'''
Created on Jun 26, 2013

@author: peterb
'''
import logging
from tornado import websocket
from tornado.escape import json_encode
from tornado.web import create_signed_value


class WebSocketHandler(websocket.WebSocketHandler):
    
    def open(self):
        self.application.add_client(self)
        logging.info("WebSocket opened")
        

    def on_message(self, message):
        self.write_message(u"You said: " + message)


    def on_close(self):
        self.application.remove_client(self)
        logging.info("WebSocket closed")
        
        
    @property
    def cookie_name(self):
        return self.application.settings.get('cookie_name')
    
    
    def get_current_user(self):
        return self.get_secure_cookie(self.cookie_name)
    
        
    def set_current_user(self, accl_key):
        self.set_secure_cookie(self.cookie_name, accl_key)
        
        
    def get_accl_user_dict(self):
        try:
            if self.current_user:
                return self.application.get_accl_user(self.current_user)
        except Exception:
            self.clear_cookie(self.cookie_name)
        return 0
    
    
    def get_accl_user(self):
        return json_encode(self.get_accl_user_dict()) 
          
        
    def gen_login_cookie(self,value):
        return create_signed_value(self.application.settings["cookie_secret"],
                                   self.cookie_name, value)


    def handle_login(self, message):
        accl_key = self.application.login(message.get("email"), 
                                          message.get("password"))
        self._current_user = accl_key
        self.write_message({"result":self.get_accl_user_dict(), 
                            "cookie":self.gen_login_cookie(accl_key), 
                            "cookie_name":self.cookie_name, 
                            "request_id":message.get("request_id")})
        

    def handle_register(self, message):
        accl_key = self.application.register(message.get("email"), 
                                             message.get("password"))
        self._current_user = accl_key
        self.write_message({"result":self.get_accl_user_dict(), 
                            "cookie":self.gen_login_cookie(accl_key), 
                            "cookie_name":self.cookie_name, 
                            "request_id":message.get("request_id")})
        return accl_key

