from email.mime import base
from matplotlib.colors import NoNorm
import numpy as np
import pandas as pd

from profile import Profile
import matplotlib.pyplot as plt


class Hours:
    base = 'Base'
    peak = 'Peak'
    off_peak = 'Off-Peak'


class Products:
    none = None
    cal = 'Cal'
    q = 'Quarter'
    m = 'Month'



class Hedging:
    def __init__(self, to_hedge_profile: Profile):
        self.hedge_type = ''
        self.hedge_products_table = None
        self.to_hedge_profile_obj = to_hedge_profile

    def calc_quantity_hedge(self, product=Products.cal, hour=Hours.base):
        """Calculate a quantity hedge base on the profile - product eg. 'Cal' and hours eg. 'Peak' """
        self.hedge_type = f'{product} {hour}'
        # find base or peak or off-peak hours according to hour input
        self.__hour_matcher(hour)

        # grouping df into the hours and products
        grouped_by_hedge_product = self.__product_grouper(product=product)['mw']

        # calculate and assign every hour with the hedge product value
        self.to_hedge_profile_obj.df_profile['hedge_mw'] = grouped_by_hedge_product.transform('mean')
        self.to_hedge_profile_obj.df_profile.loc[
            self.to_hedge_profile_obj.df_profile['hedge_hour'] == False, ['hedge_mw']] = np.NaN
        
        # store the hedge products
        self.hedge_products_table = self.__hedge_per_product_table(product)
        
        # calculation residual profil
        self.__calc_residual_profile()

        # return the hedge table as df
        return self.hedge_products_table

    def combinations_of_quantity_hedge(self, base_product:Products=Products.none, peak_product:Products=Products.none):
        hedges = { 
            'base' : {},
            'peak' : {}
        }

        # only base
        if base_product and not peak_product:
            self.calc_quantity_hedge(product=base_product, hour=Hours.base)
            hedges['base'] = self.__hedge_df_to_dict()

        # only peak
        elif not base_product and peak_product:
            self.calc_quantity_hedge(product=peak_product, hour=Hours.peak)
            hedges['peak'] = self.__hedge_df_to_dict()

        # base and peak products
        if base_product and peak_product:
            # the base hedge is set to the off-peak quantity
            off_peak_hedge_df = self.calc_quantity_hedge(product=base_product, hour=Hours.off_peak) 
            hedges['base'] = self.__hedge_df_to_dict()
 
            # peak quantity calculation
            peak_hedge_df = self.calc_quantity_hedge(product=peak_product, hour=Hours.peak)

            # same duration of products i.e both cal or both q
            if base_product == peak_product:
                # substract off_peak from peak 
                peak_hedge_df['hedge_mw'] = peak_hedge_df['hedge_mw'] -  off_peak_hedge_df['hedge_mw']
            
            # base in cal and peak in q 
            if base_product==Products.cal and peak_product==Products.q:
                # peak hedges are the calculated peak hedges minus the cal base hedge
                peak_hedge_df['hedge_mw'] = peak_hedge_df['hedge_mw'] -  off_peak_hedge_df['hedge_mw'][0]
            
            # base in q and peak in cal
            if base_product==Products.q and peak_product==Products.cal:
                # off-peak cal hedge needs to be calculated and then substracted from the cal peak quantity
                off_peak_cal_hedge_df = self.calc_quantity_hedge(product=peak_product, hour=Hours.off_peak) # cal off-peak
                peak_hedge_df['hedge_mw'] = peak_hedge_df['hedge_mw'] -  off_peak_cal_hedge_df['hedge_mw']
            
            hedges['peak'] = peak_hedge_df.to_dict('list')

        return hedges


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
            grouped_profile = self.to_hedge_profile_obj.df_profile.groupby(['hedge_hour', 'year'])
            self.to_hedge_profile_obj.df_profile['hedge_group'] = self.to_hedge_profile_obj.df_profile.index.to_period(
                'Y')
        elif product == Products.q:
            grouped_profile = self.to_hedge_profile_obj.df_profile.groupby(['hedge_hour', 'year', 'quarter'])
            self.to_hedge_profile_obj.df_profile['hedge_group'] = self.to_hedge_profile_obj.df_profile.index.to_period(
                'Q')
        elif product == Products.m:
            grouped_profile = self.to_hedge_profile_obj.df_profile.groupby(['hedge_hour', 'year', 'month'])
            self.to_hedge_profile_obj.df_profile['hedge_group'] = self.to_hedge_profile_obj.df_profile.index.to_period(
                'M')

        return grouped_profile

    def __calc_residual_profile(self):
        self.to_hedge_profile_obj.df_profile['residual'] = self.to_hedge_profile_obj.df_profile['mw'] - \
                                                           self.to_hedge_profile_obj.df_profile['hedge_mw']

    def __hedge_per_product_table(self, product:Products):
        temp_df = self.to_hedge_profile_obj.df_profile.groupby('hedge_group').mean()
        temp_df.reset_index(inplace=True)
        
        if  product==Products.cal:
            temp_df['hedge_group'] = temp_df['hedge_group'].apply(lambda x: x.strftime('%F'))
        elif product==Products.q:
            temp_df['hedge_group'] = temp_df['hedge_group'].apply(lambda x: x.strftime('%F-Q%q'))
        
        return temp_df[['hedge_group', 'hedge_mw']]

    def __hedge_df_to_dict(self): 
        return self.hedge_products_table.to_dict('list')

    def print_hedge(self):
        """print the hedging values to the console"""
        print(self.hedge_type)
        print(self.hedge_products_table)

    def plot_hedge(self):
        """plot the hedging values to a bar plot"""
        df = self.__readable_hedge_output()['hedge_mw'].plot(kind='bar', title=self.hedge_type)
        plt.show()

    def print_head_profiledata(self, rows=5):
        # print the first few rows of the profile
        print(self.to_hedge_profile_obj.df_profile.head(rows))
        print(self.to_hedge_profile_obj.df_profile.dtypes)

    def export_hedge_df_to_csv(self, filename='hedge.csv'):
        self.to_hedge_profile_obj.df_profile.to_csv(filename)

    def plot_hourly(self, show_residual=False):
        if show_residual:
            self.to_hedge_profile_obj.df_profile.plot(y=['mw', 'hedge_mw', 'residual'])
            plt.legend(['Profil', self.hedge_type,'Rest'])
        else:
            self.to_hedge_profile_obj.df_profile.plot(y=['mw', 'hedge_mw'])
            plt.legend(['Profil', self.hedge_type])
        plt.show()

    def get_residual_as_profile(self):
        return Profile(profile=self.to_hedge_profile_obj.df_profile['residual'].to_frame().rename(columns={'residual':'mw'}), type='residual')


    
