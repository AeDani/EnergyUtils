from modules.profile import *
from modules.hedging import *
import pandas as pd
import matplotlib.pyplot as plt

# File with different examples how to use Profile and Hedging Class

# Profil erstellen
evu25 = HourProfile.import_csv('Assets/evu-25.csv', col_name='mw')
# Stundentabelle Peak / off Peak erhalten
print(evu25.get_hours_table())

##--- initialer Hedge
hedge = Hedging(evu25)
hedge.calc_quantity_hedges(Products.cal, Hours.base)
hedge.print_hedge()
hedge.calc_quantity_hedges(Products.cal, Hours.peak)
hedge.print_hedge()
hedge.calc_quantity_hedges(Products.cal, Hours.off_peak)
hedge.print_hedge()
#hedge.plot_hedge()
#hedge.plot_hourly(True)


##--- op nochmals hedgen
op = hedge.get_residual_as_profile()
op_hd = Hedging(op)
op_hd.calc_quantity_hedges(Products.q, Hours.base)
op_hd.print_hedge()
# hedge.plot_hedge()
op_hd.plot_hourly(False)


##--------- Hedging Base-Peak Combinations

## only base
a = hedge.combinations_of_quantity_hedge(base_product = Products.cal)
print(a)

a = hedge.combinations_of_quantity_hedge(base_product = Products.q)
print(a)

## only peak
a = hedge.combinations_of_quantity_hedge(peak_product = Products.cal)
print(a)

a = hedge.combinations_of_quantity_hedge(peak_product = Products.q)
print(a)

## base and peak in cal
a = hedge.combinations_of_quantity_hedge(base_product = Products.cal, peak_product = Products.cal)
print(a)

## base and peak in q
a = hedge.combinations_of_quantity_hedge(base_product = Products.q, peak_product = Products.q)
print(a)

## base cal and peak in q
a = hedge.combinations_of_quantity_hedge(base_product = Products.cal, peak_product = Products.q)
print(a)

## base q and peak in cal
a = hedge.combinations_of_quantity_hedge(base_product = Products.q, peak_product = Products.cal)
print(a)