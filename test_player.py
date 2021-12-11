import unittest
import shelve
from player import Player



class Test_player(unittest.TestCase):
  def setUp(self):
    self.player = Player()
    
class TestInit(Test_player):
  def test_initial_score(self):
    self.assertEqual(self.player.score, 0) 
  def test_initial_stage(self):
    self.assertEqual(self.player.stage, 1) 
  def test_initial_username(self): #username exists
    db = shelve.open('playerdb')
    self.assertEqual(self.player.username in db, "test")
  def test_initial_name(self): #name exists
    self.assertEqual(self.player.name, "test")
  db.close()

if __name__ == '__main__':
    unittest.main()
   