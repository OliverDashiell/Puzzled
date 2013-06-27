'''
Created on Jun 26, 2013

@author: peterb
'''
import logging
import time
from tornado import websocket
from tornado.escape import json_encode, json_decode
from tornado.web import create_signed_value


class WebSocketHandler(websocket.WebSocketHandler):
    
    def open(self):
        self.application.add_client(self)
        logging.info("WebSocket opened")
        if self.current_user:
            message = {
                "result": self.application.get_accl_user(self.current_user),
                "request_id": -1
            }
            self.write_message(message)
        

    def on_message(self, raw_message):
        start = time.time()
        message = json_decode(raw_message)    
        action = message.get("action")
        args = message.get("args")
        
        try:
            if action == "login":
                self.handle_login(message)
            elif action == "register":
                self.handle_register(message)
            else:
                method = getattr(self.application, action)
                result = method(**args)
                self.write_message({"result": result,
                                    "request_id": message.get("request_id")})
        except Exception, ex:
            logging.exception(message)
            self.write_message({"error": str(ex),
                                "request_id": message.get("request_id")})
            
        logging.info("200 WS %s %.05fms" % (action,(time.time() - start)/1000))



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

