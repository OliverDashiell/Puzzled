'''
Created on 28 Jun 2013

@author: dash
'''
from puzzled.model.base import Base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, PickleType
from sqlalchemy.orm import relationship


class GameProperty(Base):
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    value = Column(PickleType)
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship('Game', uselist=False,
                        primaryjoin='GameProperty.game_id==Game.id', 
                        remote_side='Game.id',
                        back_populates='properties')
