import pandas as pd
import matplotlib.pyplot as plt
from modules.enums import Values

class HourProfile:
    """Profile class stores any type of profile in hourly frequency"""

    def __init__(self, profile: pd.Series, name_val:Values=Values.mw, type='initial' ):
        self.name_val = name_val
        self.df_profile = profile.to_frame(name=name_val)
        self.type = type
        self.__set_col_peak_hours()
        self.__set_col_year_quarter_month()

    @staticmethod
    def create_timestamps(start_datetime: str, end_datetime: str):
        """From start to end the func returns a pandas DateTimeIndex in hourly frequency localized in Switzerland.
        datetime as 'YYYY-MM-DD HH:MM' """
        return pd.date_range(start=start_datetime, end=end_datetime, freq='H', tz='Europe/Zurich')

    @staticmethod
    def import_csv(file, sep=';', name_val:Values=Values.mw):
        """Imports a profile from csv file of type timestamp(hourly), values - no header -
        this returns a profile object"""
        # import the data from csv
        profile = pd.read_csv(file, sep=sep, header=None, names=['ts', name_val])

        # generate a datetime index based on the timestamp from csv
        start = profile.iloc[0][0]
        end = profile.iloc[-1][0]
        dtix = HourProfile.create_timestamps(start, end)

        # return profile object
        profile.drop(columns=['ts'], inplace=True)
        profile['ts'] = dtix
        profile.set_index('ts', inplace=True, drop=True)
        return HourProfile(profile=profile[name_val], name_val=name_val)

    def __set_col_peak_hours(self):
        def is_peak_hour(timestamp):
            return ((timestamp.hour >= 8) & (timestamp.hour < 20)) & (timestamp.weekday < 5)

        timestamps = self.df_profile.index.to_series(name='is_peak')
        self.df_profile = self.df_profile.merge(timestamps.apply(is_peak_hour).astype('bool'), left_index=True, right_index=True)

    def __set_col_year_quarter_month(self):
        self.df_profile['year'] = self.df_profile.index.year
        self.df_profile['quarter'] = self.df_profile.index.quarter
        self.df_profile['month'] = self.df_profile.index.month

    def get_hours_table(self):
        # returns base/peak/off-peak hours for Q's and Cal
        df = self.df_profile
        df['off_peak'] = ~df['is_peak']
        return pd.pivot_table(df, index=['quarter'], values=['is_peak', 'off_peak'], aggfunc='sum', margins = True, margins_name='Total')
    
    def get_sum_of_profile(self):
        return self.df_profile[self.name_val].sum().round(3)

    def display_head(self):
        self.df_profile.head(15)

    def plot_profile(self):
        self.df_profile.plot(y='mw')
        plt.show()

    def trim_date_to_other_hourProfile(self,other):
        start = other.df_profile.index[0]
        end = other.df_profile.index[-1]
        self.df_profile = self.df_profile.loc[start:end]
    
    def profile_to_csv(self):
        self.df_profile.to_csv('out.csv')

