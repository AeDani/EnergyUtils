from profile import Profile
import hedging as hd
import pandas as pd
import matplotlib.pyplot as plt


#---- import of a profile
evu25 = Profile.import_csv('Assets/evu-25.csv', col_name='mw')

##--- Nur Cal-Base Hedge
hedge = hd.Hedging(evu25)
hedge.calc_quantity_hedge(hd.Products.cal, hd.Hours.base)
hedge.print_hedge()

##--- Nur Q-Base Hedge
hedge = hd.Hedging(evu25)
hedge.calc_quantity_hedge(hd.Products.q, hd.Hours.base)
hedge.print_hedge()


a = hedge.combinations_of_quantity_hedge(hd.Products.q)
print(a)
