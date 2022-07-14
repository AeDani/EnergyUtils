from profile import Profile
import hedging as hd
import pandas as pd
import matplotlib.pyplot as plt

# File with different examples how to use Profile and Hedging Class

# Profil erstellen
evu25 = Profile.import_csv('Assets/evu-25.csv', col_name='mw')
# Stundentabelle Peak / off Peak erhalten
print(evu25.get_hours_table())

##--- initialer Hedge
hedge = hd.Hedging(evu25)
hedge.calc_quantity_hedge(hd.Products.cal, hd.Hours.base)
hedge.print_hedge()
hedge.calc_quantity_hedge(hd.Products.cal, hd.Hours.peak)
hedge.print_hedge()
hedge.calc_quantity_hedge(hd.Products.cal, hd.Hours.off_peak)
hedge.print_hedge()
#hedge.plot_hedge()
#hedge.plot_hourly(True)


##--- op nochmals hedgen
op = hedge.get_residual_as_profile()
op_hd = hd.Hedging(op)
op_hd.calc_quantity_hedge(hd.Products.q, hd.Hours.base)
op_hd.print_hedge()
# hedge.plot_hedge()
op_hd.plot_hourly(False)


##--------- Hedging Base-Peak Combinations

## only base
a = hedge.combinations_of_quantity_hedge(base_product = hd.Products.cal)
print(a)

a = hedge.combinations_of_quantity_hedge(base_product = hd.Products.q)
print(a)

## only peak
a = hedge.combinations_of_quantity_hedge(peak_product = hd.Products.cal)
print(a)

a = hedge.combinations_of_quantity_hedge(peak_product = hd.Products.q)
print(a)

## base and peak in cal
a = hedge.combinations_of_quantity_hedge(base_product = hd.Products.cal, peak_product = hd.Products.cal)
print(a)

## base and peak in q
a = hedge.combinations_of_quantity_hedge(base_product = hd.Products.q, peak_product = hd.Products.q)
print(a)

## base cal and peak in q
a = hedge.combinations_of_quantity_hedge(base_product = hd.Products.cal, peak_product = hd.Products.q)
print(a)

## base q and peak in cal
a = hedge.combinations_of_quantity_hedge(base_product = hd.Products.q, peak_product = hd.Products.cal)
print(a)