import unittest
from modules.profile import *
from modules.hedging import *
from modules.tradingProduct import *


class TestHedgingCombinationsAllOnesProfile(unittest.TestCase):
    def setUp(self) -> None:
        self.test_profile = HourProfile.import_csv('Tests/all_ones.csv')
    
    def test_dummy(self):
        self.assertEqual(sum([1,2,3]),6, "Should be 6")
    
    def test_base_cal_only(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=1)
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(base_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_peak_cal_only(self):
        hedges = [
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=1)
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(peak_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_q_only(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=1),
            TradingProduct(type=Hours.base, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=1),
            TradingProduct(type=Hours.base, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=1),
            TradingProduct(type=Hours.base, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=1),
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(base_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_peak_q_only(self):
        hedges = [
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=1),
            TradingProduct(type=Hours.peak, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=1),
            TradingProduct(type=Hours.peak, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=1),
            TradingProduct(type=Hours.peak, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=1),
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_peak_cal(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=1),
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=0)
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(base_product = Products.cal, peak_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_peak_q(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=1),
            TradingProduct(type=Hours.base, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=1),
            TradingProduct(type=Hours.base, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=1),
            TradingProduct(type=Hours.base, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=1),
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=0),
            TradingProduct(type=Hours.peak, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=0),
            TradingProduct(type=Hours.peak, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=0),
            TradingProduct(type=Hours.peak, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=0),
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(base_product = Products.q, peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")
    
    def test_base_cal_peak_q(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=1),
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=0),
            TradingProduct(type=Hours.peak, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=0),
            TradingProduct(type=Hours.peak, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=0),
            TradingProduct(type=Hours.peak, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=0),
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(base_product = Products.cal, peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")



class TestHedgingCombinationsBaseProfilEachQuarter(unittest.TestCase):
    def setUp(self) -> None:
        self.test_profile = HourProfile.import_csv('Tests/base_per_quarter.csv')
    
    def dummy_test(self):
        self.assertEqual(sum([1,2,3]),6, "Should be 6")
    
    def test_base_cal_only(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=2.51)
        ]  
        result = Hedging(self.test_profile).combinations_of_hedge(base_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_peak_cal_only(self):
        hedges = [
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=2.51)
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(peak_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_q_only(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=1),
            TradingProduct(type=Hours.base, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=2),
            TradingProduct(type=Hours.base, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=3),
            TradingProduct(type=Hours.base, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=4),
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(base_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_peak_q_only(self):
        hedges = [
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=1),
            TradingProduct(type=Hours.peak, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=2),
            TradingProduct(type=Hours.peak, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=3),
            TradingProduct(type=Hours.peak, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=4)
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_peak_cal(self):
        hedges = {
            'base': {'hedge_group': ['2025'], 'hedge_mw': [2.5080]}, 
            'peak': {'hedge_group': ['2025'], 'hedge_mw': [0.0054]}
            }
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=2.51),
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=0.00),
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(base_product = Products.cal, peak_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_peak_q(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=1),
            TradingProduct(type=Hours.base, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=2),
            TradingProduct(type=Hours.base, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=3),
            TradingProduct(type=Hours.base, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=4),
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=0),
            TradingProduct(type=Hours.peak, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=0),
            TradingProduct(type=Hours.peak, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=0),
            TradingProduct(type=Hours.peak, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=0),
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(base_product = Products.q, peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")
    
    def test_base_cal_peak_q(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=2.51),
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=-1.51),
            TradingProduct(type=Hours.peak, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=-0.51),
            TradingProduct(type=Hours.peak, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=0.49),
            TradingProduct(type=Hours.peak, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=1.49),
        ]  
        result = Hedging(self.test_profile).combinations_of_hedge(base_product = Products.cal, peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")


class TestHedgingCombinationsBasePeakProfil(unittest.TestCase):
    def setUp(self) -> None:
        self.test_profile = HourProfile.import_csv('Tests/peak_off_peak_per_quarter.csv')
    
    def dummy_test(self):
        self.assertEqual(sum([1,2,3]),6, "Should be 6")
    
    def test_base_cal_only(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=6.09)
        ]  
        result = Hedging(self.test_profile).combinations_of_hedge(base_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_peak_cal_only(self):
        hedges = [
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=12.51)
        ]  
        result = Hedging(self.test_profile).combinations_of_hedge(peak_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_q_only(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=4.56),
            TradingProduct(type=Hours.base, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=5.57),
            TradingProduct(type=Hours.base, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=6.59),
            TradingProduct(type=Hours.base, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=7.59),
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(base_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_peak_q_only(self):
        hedges = [
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=11),
            TradingProduct(type=Hours.peak, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=12),
            TradingProduct(type=Hours.peak, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=13),
            TradingProduct(type=Hours.peak, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=14),
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_peak_cal(self):
        hedges = {
            'base': {'hedge_group': ['2025'], 'hedge_mw': [2.5080]}, 
            'peak': {'hedge_group': ['2025'], 'hedge_mw': [10.0054]}
            }
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=2.51),
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=10.00)
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(base_product = Products.cal, peak_product=Products.cal)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_peak_q(self): 
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=1),
            TradingProduct(type=Hours.base, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=2),
            TradingProduct(type=Hours.base, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=3),
            TradingProduct(type=Hours.base, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=4),
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=10),
            TradingProduct(type=Hours.peak, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=10),
            TradingProduct(type=Hours.peak, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=10),
            TradingProduct(type=Hours.peak, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=10),
        ]
        result = Hedging(self.test_profile).combinations_of_hedge(base_product = Products.q, peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")

    def test_base_cal_peak_q(self):
        hedges = {
            'base': {'hedge_group': ['2025'], 'hedge_mw': [2.5080]}, 
            'peak': {'hedge_group': ['2025-Q1','2025-Q2','2025-Q3','2025-Q4'], 'hedge_mw': [8.4920, 9.4920, 10.4920, 11.4920]}
            }
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=2.51),
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=8.49),
            TradingProduct(type=Hours.peak, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=9.49),
            TradingProduct(type=Hours.peak, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=10.49),
            TradingProduct(type=Hours.peak, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=11.49),
        ] 
        result = Hedging(self.test_profile).combinations_of_hedge(base_product = Products.cal, peak_product=Products.q)
        self.assertEqual(result,hedges, "Wrong hedge output")




if __name__ == '__main__':
    unittest.main()