import pandas as pd
import matplotlib.pyplot as plt  

from modules.profile import HourProfile
from modules.hedging import *

# Profil erstellen
file = '1658481587013.csv'
path = 'Assets/'
file_path = f'{path}{file}'

evu25 = HourProfile.import_csv(file_path)
hedge = Hedging(evu25)
hedge.combinations_of_hedge(base_product= Products.cal, peak_product=Products.q)
hedge.print_hedges()
hedge.print_all_mwh_of_residual()

