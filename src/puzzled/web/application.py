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
    
    def _init_db_(self, session):
        Control._init_db_(self, session)
        game = model.Game(name="foo")
        game.set_properties({"width":100,"height":100})
        fort = model.Feature(name="fort")
        fort.set_properties({'label':'bar'})
        f1 = model.GameFeature(game=game, feature=fort)
        f1.set_properties({"label":'knox'})
        session.add_all([game])
        session.commit()
            
            
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
        
    
    def broadcast(self, signal, message, userIds=None):
        for client in self.clients:
            if userIds is not None or client.current_user in userIds:
                client.broadcast(signal,message)
    
    
    def chat(self, from_user_id, from_user, message):
        logging.info((from_user_id, from_user, message))
        chat_message = {"from_user": from_user, "message": message}
        userIds = [client.current_user for client in self.clients if client.current_user not in [None,from_user_id]]
        self.broadcast("chat", chat_message, userIds)
    
    
    def users(self):
        result = {}
        for client in self.clients:
            user = client.current_user
            if user:
                result[user]=(self.get_accl_user(user))
        return result.values()
    
    
    def get_game(self, gameId):
        with self.db_session as session:
            game = session.query(model.Game).get(gameId)
            return game.as_dict()
        
        
    def start_game(self, gameId):
        game = Control.start_game(self, gameId)
        players = game.get("players") 
        self.broadcast("game_started", {"id": gameId}, players)
        
        
    def end_game(self, gameId):
        game = Control.start_game(self, gameId)
        players = game.get("players") 
        self.broadcast("game_ended", {"id": gameId}, players)
        
        