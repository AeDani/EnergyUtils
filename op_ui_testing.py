from modules.enums import *
from modules.fwcImporter import *
from modules.hedging import Hedging
import time
start_time = time.time()



# Price curve CHMPK
file = 'Assets/20220715Sammlerexport.csv'
chmpk_chf = PriceCurve.import_chmpk_in_ch(file)

# MW profile to hedge
file = 'dumb.csv'
path = 'Assets/ui/'
file_path = f'{path}{file}'

profil_mw = HourProfile.import_csv(file_path)

hedge = Hedging(profil_mw)
hedge.add_price_curve(chmpk_chf)

hedge.clear_previous_hedges()
hedge.combinations_of_hedge(base_product=Products.q, peak_product=Products.q, hedge_type=HedgeType.value)
hedge.print_hedges()
hedge.print_all_mwh_of_residual()

print("--- %s seconds ---" % (time.time() - start_time))