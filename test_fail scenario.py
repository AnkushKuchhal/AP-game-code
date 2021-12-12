import unittest
import shelve
from player import Player



class Test_player(unittest.TestCase):
  def setUp(self):
    self.player = Player(3, "test", "test1", "test")
    self.player.score = 100
    self.player.stage = 1
    
class TestInit(Test_player):
  def test_initial_score(self):
    self.assertEqual(self.player.score, 1000)

  def test_initial_stage(self):
    self.assertEqual(self.player.stage, 2) 

  def test_initial_username(self): #username exists
    db = shelve.open('playerdb')
    #if self.player.username in db:
    self.assertEqual(self.player.username, "test1")
    db.close()
    
  def test_initial_name(self): #name exists
    db = shelve.open('playerdb')
    self.assertEqual(self.player.name, "test1")
    db.close()
  
  def test_highscore(self):
    db = shelve.open('playerdb')
    if self.player.username in db:
      self.assertEqual(self.player.highscore, 30)
    db.close()


  def test_auth(self):
    db = shelve.open('playerdb')
    if self.player.username in db:
      password = db[self.player.username].password #type: ignore
      self.player.hashPassword()
      self.assertEqual(self.player.authenticatePlayer(), True)
    else: raise ValueError('Username not found')
    db.close()

if __name__ == '__main__':
    unittest.main()
