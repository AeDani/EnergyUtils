from profile import Profile
import hedging as hd
import pandas as pd
import matplotlib.pyplot as plt

#---- import of a profile
evu25 = Profile.import_csv('Assets/evu-25.csv', col_name='mw')
#print(evu25.df_profile.head(24))
# evu25.df_profile.plot()
# plt.show()

hedge = hd.Hedging(evu25)
hedge.get_quantity_hedge(hd.Products.q, hd.Hours.base)
hedge.print_hedge()
hedge.plot_hedge()



# import a fwc
fwc = Profile.import_csv("Assets/fwc.csv", col_name='eur_mwh')
# fwc.df_profile.plot()
# plt.show()


