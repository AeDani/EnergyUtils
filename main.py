from profile import Profile
import pandas as pd
import matplotlib.pyplot as plt

# import of a profile
evu25 = Profile.import_csv('Assets/evu-25.csv', col_name='mw')
print(evu25.df_profile.head(24))
evu25.df_profile.plot()
plt.show()


# import a fwc
fwc = Profile.import_csv("Assets/fwc.csv", col_name='eur_mwh')
fwc.df_profile.plot()
plt.show()


