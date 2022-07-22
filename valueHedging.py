from modules.fwcImporter import *

# Price curve CHMPK
file = 'Assets/20220715Sammlerexport.csv'
chmpk_chf = PriceCurve.import_chmpk_in_ch(file, 2025)

# MW profile to hedge
file = '1658481587013.csv'
path = 'Assets/'
file_path = f'{path}{file}'

profil_mw = HourProfile.import_csv(file_path)