#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:57:56 2020

@author: Shahabedin Chatraee Azizabadi
"""
import pandas as pd
import numpy as np
import os
import time
import functions_common
import pickle



def convert_features_df_to_dict(well_features_df, barcode, well_key, treatment):
    well_features_df['barcode'] = barcode
    well_features_df['well_key'] = well_key
    well_features_df['treatment'] = treatment
    a = well_features_df.set_index(keys=['barcode', 'well_key', 'treatment'])
    b = a.to_dict('index')
    return b
    
def convert_features_dict_to_df(plate_wells_features_dict):
    dft = pd.DataFrame.from_dict(plate_wells_features_dict, orient='index')
    a = dft.reset_index()
    b = a.rename(columns={'level_0':'barcode', 'level_1':'well_key', 'level_2':'treatment'})
    c = b.set_index(keys=['barcode', 'well_key', 'treatment'])
    return c


# --------------------------------------------------------------------

#folder_of_well_values = "/Users/chatraees/Desktop/test"
#folder_of_well_values = "G:\immunix_project\\Normalization\\Result"
folder_of_well_values = "/home/cellprofiler/Desktop/agg_result"


# --------------------------------------------------------------------
# Consider all the wells?
plate_wells = functions_common.get_join_table(filename = '../../immunx_meta/data/plate_based_screening_list.csv')
#plate_wells = functions_common.get_reference_selection(plate_wells )

# --------------------------------------------------------------------
merge_results_folder = './plate-well-features-combined'
if not os.path.exists(merge_results_folder):
    os.makedirs(merge_results_folder)

merge_all_results_folder = './all-plate-well-features-combined'
if not os.path.exists(merge_all_results_folder):
    os.makedirs(merge_all_results_folder)

# --------------------------------------------------------------------

time_started = time.time()

plates = (plate_wells.groupby('barcode').barcode.count().to_frame('well_count'))
print("Number of plates:", len(plates))


plates_to_process = plates # default: all the plates
#plates_to_process = plates[0:2] # TODO: just for test. Remove

test_list = []

# NOTE: Rough estimate of the size of well features of all plates combined
# 179*384*1500 * 8 / (10**6) = 825 MB for all plates  -->   4.6 MB per plate
#   Assumption:
#       Features are loaded as float64, therefore we assume 64/8 = 8 bytes per feature


# --- Algoritm ---:
#    for each plate:
#       for each well of current plate:
#           read the desired values from the well file
#           ...
#       combine-wells-of-current-plate
#    combine-...
plate_dict_for_percentile= dict()

# Loop per plate, and merge well values per plate
for plate in plates_to_process.itertuples():
    barcode = plate.Index
    
    try:
        print()
        print("Processing for plate with barcode =",barcode)
        
        wells_of_this_plate = plate_wells[plate_wells.barcode == barcode]
        
        plate_wells_features_dict_for_percentile = dict() # stores features of all wells of current plate
        #well_features_dict_for_median = dict()
        
        # collect values from all wells of this plate
        for well in wells_of_this_plate.itertuples():
            # Search for the well folder:
            # Assumptions for folder name pattern:
            # - ends with well-key
            # - there is at least one character between barcode and well-key
            well_file = functions_common.find_well_folder(folder_of_well_values, barcode, well.well_key+'*.csv')            
            #print("Well info:",barcode, "|", well.well_key)
            if well_file is not None: # If such well folder was found
                #print("Found well folder for well: ", barcode, "|", well.well_key)
                #print(well_folder)
                
                # Read ALL the feature columns from well files -------------:
                
                # Read mean values and merge
                
                percentiles=['2_percentile','25_percentile','50_percentile','75_percentile','98_percentile']
                c=dict()

                for per in percentiles:
                    well_features_per = functions_common.read_well_features_from_agg_results_quan(
                                                                well_file=well_file,
                                                                desired_agg_type=per)    
                    
                    
                
                    if not well_features_per.empty:
                        well_features_per = well_features_per.drop(columns=['agg_type'])                        
                        #Herein, we add a prefix, the name of percentile, to all column names
                        well_features_per=well_features_per.add_prefix(per+'_')
                        
                        # add to dict of this well
                        d = convert_features_df_to_dict(well_features_per, barcode, well.well_key, well.treatment)                        
                        if c == {}: # First time appending the columns
                            c.update(d)
                        else: # Append the columns horizontally to existing dict of current well 
                            main_key_of_current_dict = list(c.keys())[0]
                            c[main_key_of_current_dict].update(d[main_key_of_current_dict]) 



                # add to dict of this plate
                plate_wells_features_dict_for_percentile.update(c)
               
                        
                
                    
                # Read etc. and merge
                #   ...
                #   ...
            else:
                print("Well file NOT found for well: ", barcode, "|", well.well_key)
        # END OF LOOP THAT CREATES A DICT FOR EACH PLATE ==============================
        # Save features of all wells of current plate ----------------------
        if len(plate_wells_features_dict_for_percentile) > 0:
            dft = convert_features_dict_to_df(plate_wells_features_dict_for_percentile)
            #>>>>>Herein, we can drop the duplicated columns for each plate data frame<<<<<<<
            dft = dft.loc[:,~dft.columns.duplicated()]
            dft.to_csv(merge_results_folder+'/'+str(barcode)+'-percentile.csv')            
            plate_dict_for_percentile.update(plate_wells_features_dict_for_percentile)
            del dft
            test_list.append(plate_wells_features_dict_for_percentile) # SOME TEST:
        else:
            print("Nothing merged from wells percentile values of this plate")

        # -------------------------------------------------------------------------
    except Exception as e:
        print ("")
        print (">> Plate-loop FAILED at: ---------------------")
        print (">> barcode:", barcode)
        print ("exception: ", e)
        print ("")

# Save the big files!
a = convert_features_dict_to_df(plate_dict_for_percentile)
#>>>>>>>>To remove the duplicated values from the final dataframe
a = a.loc[:,~a.columns.duplicated()]
print("Saving to .dat file ...")
with open(merge_all_results_folder+'/plate_well_features_combined_for_percentile.data', 'wb') as file:
    pickle.dump(a, file)
print("Saving to .csv ...")
a.to_csv(merge_all_results_folder+'/plate_well_features_combined_for_percentile.csv')

time_end = time.time()
print("Elapsed", np.round(time_end-time_started, 2), "seconds")