import pandas as pd

class ProfileGenerator():
    def __init__(self, type:str, start:str, end:str, mw:float):
        """ {
            'type': 'base',
            'start': 'YYYY-MM-DD HH:MM',
            'end': 'YYYY-MM-DD HH:MM',
            'mw' : 5,
        } """

        self.info = {
            'type': type,
            'start': start,
            'end': end,
            'mw' : mw,
        }

        self.df = self.generateProfile(type ,start, end, mw)

    def generateProfile(self,type ,start, end, mw):
        ts = pd.date_range(start=start, end=end, freq='H', tz='Europe/Zurich')
        df = ts.to_series(name='is_peak').apply(self.__is_peak_hour).astype('bool').to_frame()
        df['mw'] = mw
        
        if type == 'peak':
            df.loc[df['is_peak']== False,'mw'] = 0
        if type == 'off-peak':
            df.loc[df['is_peak']== True,'mw'] = 0
        
        return df
        
    
    @staticmethod
    def __is_peak_hour(timestamp):
            return ((timestamp.hour >= 8) & (timestamp.hour < 20)) & (timestamp.weekday < 5)



a = ProfileGenerator('base', '2022-01-03 00:00', '2022-01-03 23:00', 5)
print(a.df.head(10))

