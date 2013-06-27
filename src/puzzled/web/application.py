'''
Created on Jun 26, 2013

@author: peterb
'''
import logging
import tornado.web
from tornado.options import define, options
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from puzzled import model
from sqlalchemy.sql.expression import and_
from puzzled.web.control import Control




class Application(Control, tornado.web.Application):
    
    def __init__(self, *args, **kwargs):
        tornado.web.Application.__init__(self, *args, **kwargs)
        Control.__init__(self)
        self.clients = []
        
            
    def add_client(self, client):
        self.client_authenticated(client)
        self.clients.append(client)
        
    
    def remove_client(self, client):
        self.clients.remove(client)
    
    
    def client_authenticated(self, client):
        #TODO logout client with duplicate client id
        client_id = client.current_user
        if client_id:
            for other_client in self.clients:
                if other_client is not client and other_client.current_user == client_id:
                    other_client.send_close()


    def get_accl_user(self, id):
        with self.db_session as session:
            user = session.query(model.User).get(id)
            return user.accl_dict()


    def login(self, email, password):
        with self.db_session as session:
            user = session.query(model.User).filter(and_(model.User.email==email,
                                                         model.User.password==model.User.salt_n_hash(password))).first()
            if user is None:
                raise Exception("Email or password incorrect!")
            session.commit()
            return str(user.id)
    
    
    def register(self, email, password):
        with self.db_session as session:
            user = model.User(email=email, password=password,
                              name=model.User.email_to_name(email))
            session.add(user)
            session.commit()
            logging.debug("registered %s", email)
            return str(user.id) 
        
        
    def echo(self, message):
        return message
    
    
    def chat(self, from_user_id, from_user, message):
        logging.info((from_user_id, from_user, message))
        chat_message = {"from_user": from_user, "message": message}
        for client in self.clients:
            if client.current_user != from_user_id:
                client.broadcast("chat", chat_message)
    
    
    def users(self):
        result = {}
        for client in self.clients:
            user = client.current_user
            if user:
                result[user]=(self.get_accl_user(user))
        return result.values()
    
        