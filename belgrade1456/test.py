import unittest
from main import bullet

class testBullet(unittest.TestCase):
    b = bullet(10,10)
    def test_init(self, bTest = b):
        self.assertEqual(bTest.getX(),10)

    def test_hit(self, bTest = b):
        self.assertTrue(bTest.checkCollision(10, 10))

if __name__ == '__main__':
    unittest.main()
