import os
import unittest

from src.utils import data_reader, get_user_data, pearson_similarity


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

    def test_denominateur_zero(self):
        x = [1, 2, 3, 4, 5]
        y = [1, 1, 1, 1, 1]
        self.assertEqual(pearson_similarity(x, y), 0)


class TestData(unittest.TestCase):
    def setUp(self):
        self.dirname = os.path.split(os.path.abspath(__file__))[0]

    def test_data_reader(self):
        data = data_reader(f"{self.dirname}/dataset/test.xlsx")
        self.assertEqual(data.shape, (8, 1))

    def test_get_user_data(self):
        data = data_reader(f"{self.dirname}/dataset/test.xlsx")
        expected = [0, 4, 2, 1, 4, 0, 2, 1, 4, 3, 3, 2, 4, 1, 3, 1, 2, 0, 4, 1]
        self.assertEqual(get_user_data(data, 2), expected)


if __name__ == "__main__":
    unittest.main()
