import unittest
from modules.profile import *
from modules.hedging import *
from modules.tradingProduct import *
from modules.fwcImporter import *


class ValueHedgeEvu25(unittest.TestCase):
    def setUp(self) -> None:
        # mw profile
        test_profile = HourProfile.import_csv('Tests/evu-25.csv')
        self.evu_25_hedging = Hedging(test_profile)
        
        # Price curve CHMPK
        file = 'Tests/20220715Sammlerexport.csv'
        chmpk_chf = PriceCurve.import_chmpk_in_ch(file)
        self.evu_25_hedging.add_price_curve(chmpk_chf)
    
    def test_dummy(self):
        self.assertEqual(sum([1,2,3]),6, "Should be 6")
    
    def test_base_cal(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=1.25)
        ]
        result = self.evu_25_hedging.calc_value_hedges(product=Products.cal, hour=Hours.base)
        self.assertEqual(result, hedges, "Wrong hedge output")

    def test_base_q(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=1.47),
            TradingProduct(type=Hours.base, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=0.99),
            TradingProduct(type=Hours.base, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=0.89),
            TradingProduct(type=Hours.base, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=1.43),
        ]
        result = self.evu_25_hedging.calc_value_hedges(product=Products.q, hour=Hours.base)
        self.assertEqual(result, hedges, "Wrong hedge output")
    
    def test_peak_cal(self):
        hedges = [
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=1.21)
        ]
        result = self.evu_25_hedging.calc_value_hedges(product=Products.cal, hour=Hours.peak)
        self.assertEqual(result, hedges, "Wrong hedge output")

    def test_peak_q(self):
        hedges = [
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=1.43),
            TradingProduct(type=Hours.peak, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=0.86),
            TradingProduct(type=Hours.peak, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=0.81),
            TradingProduct(type=Hours.peak, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=1.44),
        ]
        result = self.evu_25_hedging.calc_value_hedges(product=Products.q, hour=Hours.peak)
        self.assertEqual(result, hedges, "Wrong hedge output")
