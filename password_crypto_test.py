import unittest, password_crypto


class TestPasswordCrypto(unittest.TestCase):

    def test_encode_and_validate(self):
        password = 'pass'
        password_salt, password_hash = password_crypto.encode(password)
        self.assertTrue(len(password_salt) > 0)
        self.assertTrue(len(password_hash) > 0)

        result = password_crypto.validate(password, password_salt, password_hash)
        self.assertTrue(result)

        result = password_crypto.validate(password, b'', b'')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
