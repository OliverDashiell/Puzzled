'''
Created on Jun 27, 2013

@author: peterb
'''
from puzzled.model.base import Base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship



class FeatureProperty(Base):
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    value = Column(String(255))
    feature_id = Column(Integer, ForeignKey('feature.id'))
    feature = relationship('Feature', uselist=False,
                           primaryjoin='FeatureProperty.feature_id==Feature.id', remote_side='Feature.id',
                           back_populates='properties')