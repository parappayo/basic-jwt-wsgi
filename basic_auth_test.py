import unittest, basic_auth


class TestBasicAuth(unittest.TestCase):

    def test_decode(self):
        username, password = basic_auth.decode('dXNlcjpwYXNz')
        self.assertEqual(username, 'user')
        self.assertEqual(password, 'pass')


if __name__ == '__main__':
    unittest.main()
