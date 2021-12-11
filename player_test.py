import unittest

import player


class PlayerTest (unittest.TestCase):
    # test_hash_password tests if the Player.hashPassword method hashes the password correctly.
    def test_hash_password(self):
        pl = player.Player()

        # The hash of this password is already known. So, can be used to verify the working.
        pl.password = "something-unhashed"
        expected_hash = "5153d7d83122027ef5c2d96baf665db692c23bc829e4f5d0820d26510f04b40c"

        # Calling the method to be tested.
        pl.hashPassword()

        # Checking if the actual hash matches the expected hash.
        self.assertEqual(pl.password, expected_hash)


if __name__ == '__main__':
    
    unittest.main()
