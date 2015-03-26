'''
Created on Jun 27, 2013

@author: peterb
'''
import unittest #@UnresolvedImport
import json #@UnresolvedImport
from puzzled.web.control import Control, GameAlreadyRunning
from puzzled import model


class Test(unittest.TestCase):


    def setUp(self):
        self.control = Control()
        self.control.drop_all_and_create()


    def tearDown(self):
        self.control._dispose_()
            
            
    def testMap(self):
        with self.control.db_session as session:
            admin = session.query(model.User).get(1)
            
            game = model.Game(name="NewWorld",owner=admin)
            game.set_properties({"width":100,"height":100})
            game.players.append(admin)
            
            brt = model.Feature(name="brt", url="image:/assets/brt16x16.png")
            tree = model.Feature(name="tree", url="sprite:/assets/16x16_forest_2.gif:0:0")
            
            session.add_all([game,tree])
            
            game.add_feature(tree,{"loc":(0,0)})
            game.add_feature(tree,{"loc":(0,16)})
            unit1 = game.add_feature(brt,{"loc":(50,50)},admin)
            
            session.commit()
            
            self.control.start_game(1)
            self.control.change_feature(1, unit1.id, "loc", (51,51))
            print json.dumps(self.control.games[0],indent=4)
            self.control.end_turn(1)
            print json.dumps(self.control.games[0],indent=4)
            
            try:
                self.control.start_game(1)
                raise Exception("Should fail")
            except GameAlreadyRunning:
                pass
            
            self.control.end_game(1)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()