import unittest
from profile import *
from hedging import *


class TestHedgingCombinationsBaseProfilEachQuarter(unittest.TestCase):
    def setUp(self) -> None:
        self.test_profile = Profile.import_csv('Tests/base_per_quarter.csv', col_name='mw')
    
    def dummy_test(self):
        self.assertEqual(sum([1,2,3]),6, "Should be 6")
    
    def test_base_cal_only(self):
        hedges = {
            'base': {'hedge_group': ['2025'], 'hedge_mw': [2.509931506849315]}, 
            'peak': {}
            }
        result = Hedging(self.test_profile).combinations_of_quantity_hedge(base_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_peak_cal_only(self):
        hedges = {
            'base': {}, 
            'peak': {'hedge_group': ['2025'], 'hedge_mw': [2.5134099616858236]}
            }
        result = Hedging(self.test_profile).combinations_of_quantity_hedge(peak_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_q_only(self):
        hedges = {
            'base': {'hedge_group': ['2025-Q1','2025-Q2','2025-Q3','2025-Q4'], 'hedge_mw': [1,2,3,4]}, 
            'peak': {}
            }
        result = Hedging(self.test_profile).combinations_of_quantity_hedge(base_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_peak_q_only(self):
        hedges = {
            'base': {}, 
            'peak': {'hedge_group': ['2025-Q1','2025-Q2','2025-Q3','2025-Q4'], 'hedge_mw': [1,2,3,4]}
            }
        result = Hedging(self.test_profile).combinations_of_quantity_hedge(peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_peak_q_only(self):
        hedges = {
            'base': {}, 
            'peak': {'hedge_group': ['2025-Q1','2025-Q2','2025-Q3','2025-Q4'], 'hedge_mw': [1,2,3,4]}
            }
        result = Hedging(self.test_profile).combinations_of_quantity_hedge(peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_peak_cal(self):
        hedges = {
            'base': {'hedge_group': ['2025'], 'hedge_mw': [2.507995735607676]}, 
            'peak': {'hedge_group': ['2025'], 'hedge_mw': [0.005414226078147788]}
            }
        result = Hedging(self.test_profile).combinations_of_quantity_hedge(base_product = Products.cal, peak_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_peak_q(self):
        hedges = {
            'base': {'hedge_group': ['2025-Q1','2025-Q2','2025-Q3','2025-Q4'], 'hedge_mw': [1,2,3,4]}, 
            'peak': {'hedge_group': ['2025-Q1','2025-Q2','2025-Q3','2025-Q4'], 'hedge_mw': [0,0,0,0]}
            }
        result = Hedging(self.test_profile).combinations_of_quantity_hedge(base_product = Products.q, peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")



class TestHedgingCombinationsBasePeakProfil(unittest.TestCase):
    def setUp(self) -> None:
        self.test_profile = Profile.import_csv('Tests/peak_off_peak_per_quarter.csv', col_name='mw')
    
    def dummy_test(self):
        self.assertEqual(sum([1,2,3]),6, "Should be 6")
    
    def test_base_cal_only(self):
        hedges = {
            'base': {'hedge_group': ['2025'], 'hedge_mw': [6.08527397260274]}, 
            'peak': {}
            }
        result = Hedging(self.test_profile).combinations_of_quantity_hedge(base_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_peak_cal_only(self):
        hedges = {
            'base': {}, 
            'peak': {'hedge_group': ['2025'], 'hedge_mw': [12.513409961685824]}
            }
        result = Hedging(self.test_profile).combinations_of_quantity_hedge(peak_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_q_only(self):
        hedges = {
            'base': {'hedge_group': ['2025-Q1','2025-Q2','2025-Q3','2025-Q4'], 'hedge_mw': [4.557202408522464, 5.571428571428571, 6.586956521739131, 7.585332729741965]}, 
            'peak': {}
            }
        result = Hedging(self.test_profile).combinations_of_quantity_hedge(base_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_peak_q_only(self):
        hedges = {
            'base': {}, 
            'peak': {'hedge_group': ['2025-Q1','2025-Q2','2025-Q3','2025-Q4'], 'hedge_mw': [1,2,3,4]}
            }
        result = Hedging(self.test_profile).combinations_of_quantity_hedge(peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_peak_q_only(self):
        hedges = {
            'base': {}, 
            'peak': {'hedge_group': ['2025-Q1','2025-Q2','2025-Q3','2025-Q4'], 'hedge_mw': [11,12,13,14]}
            }
        result = Hedging(self.test_profile).combinations_of_quantity_hedge(peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_peak_cal(self):
        hedges = {
            'base': {'hedge_group': ['2025'], 'hedge_mw': [2.507995735607676]}, 
            'peak': {'hedge_group': ['2025'], 'hedge_mw': [10.005414226078148]}
            }
        result = Hedging(self.test_profile).combinations_of_quantity_hedge(base_product = Products.cal, peak_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_peak_q(self):
        hedges = {
            'base': {'hedge_group': ['2025-Q1','2025-Q2','2025-Q3','2025-Q4'], 'hedge_mw': [1,2,3,4]}, 
            'peak': {'hedge_group': ['2025-Q1','2025-Q2','2025-Q3','2025-Q4'], 'hedge_mw': [10,10,10,10]}
            }
        result = Hedging(self.test_profile).combinations_of_quantity_hedge(base_product = Products.q, peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")




if __name__ == '__main__':
    unittest.main()