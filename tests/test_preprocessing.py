from flood_forecast.preprocessing.interpolate_preprocess import back_forward_generic
from flood_forecast.preprocessing.temporal_feats import feature_fix
import unittest
import pandas as pd
import os


class TestInterpolationCode(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), "test_data", "farm_ex.csv")
        file_path_2 = os.path.join(os.path.dirname(__file__), "test_data", "fake_test_small.csv")
        self.df = pd.read_csv(file_path)
        self.df_2 = pd.read_csv(file_path_2, delimiter="\t")

    def test_back_forward(self):
        """Test the generation of forward and backward data
        """
        df = back_forward_generic(self.df, ["NumberOfAnimals"])
        self.assertEqual(df.iloc[3]["NumberOfAnimals"], 165)

    def test_make_temp_feats(self):
        feats = feature_fix({"hour": "cyclical"}, "datetime", self.df_2)
        self.assertIn("sin_hour", feats.columns)
        self.assertIn("cos_hour", feats.columns)

if __name__ == '__main__':
    unittest.main()
