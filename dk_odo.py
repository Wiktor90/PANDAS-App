import os
import pandas as pd
import numpy as np

#ODO correction
def odometers_dk(path="", filename=""):
    #dawnload / cleam / prepare df from dir
    df = pd.read_excel(os.path.join(path,filename))

    #split date and time
    date_split = df['Dato'].str.split(" ",1)
    df['Date']=date_split.str.get(0)
    df['Time']=date_split.str.get(1)
    
    #split registration number and finance id. Registration num. will be an index.
    kort_split = df['Kort tekst linje 2'].str.split(' ',1)
    df['VEHICLE_ID_FW']=kort_split.str.get(1)
    df['VEHICLE_ID_FW'].str.replace(" ","") # fixing unnecessary spaces between registration nummbers

    #cleacing df + removing stupid values
    del df['Dato']
    del df['Chauffør']
    del df['Køretøj']
    del df['Kort tekst linje 2']
    df.dropna(inplace = True)
    df['Odometer'] = df['Odometer'].apply(lambda x: 0 if x <1000 else x) # stupid values
    #sorting / set index
    df.sort_values(by=['VEHICLE_ID_FW','Date','Time'], ascending=[True,False,False],inplace=True)
    df.set_index(['VEHICLE_ID_FW'], inplace=True)
    #create of unique Vehicle IDs list
    ids = df.index.unique().tolist()
    #create new df to store corrected data from dawnloaded df
    df_corrected = pd.DataFrame()

    #odo correction and storing data in df_corrected
    for i in ids:
        temp_df = df.loc[i]
        odo = df.loc[i,"Odometer"].tolist()
        
        if type(odo) == list:
            odo.sort(reverse=True)
        
            for j in range(len(odo)-1):
                if odo[j] - odo[j+1] > 9999 and odo[j+1] != 0:
                    odo[j+1] = 0
                
            temp_df.loc[:,"Odometer"] = odo #temp_df["ODOMETER_FW"] = odo
            df_corrected = df_corrected.append(temp_df)
    
        else:
            df_corrected = df_corrected.append(temp_df)

    df_corrected.index.name = "VEHICLE_ID_FW"
    return df_corrected

if __name__ == "__main__":
    odometers_dk()