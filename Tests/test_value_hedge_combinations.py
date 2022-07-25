import unittest
from modules.profile import *
from modules.hedging import *
from modules.tradingProduct import *
from modules.fwcImporter import *


class ValueHedgeCombinationsEvu25(unittest.TestCase):
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
    
    def test_base_cal_only(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=1.25)
        ]
        result = self.evu_25_hedging.combinations_of_hedge(base_product=Products.cal, hedge_type=HedgeType.value )
        self.assertEqual(result, hedges, "Wrong hedge output")

    def test_base_q_only(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=1.47),
            TradingProduct(type=Hours.base, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=0.99),
            TradingProduct(type=Hours.base, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=0.89),
            TradingProduct(type=Hours.base, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=1.43),
        ]
        result = self.evu_25_hedging.combinations_of_hedge(base_product=Products.q, hedge_type=HedgeType.value)
        self.assertEqual(result, hedges, "Wrong hedge output")
    
    def test_peak_cal(self):
        hedges = [
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=1.21)
        ]
        result = self.evu_25_hedging.combinations_of_hedge(peak_product=Products.cal, hedge_type=HedgeType.value)
        self.assertEqual(result, hedges, "Wrong hedge output")

    def test_peak_q_only(self):
        hedges = [
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=1.43),
            TradingProduct(type=Hours.peak, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=0.86),
            TradingProduct(type=Hours.peak, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=0.81),
            TradingProduct(type=Hours.peak, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=1.44),
        ]
        result = self.evu_25_hedging.combinations_of_hedge(peak_product=Products.q, hedge_type=HedgeType.value)
        self.assertEqual(result, hedges, "Wrong hedge output")

    def test_base_peak_cal(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=1.29),
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=-0.08)
        ]
        result = self.evu_25_hedging.combinations_of_hedge(base_product=Products.cal, peak_product=Products.cal, hedge_type=HedgeType.value)
        self.assertEqual(result, hedges, "Wrong hedge output")


    def test_base_peak_q(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=1.50),
            TradingProduct(type=Hours.base, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=1.08),
            TradingProduct(type=Hours.base, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=0.95),
            TradingProduct(type=Hours.base, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=1.42),
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=-0.07),
            TradingProduct(type=Hours.peak, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=-0.22),
            TradingProduct(type=Hours.peak, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=-0.14),
            TradingProduct(type=Hours.peak, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=0.02),   
        ]
        result = self.evu_25_hedging.combinations_of_hedge(base_product=Products.q, peak_product=Products.q, hedge_type=HedgeType.value)
        self.assertEqual(result, hedges, "Wrong hedge output")

    def test_base_cal_peak_q(self):
        hedges = [
            TradingProduct(type=Hours.base, start='2025-01-01 00:00', end='2025-12-31 23:00', mw=1.29),
            TradingProduct(type=Hours.peak, start='2025-01-01 00:00', end='2025-03-31 23:00', mw=0.14),
            TradingProduct(type=Hours.peak, start='2025-04-01 00:00', end='2025-06-30 23:00', mw=-0.43),
            TradingProduct(type=Hours.peak, start='2025-07-01 00:00', end='2025-09-30 23:00', mw=-0.48),
            TradingProduct(type=Hours.peak, start='2025-10-01 00:00', end='2025-12-31 23:00', mw=0.15)
        ]
        result = self.evu_25_hedging.combinations_of_hedge(base_product=Products.cal, peak_product=Products.q, hedge_type=HedgeType.value)
        self.assertEqual(result, hedges, "Wrong hedge output")