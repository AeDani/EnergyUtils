from modules.profile import *
from modules.hedging import *

# File with different examples how to use Profile and Hedging Class

# Profil erstellen
evu25 = HourProfile.import_csv('Assets/evu-25.csv', name_val="12")
# Stundentabelle Peak / off Peak erhalten
print(evu25.get_hours_table())

##--- Single Hedge
hedge = Hedging(evu25)
hedge.calc_quantity_hedges(Products.cal, Hours.base)
hedge.calc_quantity_hedges(Products.cal, Hours.peak)
hedge.calc_quantity_hedges(Products.cal, Hours.off_peak)
hedge.print_hedges()


##--- Hedge Combinations
hedge.clear_previous_hedges()
hedge.combinations_of_hedge(base_product=Products.cal, peak_product=Products.cal)
hedge.print_hedges()
hedge.print_all_mwh_of_residual()