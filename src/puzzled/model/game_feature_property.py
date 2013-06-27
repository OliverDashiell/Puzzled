'''
Created on Jun 27, 2013

@author: peterb
'''
from puzzled.model.base import Base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship


class GameFeatureProperty(Base):
    
    id = Column(Integer, primary_key=True)
    game_feature_id = Column(Integer, ForeignKey('game_feature.id'))
    game_feature = relationship('GameFeature', uselist=False,
                                primaryjoin='GameFeatureProperty.game_feature_id==GameFeature.id', 
                                remote_side='GameFeature.id',
                                back_populates='properties')
    name = Column(String(255))
    value = Column(String(255))