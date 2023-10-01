import unittest

from service.app.auth.auth_utils import generate_hash


class MyTestCase(unittest.TestCase):

    def test_generate_hash(self):
        password = "my_password"
        expected_hash = "$2a$12$cWyEuES9LXSO4/JD9nzN2O.7NtuWcIUv7IKoHh9LpkjTyjzhyp.pG"
        hashed_password = generate_hash(password)
        self.assertEqual(expected_hash, hashed_password)
