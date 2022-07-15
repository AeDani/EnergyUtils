import pandas as pd
import matplotlib.pyplot as plt  

from modules.profile import HourProfile
from modules.hedging import *


print(HourProfile)
# Profil erstellen
file = 'base_per_quarter.csv'
path = 'Tests/'
file_path = f'{path}{file}'

evu25 = HourProfile.import_csv(file_path, col_name='mw')
# Stundentabelle Peak / off Peak erhalten
print(evu25.get_hours_table())
hedge = Hedging(evu25)

a = hedge.combinations_of_quantity_hedge(base_product= Products.cal, peak_product = Products.cal)
print(a)

print(hedge.get_mwh_of_residual_profile())