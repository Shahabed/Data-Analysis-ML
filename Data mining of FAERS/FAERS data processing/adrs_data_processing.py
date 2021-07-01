#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 15:26:11 2020

@author: Shahabedin Chatraee Azizabadi

The data from FDA for adverse drug reactions needs preprocessing. Here, the necessary algorithm for this process is provided.
"""
import pandas as pd
import numpy as np
import time
import csv
import functions_set


# reading the FAERS data

df_drug=pd.read_csv('/drug.csv')
#>>>>>>>>>>>>>>>> head=dft.head(Number of rows from top)   This function,head(), can be used to pick up some rows from the top of the data frame.
#Should be disabled if one wants the whole dataframe
df_demographic=pd.read_csv('/demographic.csv')#.head(5000)
df_reaction=pd.read_csv('/reaction.csv',sep = '\t')
#<<<<<<<<<<<<<-------------------------.......,,,,,,,,,,,,,,,,,,,,,,,,---------------------------------------------------------------------------
time_started = time.time()

# ****Finding the  corrupted lines that causes the problem in the reading of csv, to run it******* turn False>>>>True*****
if False: 
    file = '/reaction.csv' # use your filename
    lines_set = set([100, 200]) # use your bad lines numbers here
    
    with open(file) as f_obj:
        for line_number, row in enumerate(csv.reader(f_obj)):
            if line_number > max(lines_set):
                break
            elif line_number in lines_set: # put your bad lines numbers here
                print(line_number, row)
#>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#finding the unique drug names and reaction names 
df_unique_drug=df_drug['drugname'].unique()
df_unique_reaction=df_reaction['pt'].unique()
#<<<<<<<<<<<<>>>>>>>>>>><<<<<<<<>>>>>>>>>><<<<<<<<<>>>>>>>>>>
#Creating the connected dataframe
a=functions_set.ADR_data_connector(df_demographic,df_drug,df_reaction)
a.to_csv('test_dataframe_result.csv')


time_end = time.time()
print("Elapsed", np.round(time_end-time_started, 2), "seconds")
