import pandas as pd
import json
from modules.enums import *
from modules.profile import HourProfile

class TradingProduct():
    def __init__(self, type:Hours, start:str, end:str, mw:float):
        """ Generates from the input below a pandas Dataframe timeseries with timestamp as index, is_peak and mw values columns according to the specified type.

            'type': String 'base' or 'peak' or 'off-peak'
            'start': String in format 'YYYY-MM-DD HH:MM',
            'end': String in format 'YYYY-MM-DD HH:MM',
            'mw' : Float, """

        self.info = {
            'type': type,
            'start': start,
            'end': end,
            'mw' : mw,
        }

    def change_type(self, type:Hours):
        self.info['type'] = type

    def change_mw(self, mw:float):
        self.info['mw'] = mw

    def trading_product_minus_other(self, other):
        return (self.info['mw'] - other.info['mw']).round(2)

    def generateProfile(self):
        ts = pd.date_range(start=self.info['start'], end=self.info['end'], freq='H', tz='Europe/Zurich')
        df = ts.to_series(name='is_peak').apply(self.__is_peak_hour).astype('bool').to_frame()
        df['mw'] = self.info['mw']
        
        if type == Hours.peak:
            df.loc[df['is_peak']== False,'mw'] = 0
        if type == Hours.off_peak:
            df.loc[df['is_peak']== True,'mw'] = 0
        
        return HourProfile(profile=df , type=self.info['type'])

    def get_mwh(self):
        profile = self.generateProfile()
        return profile.df_profile['mw'].sum().round(3)

    def __str__(self) -> str:
        return json.dumps(self.info)

    def __eq__(self, other):
        return self.info == other.info
    
    @staticmethod
    def __is_peak_hour(timestamp):
            return ((timestamp.hour >= 8) & (timestamp.hour < 20)) & (timestamp.weekday < 5)


