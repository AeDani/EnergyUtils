from profile import Profile
import matplotlib.pyplot as plt


class Hours:
    base = 'Base',
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

        if product == Products.cal:
            grouped_profile = self.to_hedge_profile_obj.df_profile.groupby('year')
        elif product == Products.q:
            grouped_profile = self.to_hedge_profile_obj.df_profile.groupby(['year', 'quarter'])
        elif product == Products.m:
            grouped_profile = self.to_hedge_profile_obj.df_profile.groupby(['year', 'month'])

        self.hedge_products = grouped_profile['mw'].mean()

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

    def print_hedge(self):
        """print the hedging values to the console"""
        print(self.hedge_type)
        print(self.hedge_products)

    def plot_hedge(self):
        """plot the hedging values to a bar plot"""
        self.hedge_products.plot(x=['year', 'month'], y='mw', kind='bar')
        plt.show()
