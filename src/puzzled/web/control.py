'''
Created on Jun 27, 2013

@author: peterb
'''
import logging
from tornado.options import define, options
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from puzzled import model

define("db_url", "sqlite://", help="default database url")


class GameAlreadyRunning(Exception):
    def __init__(self, message="Game already running!"):
        Exception.__init__(self, message)
        
        
class GameNotFound(Exception):
    def __init__(self, message="Game not found!"):
        Exception.__init__(self, message)
        

class FeatureNotFound(Exception):
    def __init__(self, message="Feature not found!"):
        Exception.__init__(self, message)
        

class Control(object):
    
    def __init__(self):
        self._engine_ = create_engine(options.db_url, echo=False)
        self._Session_ = sessionmaker(bind=self._engine_)
        self.games = []
        
        
    def _dispose_(self):
        ''' 
            tidy up we've gone away
        '''
        if self._engine_:
            self._engine_.dispose()
        self._Session_ = self._engine_ = None
        logging.debug("control disposed")


    def _init_db_(self, session):
        session.add(model.User("admin@test.com","admin"))
        session.commit()
        
        
    def drop_all_and_create(self):
        with self.db_session as session:
            model.base.drop_all(session)
            model.base.create_all(self._engine_)
            self._init_db_(session)
        

    @property
    def db_session(self):
        ''' 
            returns a self closing session for use by with statements 
        '''
        session = self._Session_()
        class closing_session:
            def __enter__(self):
                logging.debug("db session open")
                return session
            def __exit__(self, type, value, traceback):
                logging.debug("db session closed")
                session.close()
        return closing_session()
    
    
    def start_game(self, gameId):
        ''' 
            starts a game and adds it to the server game list 
        '''
        game = self._running_game_(gameId)
        if game:
            raise GameAlreadyRunning()
        with self.db_session as session:
            game = session.query(model.Game).get(gameId)
            game_dict = game.as_dict()
            game_dict["_moves_"] = []
            self.games.append(game_dict)
            return game_dict
        
        
    def end_game(self, gameId):
        ''' 
            ends a game and removes it from the server game list 
        '''
        game = self._get_running_game_(gameId)
        self.games.remove(game)
        return game
        
        
    def change_feature(self, gameId, featureId, propertyName, newValue):
        ''' 
            add value to pending moves in game 
        '''
        game = self._get_running_game_(gameId)
        game["_moves_"].append((featureId, propertyName, newValue))
        
        
    def end_turn(self, gameId):
        ''' 
            resolve move conflicts 
        '''
        game = self._get_running_game_(gameId)
        for move in game.get("_moves_"):
            self._change_feature_(game, *move)
        game['_moves_'] = []
        
        
    def _change_feature_(self, game, featureId, propertyName, newValue):
        feature_set = False
        for feature in game.get("features"):
            if feature.get("id") == featureId:
                feature[propertyName] = newValue
                feature_set = True
                
        if feature_set == False:
            raise FeatureNotFound()

    
    def _get_running_game_(self, gameId):
        game = self._running_game_(gameId)
        if game is None:
            raise GameNotFound("Game offline or does not exist")
        return game
        
    def _running_game_(self, gameId):
        for g in self.games:
            if g.get("id") == gameId:
                return g
        
        