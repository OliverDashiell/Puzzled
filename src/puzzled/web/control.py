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

class Control(object):
    
    def __init__(self):
        self._engine_ = create_engine(options.db_url, echo=False)
        self._Session_ = sessionmaker(bind=self._engine_)
        
        
    def _dispose_(self):
        ''' 
            tidy up we've gone away
        '''
        if self._engine_:
            self._engine_.dispose()
        self._Session_ = self._engine_ = None
        logging.debug("control disposed")
        
        
    def drop_all_and_create(self):
        with self.db_session as session:
            model.base.drop_all(session)
            model.base.create_all(self._engine_)
            self._init_db_(session)


    def _init_db_(self, session):
        session.add(model.User("admin@test.com","admin"))
        session.commit()
        

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