'''
Created on Jun 27, 2013

@author: peterb
'''
from puzzled.model.base import Base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship



class Feature(Base):
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    url = Column(String(255))

    properties = relationship('FeatureProperty', uselist=True, 
                              primaryjoin='FeatureProperty.feature_id==Feature.id', remote_side='FeatureProperty.feature_id',
                              back_populates='feature')