'''
Created on Jun 3, 2013

@author: peterb
'''
import hashlib
from sqlalchemy.types import String, Integer
from sqlalchemy.schema import Column
from sqlalchemy.orm import deferred
from sqlalchemy.ext.hybrid import hybrid_property
from puzzled.model.base import Base


class User(Base):
    
    id = Column(Integer, primary_key=True)
    email = Column(String(80), unique=True, nullable=False)
    name = Column(String(80))
    _password = deferred(Column("password",String(40), nullable=False))    

    def __init__(self, email, password, name=None):
        ''' only used at creation'''
        self.email = email
        self.password = password
        self.name = name if name else self.email_to_name(email)


    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = self.salt_n_hash(value)
        
    @password.expression
    def password(self):
        return self._password
    
    def favorite_keys(self):
        return []
    
    def entitlement_keys(self):
        return []
    
    @classmethod
    def salt_n_hash(cls, value):
        return hashlib.sha1(value).hexdigest()
    
    @classmethod
    def email_to_name(cls, email):
        name, domain = email.split("@")
        return name.replace("."," ")
    
    
    def accl_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

    