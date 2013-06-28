'''
Created on Jun 27, 2013

@author: peterb
'''
from puzzled.model.base import Base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer
from sqlalchemy.orm import relationship


class GameFeature(Base):
    
    id = Column(Integer, primary_key=True)
    map_x = Column(Integer)
    map_y = Column(Integer)
    feature_id = Column(Integer, ForeignKey('feature.id'))
    feature = relationship('Feature', uselist=False,
                           primaryjoin='GameFeature.feature_id==Feature.id', remote_side='Feature.id')
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship('Game', uselist=False,
                        primaryjoin='GameFeature.game_id==Game.id', remote_side='Game.id',
                        back_populates='features')


    properties = relationship('GameFeatureProperty', uselist=True, 
                              primaryjoin='GameFeatureProperty.game_feature_id==GameFeature.id', 
                              remote_side='GameFeatureProperty.game_feature_id',
                              back_populates='game_feature')
    
    def as_dict(self):
        result = {}
        for p in self.feature.properties:
            result[p.name]=p.value
        for p in self.properties:
            result[p.name]=p.value
        result['id'] = self.id
        result['x'] = self.map_x
        result['y'] = self.map_y
        result['name'] = self.feature.name
        result['url'] = self.feature.url
        return result
    
    
    def set_properties(self, new_properties):
        from puzzled.model.game_feature_property import GameFeatureProperty
        
        # remove properties that are in feature properties
        fproperties = dict([(p.name,p.value) for p in self.feature.properties])
        for key,value in new_properties.items():
            if fproperties.has_key(key) and fproperties[key] == value:
                del new_properties[key]
        
        properties = dict([(p.name,p) for p in self.properties])
        for key,value in new_properties.iteritems():
            if properties.has_key(key):
                properties[key].value = value
            else:
                self.properties.append(GameFeatureProperty(name=key,value=value))
