import pandas as pd
from modules.profile import *

##------ Preparation of FWCs

# Import FWCs
file='Assets/20220715Sammlerexport.csv'
col_name_time = 'Timestamp (DD.MM.YYYY HH:mm)'

df_fwc = pd.read_csv(file)
df_fwc.dropna(inplace=True)

## eigener Zeitstempel generieren
time_col = 'Timestamp (DD.MM.YYYY HH:mm)'
dtix = HourProfile.create_timestamps(start_datetime=df_fwc[time_col].iloc[0], end_datetime=df_fwc[time_col].iloc[-1])
df_fwc.set_index(dtix,inplace=True)
# Start and End for all timeseries
df_fwc = df_fwc.loc['2023-01-01 00:00':'2023-12-31 23:00']

## calculate FWC CHMPF CHF
df_fwc['chmpk_chf'] = df_fwc['CHMPK (EUR/MWh)'] * df_fwc['FX (CHF/EUR)']

# FWC CHMPK EUR as Profile 
df_for_profile = df_fwc['chmpk_chf'].to_frame()
chmpk_chf = HourProfile(profile=df_for_profile,type='CHMPK_EUR')




