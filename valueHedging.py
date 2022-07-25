from modules.enums import *
from modules.fwcImporter import *
from modules.hedging import Hedging

# Price curve CHMPK
file = 'Assets/20220715Sammlerexport.csv'
chmpk_chf = PriceCurve.import_chmpk_in_ch(file)

# MW profile to hedge
file = 'evu-25.csv'
path = 'Assets/'
file_path = f'{path}{file}'

profil_mw = HourProfile.import_csv(file_path)

hedge = Hedging(profil_mw)
hedge.add_price_curve(chmpk_chf)
hedge.calc_value_hedges(product=Products.q, hour=Hours.peak)
hedge.print_hedges()

hedge.clear_previous_hedges()
hedge.combinations_of_hedge(base_product=Products.q, hedge_type=HedgeType.value)
hedge.print_hedges()