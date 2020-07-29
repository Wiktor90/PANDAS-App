import os
import pandas as pd
import numpy as np

print("What country is this fuel file from ?")
print("Choose the Country Code:")
countries =['DK','GB',]

for n,country in enumerate((countries),1):
    print("{}.{}".format(n,country))

choice = input("Country: ")