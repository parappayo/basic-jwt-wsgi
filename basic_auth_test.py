import unittest, basic_auth


class TestBasicAuth(unittest.TestCase):

    def test_decode(self):
        username, password = basic_auth.decode('dXNlcjpwYXNz')
        self.assertEqual(username, 'user')
        self.assertEqual(password, 'pass')


    def test_decode_header(self):
        username, password = basic_auth.decode_header('Basic dXNlcjpwYXNz')
        self.assertEqual(username, 'user')
        self.assertEqual(password, 'pass')

        username, password = basic_auth.decode_header('blah')
        self.assertEqual(username, False)
        self.assertEqual(password, False)


if __name__ == '__main__':
    unittest.main()
