import numpy as np
import pandas as pd

from modules.enums import *
from modules.profile import HourProfile
from modules.tradingProduct import TradingProduct 


class Hedging:
    def __init__(self, to_hedge_profile: HourProfile):
        self.initial_hourProfile = to_hedge_profile
        self.__rename_val_col_to_mw()
        self.hedge_product_selection = []
        self.hedge_products_list = []
        self.hedge_timeseries_df = []
        
    def calc_quantity_hedges(self, product=Products.cal, hour=Hours.base) -> list:
        """Calculate a quantity hedge base on the profile - product eg. 'Cal' and hours eg. 'Peak' """
        
        # initialies a onw list entry with all the relevant timeseries for the upcoming hedge.
        self.hedge_product_selection.append(f'{product} {hour}')
        profile = self.initial_hourProfile.df_profile.copy()

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
        hedges = self.to_list_of_trading_products(profile=profile, product=product, hour=hour)
        self.hedge_products_list.extend(hedges)
        
        # calculation residual profil
        profile = self.__calc_residual_profile(profile=profile)

        # store the timeseries df
        self.hedge_timeseries_df.append(profile)

        # return the hedge table as df
        return hedges

    def combinations_of_quantity_hedge(self, base_product:Products=Products.none, peak_product:Products=Products.none):
        hedges_list_combinations = []

        # only base
        if base_product and not peak_product:
            hedges = self.calc_quantity_hedges(product=base_product, hour=Hours.base)
            hedges_list_combinations.extend(hedges)

        # only peak
        elif not base_product and peak_product:
            hedges = self.calc_quantity_hedges(product=peak_product, hour=Hours.peak)
            hedges_list_combinations.extend(hedges)

        # base and peak products
        if base_product and peak_product:
            # the base hedge is set to the off-peak quantity
            hedges_base = self.calc_quantity_hedges(product=base_product, hour=Hours.off_peak)
            for hedge in hedges_base:
                hedge.set_type(Hours.base) 
            hedges_list_combinations.extend(hedges_base)
 
            # peak quantity calculation
            hedges_peak = self.calc_quantity_hedges(product=peak_product, hour=Hours.peak)

            for index, hedge_peak in enumerate(hedges_peak):
                # same duration of products i.e both cal or both q
                if base_product == peak_product:
                # substract base from peak hedge 
                    hedge_peak.set_mw(hedge_peak.trading_product_minus_other(hedges_base[index]))
               
            
                # base in cal and peak in q 
                if base_product==Products.cal and peak_product==Products.q:
                    # peak hedges are the calculated peak hedges minus the cal base hedge
                    hedge_peak.set_mw(hedge_peak.trading_product_minus_other(hedges_base[0]))

            hedges_list_combinations.extend(hedges_peak)

        return hedges_list_combinations

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
            period = profile.index.to_period('Y')
        elif product == Products.q:
            period = profile.index.to_period('Q')
        elif product == Products.m:
            period = profile.index.to_period('M')

        profile['hedge_group'] = period
        profile['start'] = period.to_timestamp(how='start')
        profile['end'] = period.to_timestamp(how='end')
        
        return profile

    @staticmethod
    def __calc_residual_profile(profile:pd.DataFrame):
        profile['residual'] = profile['mw'] - profile['hedge_mw_non_nan']
        return profile


    def to_list_of_trading_products(self, profile:pd.DataFrame, product:Products, hour:Hours):
        # profile DF gruppieren und aus den einzelnen Gruppen ein Hedge object herstellen
        temp_df_grouped = profile.groupby('hedge_group')
        
        out_list = []

        for name, group in temp_df_grouped:

            out_list.append(TradingProduct(
                type=hour, 
                mw=group['hedge_mw'].mean().round(2), # round to 2 digits 
                start=group['start'].iloc[0].strftime('%Y-%m-%d %H:00'), 
                end= group['end'].iloc[0].strftime('%Y-%m-%d %H:00')))
        return out_list

    def initial_profile_minus_all_hedges(self) -> tuple:
        """ 
        returns an tupple of HourProfile of calculated as the initial profile minus all hedges.
        first element: profile with positive and negative values
        second element: the profile with the positiv values
        third element: the negative values of the profile transformed to positiv values  
        """
        
        list_of_df = []
        for trading_product in self.hedge_products_list:
            list_of_df.append(trading_product.generateProfile().df_profile)
            concated = pd.concat(list_of_df, axis=1)
        
        if len(self.hedge_products_list) >1:
            summed_hedge_profile = concated['mw'].sum(axis=1)
        else:
            summed_hedge_profile = concated['mw']

        res = (self.initial_hourProfile.df_profile['mw'] - summed_hedge_profile).to_frame(name='mw')
        pos = res['mw'] > 0
        
        res['pos'] = res['mw']
        res['pos'].loc[~pos] = 0
        
        res['neg'] = res['mw']
        res['neg'].loc[pos] = 0
        res['neg'] = res['neg'].abs()

        return (
            HourProfile(profile=res['mw'], name_val=Values.mw, type='residual_all'),
            HourProfile(profile=res['pos'], name_val=Values.mw, type='residual_pos'),
            HourProfile(profile=res['neg'], name_val=Values.mw, type='residual_neg'),
        )

    def print_all_mwh_of_residual(self):
        res_profiles = self.initial_profile_minus_all_hedges()
        for pro in res_profiles:
            print(f'{pro.type} with {pro.get_sum_of_profile()} Mwh')

    def print_hedges(self):
        for trading_prod in self.hedge_products_list:
            print(trading_prod)

    def clear_previous_hedges(self):
        self.hedge_product_selection = []
        self.hedge_products_list = []
        self.hedge_timeseries_df = []

    def __rename_val_col_to_mw(self):
        rename = {
            self.initial_hourProfile.name_val : 'mw'
        }
        self.initial_hourProfile.df_profile.rename(columns=rename, inplace=True)
        self.initial_hourProfile.name_val = 'mw'
