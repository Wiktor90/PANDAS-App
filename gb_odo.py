import os
import pandas as pd
import numpy as np

path = 'C:\\Users\\PL9891\\Desktop\\Fleet\\FUEL_FILES_TO_TRANSFORM\\GB_temp_save\\'
convert_file_path= 'C:\\Users\\PL9891\\Desktop\\Fleet\\FUEL_FILES_TO_TRANSFORM\\RTI\\'

#RETURN LIST: [PATH, FILE NAME] (.xlsx in DIR)
def list_all_files(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.xlsx' in file:
                tuple_row = (r,file)
                files.append(tuple_row)

    return files

#SAVING NEW EXCLE FILE (corrected)
def save_excel(path, filename, dataframe):
    excelWriter = pd.ExcelWriter(path + filename)
    dataframe.to_excel(excelWriter, index=False)
    excelWriter.save()

#ODO correction
def odometers(path, filename):
    #dawnload / cleam / prepare df from dir
    df = pd.read_excel(os.path.join(path,filename), skiprows=6)
    df.loc[:,"ODOMETER_FW"] = df.loc[:,"ODOMETER_FW"].fillna(0).astype('int')
    df.dropna(inplace = True)
    df.sort_values(by=['VEHICLE_ID_FW','TRANSACTION_DATE_FW','TRANSACTION_TIME_FW'], ascending=[True,False,False],inplace=True)
    df['ODOMETER_FW'] = df['ODOMETER_FW'].apply(lambda x: 0 if x <1000 else x)
    df.set_index(['VEHICLE_ID_FW'], inplace=True)

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

    df_corrected.index.name = "VEHICLE_ID_FW"
    #saving corrected df to excel in corrected_file_path dir. Name of corrected file
    corected_file = 'RTI_'+ filename
    save_excel(convert_file_path, corected_file, df_corrected)

directory = list_all_files(path)
for i in directory:
    odometers(i[0],i[1])
    print(i[1],' - formating COMPLETE')
