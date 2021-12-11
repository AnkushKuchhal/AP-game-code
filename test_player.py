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
    if self.player.username in db:
      self.assertEqual(self.player.username, "test")
      db.close()
    
  def test_initial_name(self): #name exists
    db = shelve.open('playerdb')
    if self.player.name == "test" in db:
      self.assertEqual(self.player.name, "test")
    db.close()
  
  def test_highscore(self):
    db = shelve.open('playerdb')
    if self.player.username == "test" in db:
      self.assertEqual(self.player.highscore, 3)
      print (self.player.highscore)
    db.close()

if __name__ == '__main__':
    unittest.main()
   