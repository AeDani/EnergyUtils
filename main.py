from profile import Profile
import hedging as hd
import pandas as pd
import matplotlib.pyplot as plt

#---- import of a profile
evu25 = Profile.import_csv('Assets/evu-25.csv', col_name='mw')

##--- initialer Hedge
hedge = hd.Hedging(evu25)
hedge.get_quantity_hedge(hd.Products.cal, hd.Hours.base)
hedge.print_hedge()
#hedge.plot_hedge()
#hedge.plot_hourly(True)


# #--- op nochmals hedgen
op = hedge.get_residual_as_profile()
op_hd = hd.Hedging(op)
op_hd.get_quantity_hedge(hd.Products.q, hd.Hours.base)
op_hd.print_hedge()
# hedge.plot_hedge()
op_hd.plot_hourly(False)




# import a fwc
fwc = Profile.import_csv("Assets/fwc.csv", col_name='eur_mwh')
# fwc.df_profile.plot()
# plt.show()


