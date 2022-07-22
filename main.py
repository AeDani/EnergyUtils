from modules.profile import *
from modules.hedging import *

# File with different examples how to use Profile and Hedging Class

# Profil erstellen
evu25 = HourProfile.import_csv('Assets/evu-25.csv')
# Stundentabelle Peak / off Peak erhalten
print(evu25.get_hours_table())

##--- single Hedge
hedge = Hedging(evu25)
hedge.calc_quantity_hedges(Products.cal, Hours.base)
hedge.calc_quantity_hedges(Products.cal, Hours.peak)
hedge.calc_quantity_hedges(Products.cal, Hours.off_peak)
hedge.print_hedges()


##--------- Hedging Base-Peak Combinations

## only base
list = hedge.combinations_of_quantity_hedge(base_product = Products.cal)
for tp in list:
    print(tp)
    print(tp.get_mwh())

list = hedge.combinations_of_quantity_hedge(base_product = Products.q)
for tp in list:
    print(tp)
    print(tp.get_mwh())

## only peak
list = hedge.combinations_of_quantity_hedge(peak_product = Products.cal)
for tp in list:
    print(tp)
    print(tp.get_mwh())

list = hedge.combinations_of_quantity_hedge(peak_product = Products.q)
for tp in list:
    print(tp)
    print(tp.get_mwh())

## base and peak in cal
list = hedge.combinations_of_quantity_hedge(base_product = Products.cal, peak_product = Products.cal)
for tp in list:
    print(tp)
    print(tp.get_mwh())

## base and peak in q
list = hedge.combinations_of_quantity_hedge(base_product = Products.q, peak_product = Products.q)
for tp in list:
    print(tp)
    print(tp.get_mwh())

## base cal and peak in q
list = hedge.combinations_of_quantity_hedge(base_product = Products.cal, peak_product = Products.q)
for tp in list:
    print(tp)
    print(tp.get_mwh())

## base q and peak in cal
list = hedge.combinations_of_quantity_hedge(base_product = Products.q, peak_product = Products.cal)
for tp in list:
    print(tp)
    print(tp.get_mwh())