import pandas as pd
import numpy as np


class Profile:
    @staticmethod
    def random_profile(start_datetime, end_datetime):
        date_index = Profile.create_timestamps(start_datetime, end_datetime)
        values = pd.Series(np.random.randint(low=0, high=500, size=len(date_index)))
        return Profile(date_index[0], values)

    @staticmethod
    def create_timestamps(start_datetime, end_datetime):
        return pd.date_range(start=start_datetime, end=end_datetime, freq='H', tz='Europe/Zurich')

    def __init__(self, start_datetime, values: pd.Series):
        self.start_datetime = start_datetime
        self.values = values



