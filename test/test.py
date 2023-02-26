import unittest

class PlaceholderTest(unittest.TestCase):

    def placeholder(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()