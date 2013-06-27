'''
Created on Jun 27, 2013

@author: peterb
'''
import unittest
from puzzled.web.control import Control
from puzzled import model


class Test(unittest.TestCase):


    def setUp(self):
        self.control = Control()
        self.control.drop_all_and_create()


    def tearDown(self):
        self.control._dispose_()


    def testName(self):
        with self.control.db_session as session:
            game = model.Game(name="foo")
            fort = model.Feature(name="fort")
            f1 = model.GameFeature(game=game, feature=fort)
            session.add_all([game,fort,f1])
            session.commit()
            
            for game in session.query(model.Game):
                print game.name
                for f in game.features:
                    print f.all_properties


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()