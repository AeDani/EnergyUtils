from profile import Profile
import hedging as hd
import pandas as pd
import matplotlib.pyplot as plt


#---- import of a profile
evu25 = Profile.import_csv('Assets/evu-25.csv', col_name='mw')
hedge = hd.Hedging(evu25)

# ##--- Nur Cal-Base Hedge
# 
# hedge.calc_quantity_hedge(hd.Products.cal, hd.Hours.base)
# hedge.print_hedge()

# ##--- Nur Q-Base Hedge
# hedge = hd.Hedging(evu25)
# hedge.calc_quantity_hedge(hd.Products.q, hd.Hours.base)
# hedge.print_hedge()


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