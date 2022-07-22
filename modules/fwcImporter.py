import pandas as pd
from modules.profile import *

class PriceCurve():
    def import_chmpk_in_ch(file_path:str) -> HourProfile:
        """Convert CHMPK in EUR to CHF from the Sammlerexport.csv file located at the sharepoint url
        file_path: path to the sammlerexport csv
        year: the year to extract from Sammlerexport.csv
        """
        
        # Import FWCs
        col_name_time = 'Timestamp (DD.MM.YYYY HH:mm)'
        df_fwc = pd.read_csv(file_path)
        df_fwc.dropna(inplace=True)

        ## eigener Zeitstempel generieren
        time_col = 'Timestamp (DD.MM.YYYY HH:mm)'
        dtix = HourProfile.create_timestamps(start_datetime=df_fwc[time_col].iloc[0], end_datetime=df_fwc[time_col].iloc[-1])
        df_fwc.set_index(dtix,inplace=True)

        ## calculate FWC CHMPF CHF
        df_fwc['chmpk_chf'] = df_fwc['CHMPK (EUR/MWh)'] * df_fwc['FX (CHF/EUR)']

        # FWC CHMPK EUR as Profile 
        df_for_profile = df_fwc['chmpk_chf'].to_frame()
        return HourProfile(profile=df_for_profile['chmpk_chf'], name_val=Values.chf, type='CHMPK_EUR')

