'''
Created on Jun 27, 2013

@author: peterb
'''

from tornado.web import create_signed_value
from tornado.escape import json_encode


class UserMixin(object):

    @property
    def cookie_name(self):
        return self.application.settings.get('cookie_name')
    
    
    def get_current_user(self):
        return self.get_secure_cookie(self.cookie_name)
                        
        
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