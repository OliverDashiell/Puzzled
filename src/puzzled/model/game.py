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
    
    features = relationship('GameFeature', uselist=True, 
                            primaryjoin='GameFeature.game_id==Game.id', 
                            remote_side='GameFeature.game_id',
                            back_populates='game')
    
    properties = relationship('GameProperty', uselist=True, 
                              primaryjoin='GameProperty.game_id==Game.id', 
                              remote_side='GameProperty.game_id',
                              back_populates='game')
    
    def as_dict(self):
        result = {}
        for p in self.properties:
            result[p.name]=p.value
        result['id'] = self.id
        result['name'] = self.name
        result['features'] = [feature.as_dict() for feature in self.features]
        return result
    
    def set_properties(self, new_properties):
        from puzzled.model.game_property import GameProperty
        
        properties = dict([(p.name,p) for p in self.properties])
        for key,value in new_properties.iteritems():
            if properties.has_key(key):
                properties[key].value = value
            else:
                self.properties.append(GameProperty(name=key,value=value))
    
    