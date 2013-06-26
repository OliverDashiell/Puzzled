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


define("db_url", "sqlite://", help="default database url")


class Application(tornado.web.Application):
    
    def __init__(self, *args, **kwargs):
        tornado.web.Application.__init__(self, *args, **kwargs)
        self.clients = []
        self._engine_ = create_engine(options.db_url, echo=False)
        self._Session_ = sessionmaker(bind=self._engine_)
        
            
    def add_client(self, client):
        self.clients.append(client)
        
    
    def remove_client(self, client):
        self.clients.remove(client)
    
    
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


    def get_accl_user(self, id):
        with self.db_session as session:
            user = session.query(model.User).get(id)
            return user.accl_dict()


    def login(self, email, password):
        with self.session as session:
            user = session.query(model.User).filter(and_(model.User.email==email,
                                                         model.User.password==model.User.salt_n_hash(password))).first()
            if user is None:
                raise Exception("Email or password incorrect!")
            session.commit()
            return str(user.id)
    
    
    def register(self, email, password):
        with self.session as session:
            user = model.User(email=email, password=password,
                              name=model.User.email_to_name(email))
            session.add(user)
            session.commit()
            logging.debug("registered %s", email)
            return str(user.id) 
        