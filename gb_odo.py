import os
import pandas as pd
import numpy as np

#ODO correction
def odometers_gb(path="", filename=""):
    #dawnload / cleam / prepare df from dir
    df = pd.read_excel(os.path.join(path,filename), skiprows=6)
    df.loc[:,"ODOMETER_FW"] = df.loc[:,"ODOMETER_FW"].fillna(0).astype('int')
    df.dropna(inplace = True)
    df.sort_values(by=['VEHICLE_ID_FW','TRANSACTION_DATE_FW','TRANSACTION_TIME_FW'], ascending=[True,False,False],inplace=True)
    df['ODOMETER_FW'] = df['ODOMETER_FW'].apply(lambda x: 0 if x <1000 else x)

    #create of unique Vehicle IDs list
    ids = df.index.unique().tolist()
    #create new df to store corrected data from dawnloaded df
    df_corrected = pd.DataFrame()

    #odo correction and storing data in df_corrected
    for i in ids:
        temp_df = df.loc[i]
        odo = df.loc[i,"ODOMETER_FW"].tolist()
        
        if type(odo) == list:
            odo.sort(reverse=True)
        
            for j in range(len(odo)-1):
                if odo[j] - odo[j+1] > 9999 and odo[j+1] != 0:
                    odo[j+1] = 0
                
            temp_df.loc[:,"ODOMETER_FW"] = odo #temp_df["ODOMETER_FW"] = odo
            df_corrected = df_corrected.append(temp_df)
    
        else:
            df_corrected = df_corrected.append(temp_df)

    return df_corrected

if __name__ == '__main__':
    odometers_gb()


