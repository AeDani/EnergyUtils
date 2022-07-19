import profile
from matplotlib.colors import NoNorm
import numpy as np
import pandas as pd

from modules.profile import HourProfile
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
    def __init__(self, to_hedge_profile: HourProfile):
        self.to_hedge_profile_obj = to_hedge_profile
        self.hedge_product = []
        self.hedge_products_table = []
        self.hedge_timeseries_df = []
        
    def calc_quantity_hedge(self, product=Products.cal, hour=Hours.base):
        """Calculate a quantity hedge base on the profile - product eg. 'Cal' and hours eg. 'Peak' """
        
        # initialies a onw list entry with all the relevant timeseries for the upcoming hedge.
        self.hedge_product.append(f'{product} {hour}')
        profile = self.to_hedge_profile_obj.df_profile.copy()

        # find base or peak or off-peak hours according to hour input
        profile = self.__hour_matcher(profile=profile, hour=hour)

        # grouping df into the hours and products
        grouped_by_hedge_product = self.__product_grouper(profile=profile, product=product)

        # adjust index to cal,q or m
        profile = self.__to_period_on_index(profile=profile, product=product)

        # calculate and assign every hour with the hedge product value
        profile['hedge_mw'] = grouped_by_hedge_product.transform('mean')
        # write nan on the hours not included in the hedge
        profile.loc[profile['hedge_hour'] == False, ['hedge_mw']] = np.NaN
        # create another column with 0 instead of nan, to better caclulate later
        profile['hedge_mw_non_nan'] = profile['hedge_mw'].fillna(0)
        
        # store the hedge products
        self.hedge_products_table.append(self.__hedge_per_product_table(profile=profile, product=product))
        
        # calculation residual profil
        profile = self.__calc_residual_profile(profile=profile)

        # store the timeseries df
        self.hedge_timeseries_df.append(profile)

        # return the hedge table as df
        return self.hedge_products_table[-1]

    def combinations_of_quantity_hedge(self, base_product:Products=Products.none, peak_product:Products=Products.none):
        hedges = {
            'base' : {},
            'peak' : {}
        }

        # only base
        if base_product and not peak_product:
            self.calc_quantity_hedge(product=base_product, hour=Hours.base)
            hedges['base'] = self.__hedge_df_to_dict(self.hedge_products_table[-1])

        # only peak
        elif not base_product and peak_product:
            self.calc_quantity_hedge(product=peak_product, hour=Hours.peak)
            hedges['peak'] = self.__hedge_df_to_dict(self.hedge_products_table[-1])

        # base and peak products
        if base_product and peak_product:
            # the base hedge is set to the off-peak quantity
            off_peak_hedge_df = self.calc_quantity_hedge(product=base_product, hour=Hours.off_peak)
            hedges['base'] = self.__hedge_df_to_dict(self.hedge_products_table[-1])
 
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
            #to_dict rounds with an error and changes datatyp
            hedges['peak']['hedge_mw'] = [round(el,4) for el in hedges['peak']['hedge_mw']]

        return hedges

    @staticmethod
    def __hour_matcher(profile:pd.DataFrame, hour: Hours):
        """find the hours matching the input of hour"""
        if hour == Hours.base:
            profile['hedge_hour'] = True
        elif hour == Hours.off_peak:
            profile['hedge_hour'] = profile['is_peak'] \
                .map({True: False, False: True})
        elif hour == Hours.peak:
            profile['hedge_hour'] = profile['is_peak']
        return profile

    @staticmethod
    def __product_grouper(profile:pd.DataFrame, product: Products):
        """find the product hours matching the input and group the date accordingly"""
        if product == Products.cal:
            grouped_profile = profile.groupby(['hedge_hour', 'year'])
        elif product == Products.q:
            grouped_profile = profile.groupby(['hedge_hour', 'year', 'quarter'])
        elif product == Products.m:
            grouped_profile = profile.groupby(['hedge_hour', 'year', 'month'])

        return grouped_profile['mw']

    @staticmethod
    def __to_period_on_index(profile:pd.DataFrame, product: Products):
             
        if product == Products.cal:
            profile['hedge_group'] = profile.index.to_period('Y')
        elif product == Products.q:
            profile['hedge_group'] = profile.index.to_period('Q')
        elif product == Products.m:
           profile['hedge_group'] = profile.index.to_period(
                'M')
        
        return profile

    @staticmethod
    def __calc_residual_profile(profile:pd.DataFrame):
        profile['residual'] = profile['mw'] - profile['hedge_mw_non_nan']
        return profile

    @staticmethod
    def __hedge_per_product_table(profile:pd.DataFrame, product:Products):
        temp_df = profile.groupby('hedge_group').mean()
        temp_df.reset_index(inplace=True)
        
        if  product==Products.cal:
            temp_df['hedge_group'] = temp_df['hedge_group'].apply(lambda x: x.strftime('%F'))
        elif product==Products.q:
            temp_df['hedge_group'] = temp_df['hedge_group'].apply(lambda x: x.strftime('%F-Q%q'))
        
        return temp_df[['hedge_group', 'hedge_mw']].round({'hedge_mw' : 4})

    def __hedge_df_to_dict(self, hedge_products_table): 
        return hedge_products_table.to_dict('list')

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

    def calc_residual_with_hedges(self,hedges, profile):
        """Calculate the hourly residual profile based on an hedges object and return a HourProfile"""

        # generate timestamp
     
        HourProfile.create_timestamps()

        # generate hedges as profile


        # calcualte residual profile based on hedges an profile input
        
    
