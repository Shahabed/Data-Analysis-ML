#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 11:14:48 2020

@author: Shahabedin Chatraee Azizabadi
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt


def get_join_table(filename):
    tbl = pd.read_csv('../../---/--/plate_based_screening_list.csv')
    tbl.index = tbl['barcode']
    
    join_list = [] # List is much faster in loop appends comapred to DataFrame
    
    for index, row in tbl.iterrows():
        
        barcode = index
        donor = row['donor_1']
        
        layout_name = row['layout']
        layout_file_path = '../../----/data/layouts/'+layout_name+'.csv'
        # print ("For barcode "+barcode+". Reading from layout file: "+layout_file_path)
        layout = pd.read_csv(layout_file_path)
                
        # Each plate (each row from the main csv file) has several wells:
        for record in layout.itertuples():            
    
            well_key = record.well_key
            treatment = record.treatment
            
            # Join values from the two tables into one list
            join_list.append([barcode, donor, well_key, treatment])
    
    # make a datafarame from it
    col_names =  ['barcode', 'donor', 'well_key', 'treatment']
    join_table = pd.DataFrame(join_list, columns=col_names)
    return join_table
    

# Split the list into groups ----------------------------------------
def get_reference_selection(df):
    df_sel = (df[(df['treatment'] == 'sample_prim01_activ01') |
                 (df['treatment'] == 'ctrl_prim01_activ01_dmso')|
                 (df['treatment'] == 'ctrl_prim01_activ02_dmso')|
                 (df['treatment'] == 'sample_prim01_activ02') |
                 (df['treatment'] == 'ctrl_prim01_activ02') |
                 (df['treatment'] == 'ctrl_prim01_activ01')]).copy()
    
    return df_sel
    
#this groupby can be used later
#df_sel2=df_sel.groupby(['barcode'])

#df_sel2.describe()

# -----------------------------------------------
def find_well_folder(parent_folder, plate_barcode, well_key):
    # Search for the well folder:
    # Assumptions for folder name pattern:
    # - ends with well-key
    # - there is at least one character between barcode and well-key
    
    well_folder_pattern = '*' + plate_barcode + '?*' + well_key
    full_path_pattern = os.path.join(parent_folder, well_folder_pattern)        
    folders_found = glob.glob(full_path_pattern)
    
    # assumption: only one folder exists per each well
    if len(folders_found) > 0:
        return folders_found[0]
    else:
        return None

def read_well_features_from_agg_results(well_folder, desired_agg_type):
    
    try:        
        # load the features
        well_file = well_folder+'/aggregation_result.csv'        
        if os.path.exists(well_file):
            dfs = pd.read_csv(well_file)
        
            # fix some columns
            dfs.rename(columns={'Unnamed: 0':'agg_type'}, inplace=True)
            
            # select desired values
            selected_well_features = (dfs[dfs['agg_type'] == desired_agg_type]).copy()
            
            del dfs
            return selected_well_features            
        else:
            print("read_well_features_from_agg_results() WARNING: file does not exists:",well_file)
            return pd.DataFrame() # return an empty dataframe
    except Exception as e:
        print ("")
        print (">> read_well_features_from_agg_results():: FAILED ------------------------")
        print (">> well_folder:", well_folder)
        print ("exception: ", e)
        print ("")        
        return pd.DataFrame() # return an empty dataframe

# ==================================================================
#CHDPR01S01R01p01E01_A01_quantiles
def read_well_features_from_agg_results_quan(well_file, desired_agg_type):
    
    try:        
        # load the features        
        if os.path.exists(well_file):
            dfs = pd.read_csv(well_file)
        
            # fix some columns
            dfs.rename(columns={'Unnamed: 0':'agg_type'}, inplace=True)
            
            # select desired values
            selected_well_features = (dfs[dfs['agg_type'] == desired_agg_type]).copy()
            
            del dfs
            return selected_well_features            
        else:
            print("read_well_features_from_agg_results_quan() WARNING: file does not exists:",well_file)
            return pd.DataFrame() # return an empty dataframe
    except Exception as e:
        print ("")
        print (">> read_well_features_from_agg_results_quan():: FAILED ------------------------")
        print (">> well_file:", well_file)
        print ("exception: ", e)
        print ("")        
        return pd.DataFrame() # return an empty dataframe










# ==================================================================
def get_dataframe_memory_usage(data):
    return round(data.memory_usage(deep=True).sum()/(2**20)) # assume 1 MB = 1024 KBs, etc.


def pandas_groupby_to_list(groups, att_name):
    vals_list = []
    keys_list = []
    for key, vals in groups:
        vals_list.append(vals[att_name].values)
        keys_list.append(key)
    return keys_list, vals_list

# ==================================================================
# ==================================================================

def set_plot_style(labels_font_size = 10, tightlayout=True):
    plt.rcParams["figure.autolayout"] = tightlayout 
    plt.rcParams['font.size'] = labels_font_size
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['axes.labelsize'] = labels_font_size
    plt.rcParams['axes.labelweight'] = 'bold'


def add_boxplot_legend(boxplots, legend_labels, fontsize=10, location='best'):
    legend_artists = []
    for bplot in boxplots:
        legend_artists.append(bplot['boxes'][0])
    plt.legend(legend_artists, legend_labels,
               prop={'size':fontsize, 'weight':'bold'}, loc=location, framealpha=0.5)    
