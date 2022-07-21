import pandas as pd
import matplotlib.pyplot as plt  

from modules.profile import HourProfile
from modules.hedging import *


print(HourProfile)
# Profil erstellen
file = 'evu-25.csv'
path = 'Assets/'
file_path = f'{path}{file}'

evu25 = HourProfile.import_csv(file_path, col_name='mw')
# Stundentabelle Peak / off Peak erhalten
print(evu25.get_hours_table())
hedge = Hedging(evu25)

a = hedge.combinations_of_quantity_hedge(base_product= Products.cal)
for hedge in a:
    print(hedge)
    print(hedge.get_mwh())

