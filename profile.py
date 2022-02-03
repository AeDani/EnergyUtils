import pandas as pd
import numpy as np


class Profile:
    """Profile class stores any type of profile in hourly frequency"""

    @staticmethod
    def create_timestamps(start_datetime:str, end_datetime:str):
        """From start to end the func returns a pandas DateTimeIndex in hourly frequency localized in Switzerland.
        datetime as 'YYYY-MM-DD HH:MM' """
        return pd.date_range(start=start_datetime, end=end_datetime, freq='H', tz='Europe/Zurich')

    @staticmethod
    def import_csv(file, sep=';'):
        """Imports a profile from csv file of type timestamp(hourly), values - no header - this returns a profile object"""
        # import the data from csv
        profile = pd.read_csv(file, sep=sep, header=None, names=['ts','mw'])

        # generate a datetime index based on the timestamp from csv
        start = profile.iloc[0][0]
        end = profile.iloc[-1][0]
        dtix = Profile.create_timestamps(start, end)

        # return profile object
        profile.drop(columns=['ts'], inplace=True)
        profile['ts'] = dtix
        profile.set_index('ts', inplace=True, drop=True)
        return Profile(profile)


    def __init__(self, profile: pd.DataFrame):
        self.df_profile = profile

