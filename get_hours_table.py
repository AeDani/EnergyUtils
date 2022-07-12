from profile import *

# Profil erstellen
evu25 = Profile.import_csv('Assets/evu-25.csv', col_name='mw')

evu25.df_profile

print(evu25.get_hours_table())