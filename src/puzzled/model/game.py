'''
Created on 27 Jun 2013

@author: dash
'''
from puzzled.model.base import Base
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime


game_players_user = Table('game_players_user', Base.metadata,
                          Column('players_id', Integer, ForeignKey('game.id')),
                          Column('user_id', Integer, ForeignKey('user.id')),
                          mysql_engine='InnoDB')


class Game(Base):
    
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    created = Column(DateTime, default=datetime.datetime.now)
    started = Column(DateTime)
    ended = Column(DateTime)
    
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship('User', uselist=False,
                         primaryjoin='Game.owner_id==User.id', remote_side='User.id')
    
    
    players = relationship('User',
                           primaryjoin='Game.id==game_players_user.c.players_id',
                           secondaryjoin='User.id==game_players_user.c.user_id',
                           secondary='game_players_user',
                           lazy='joined')
    