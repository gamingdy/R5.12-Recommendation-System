import os
import unittest

from src.utils import data_reader, efficacite2, efficacite_simple, get_liste_utilisateur, get_user_data, pearson_similarity,prediction, prediction_cosine, remplir_total_pearson,efficacite


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


class TestPrediction(unittest.TestCase):
    def setUp(self):
        self.dirname = os.path.split(os.path.abspath(__file__))[0]
        self.data = data_reader(f"{self.dirname}/dataset/test2.xlsx")
        self.data2 = data_reader(f"{self.dirname}/dataset/test.xlsx")
        self.data3 = data_reader(f"{self.dirname}/dataset/toy_incomplet.xlsx")
        self.data4=data_reader(f"{self.dirname}/dataset/toy_complet.xlsx")
    """
    def test_remplir_total_p(self):
        used_data = self.data3
        remplir_total_pearson(used_data)
        self.assertEqual(1, 1)

    def test_prediction_values(self):
        used_data = self.data3
        u = get_user_data(used_data, 0)
        match_ = [(0, 1), (1, 2), (3, 5), (4, 4), (6, 0), (7, 2), (10, 3)]
        result = []
        for note in match_:
            item = note[0]
            liste=get_liste_utilisateur(used_data,item)
            result.append(prediction(u,item,liste))
        
        for k,v in enumerate(result):
            print(match_[k][1], v)
    """
    
    def test_efficate(self):
        data_incomplet = self.data3
        data_complet = self.data4
        efficacite(data_incomplet, data_complet)
        efficacite2(data_incomplet, data_complet)
        #efficacite_simple(data_incomplet,data_complet)

    def test_prediction_item(self):
        data_incomplet = self.data3
        data_complet = self.data4
        #efficacite_simple(data_incomplet,data_complet)
    """  
    def test_prediction(self):
        used_data = self.data
        u=get_user_data(used_data,0)
        item=1
        liste=get_liste_utilisateur(used_data,item)
        self.assertEqual(prediction(u,item,liste), 5)

    def test_prediction2(self):
        used_data = self.data
        u=get_user_data(used_data,0)
        item=1
        liste=get_liste_utilisateur(used_data,item)
        self.assertEqual(prediction_cosine(u,item,liste), 5)
    
    def test_prediction_gros(self):
        used_data = self.data3
        u=get_user_data(used_data,0)
        item=3
        liste=get_liste_utilisateur(used_data,item)
        self.assertEqual(prediction(u,item,liste), 2)

    def test_prediction2_gros(self):
        used_data = self.data3
        u=get_user_data(used_data,0)
        item=3
        liste=get_liste_utilisateur(used_data,item)
        self.assertEqual(prediction_cosine(u,item,liste), 2)
    
    
    """


if __name__ == "__main__":
    unittest.main()
