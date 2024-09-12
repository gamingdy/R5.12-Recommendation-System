import unittest

from src.utils import pearson_similarity


class TestPearson(unittest.TestCase):
    def tests_taille_different(self):
        with self.assertRaises(ValueError):
            pearson_similarity([1, 2, 3], [1, 2, 3, 4])

    def test_similarity(self):
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 3, 4, 5]
        self.assertEqual(pearson_similarity(x, y), 1)

    def test_similarity_2(self):
        x = [8, 13, 2, 37, 71, 13, 16, 26, 96, 54]
        y = [87, 73, 98, 20, 70, 64, 9, 82, 66, 24]
        self.assertAlmostEqual(pearson_similarity(x, y), -0.1915, places=4)


if __name__ == "__main__":
    unittest.main()
