"""
Created Dec 2025 by Jillian Hesler
"""
import pandas as pd

#Define preprocessing as a function
def preprocess(filepath):
    df = pd.read_excel(filepath, parse_dates=True) 
    return df
  
#Call preprocessing function on desired data
preprocess("E:\Python\DataExplorerPackage\exppack\data\data.xlsx")    
