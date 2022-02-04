from profile import Profile
import matplotlib.pyplot as plt


class Hours:
    base = 'Base'
    peak = 'Peak'
    off_peak = 'Off-Peak'


class Products:
    cal = 'Cal'
    q = 'Q'
    m = 'M'


class Hedging:
    def __init__(self, to_hedge_profile: Profile):
        self.hedge_type = ''
        self.hedge_products = None
        self.to_hedge_profile_obj = to_hedge_profile

    def get_quantity_hedge(self, product=Products.cal, hour=Hours.base):
        """Calculate a quantity hedge base on the profile - product eg. 'Cal' and hours eg. 'Peak' """
        self.hedge_type = f'{product} {hour}'
        self.__hour_matcher(hour)
        self.hedge_products = self.__product_grouper(product=product)['mw'].mean()

        # TODO Hedge as hourly profile

        # TODO residual profil berechnen

    def __hour_matcher(self, hour: Hours):
        """find the hours matching the input of hour"""
        if hour == Hours.base:
            self.to_hedge_profile_obj.df_profile['hedge_hour'] = True
        elif hour == Hours.off_peak:
            self.to_hedge_profile_obj.df_profile['hedge_hour'] = self.to_hedge_profile_obj.df_profile['is_peak'] \
                .map({True: False, False: True})
        elif hour == Hours.peak:
            self.to_hedge_profile_obj.df_profile['hedge_hour'] = self.to_hedge_profile_obj.df_profile['is_peak']

    def __product_grouper(self, product: Products):
        """find the product hours matching the input and group the date accordingly"""
        if product == Products.cal:
            grouped_profile = self.to_hedge_profile_obj.df_profile.groupby(['hedge_hour','year'])
        elif product == Products.q:
            grouped_profile = self.to_hedge_profile_obj.df_profile.groupby(['hedge_hour','year', 'quarter'])
        elif product == Products.m:
            grouped_profile = self.to_hedge_profile_obj.df_profile.groupby(['hedge_hour','year', 'month'])

        return grouped_profile

    def print_hedge(self):
        """print the hedging values to the console"""
        print(self.hedge_type)
        idx = self.hedge_products.index.get_level_values('hedge_hour')==True
        print(self.hedge_products.loc[idx])

    def plot_hedge(self):
        """plot the hedging values to a bar plot"""
        self.hedge_products.plot(x=['year', 'month'], y='mw', kind='bar')
        plt.show()
