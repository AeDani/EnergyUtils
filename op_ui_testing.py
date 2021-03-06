from modules.enums import *
from modules.fwcImporter import *
from modules.hedging import Hedging


# Price curve CHMPK
file = 'Assets/ui/20220726Sammlerexport.csv'
chmpk_chf = PriceCurve.import_chmpk_in_ch(file)

# MW profile to hedge
file = 'gobat.csv'
path = 'Assets/ui/'
file_path = f'{path}{file}'

profil_mw = HourProfile.import_csv(file_path)

hedge = Hedging(profil_mw)
hedge.add_price_curve(chmpk_chf)

# peak_product=Products.cal,
hedge.combinations_of_hedge(base_product=Products.cal, peak_product=Products.q, hedge_type=HedgeType.value)
hedge.print_hedges()
hedge.print_all_mwh_of_residual()
