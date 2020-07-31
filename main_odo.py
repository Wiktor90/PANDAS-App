import os
import pandas as pd
import numpy as np
from dk_odo import odometers_dk
from gb_odo import odometers_gb
from template_odo import template

path_dk = 'C:\\Users\\PL9891\\Desktop\\Fleet\\FUEL_FILES_TO_TRANSFORM\\DK_temp_save\\'
path_gb = 'C:\\Users\\PL9891\\Desktop\\Fleet\\FUEL_FILES_TO_TRANSFORM\\GB_temp_save\\'
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
    dataframe.to_excel(excelWriter, index=False, startrow=6)
    excelWriter.save()


print("What country is this fuel file from ?")
print("Choose the Country Code:")
countries =['DK','GB',]

for n,country in enumerate((countries),1):
    print("{}.{}".format(n,country))
choice = input("Country: ").lower()
# run particular script depends on choice variable
if choice == "dk":
    directory = list_all_files(path_dk)
    for i in directory:
        df = odometers_dk(i[0],i[1])
        new_file = 'RTI_'+ i[1] # file name with corrected data frame.
        save_excel(convert_file_path, new_file, df)
        template(convert_file_path, new_file)
        print('{} - formating COMPLETE'.format(i[1]))

elif choice == "gb":
    directory = list_all_files(path_gb)
    for i in directory:
        df = odometers_gb(i[0],i[1])
        new_file = 'RTI_'+ i[1] # file name with corrected data frame.
        save_excel(convert_file_path, new_file, df)
        template(convert_file_path, new_file)
        print('{} - formating COMPLETE'.format(i[1]))
else:
    print("Country Code: {} - not found!".format(choice))

    
