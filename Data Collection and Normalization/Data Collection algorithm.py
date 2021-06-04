# -*- coding: utf-8 -*-
"""
@author: Shahabedin Chatraee Azizabadi
"""

import pandas as pd
import numpy as np
import os
import time
import functions_common
import pickle


def convert_features_dict_to_df(plate_wells_features_dict):
    dft = pd.DataFrame.from_dict(plate_wells_features_dict, orient='index')
    a = dft.reset_index()
    b = a.rename(columns={'level_0':'barcode', 'level_1':'well_key', 'level_2':'treatment'})
    c = b.set_index(keys=['barcode', 'well_key', 'treatment'])
    return c

def convert_features_df_to_dict(well_features_df, barcode, well_key, treatment):
    well_features_df['barcode'] = barcode
    well_features_df['well_key'] = well_key
    well_features_df['treatment'] = treatment
    a = well_features_df.set_index(keys=['barcode', 'well_key', 'treatment'])
    b = a.to_dict('index')
    return b
    
# --------------------------------------------------------------------
folder_of_well_values = "../../result"
# --------------------------------------------------------------------
# Here, we consider all the wells
plate_wells = functions_common.get_join_table(filename = '../../--/--/plate_based_screening_list.csv')
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


plates_to_process = plates # The default is for all the plates


test_list = []

plate_dict_for_mean = dict()
plate_dict_for_ask = dict()
plate_dict_for_tnfa = dict()

# Loop per plate, and merge well values per plate
for plate in plates_to_process.itertuples():
    barcode = plate.Index
    
    try:
        print()
        print("Processing for plate with barcode =",barcode)
        
        wells_of_this_plate = plate_wells[plate_wells.barcode == barcode]
        
        plate_wells_features_dict_for_mean = dict() # stores features of all wells of current plate
        plate_wells_features_dict_for_ask = dict()
        plate_wells_features_dict_for_tnfa = dict()
        #well_features_dict_for_median = dict()
        
        # collect values from all wells of this plate
        for well in wells_of_this_plate.itertuples():
            # Search for the well folder:
            # Assumptions for folder name pattern:
            # - ends with well-key
            # - there is at least one character between barcode and well-key
            well_folder = functions_common.find_well_folder(folder_of_well_values, barcode, well.well_key)
            #print("Well info:",barcode, "|", well.well_key)
            if well_folder is not None: # If such well folder was found
                #print("Found well folder for well: ", barcode, "|", well.well_key)
                #print(well_folder)
                
                # Read ALL the feature columns from well files -------------:
                
                # Read mean values and merge
                well_features_mean = functions_common.read_well_features_from_agg_results(
                                                            well_folder=well_folder, 
                                                            desired_agg_type='mean')
                if not well_features_mean.empty:
                    # add to dict of this plate
                    d = convert_features_df_to_dict(well_features_mean, barcode, well.well_key, well.treatment)
                    plate_wells_features_dict_for_mean.update(d)
                    
                #read ask positive rate values    
                well_features_ask_rate = functions_common.read_positive_rates_from_agg_results(
                                                            well_folder=well_folder, 
                                                            desired_agg_type='ask_positive_rate')
                if not well_features_ask_rate.empty:
                    # add to dict of this plate
                    w = convert_features_df_to_dict(well_features_ask_rate, barcode, well.well_key, well.treatment)
                    plate_wells_features_dict_for_ask.update(w)
                    
                #read Tnfa positive rate values
                well_features_tnfa_rate = functions_common.read_positive_rates_from_agg_results(
                                                            well_folder=well_folder, 
                                                            desired_agg_type='tnfa_positive_rate')
                if not well_features_tnfa_rate.empty:
                    # add to dict of this plate
                    v = convert_features_df_to_dict(well_features_tnfa_rate, barcode, well.well_key, well.treatment)
                    plate_wells_features_dict_for_tnfa.update(v)     
                # Read etc. and merge
                #   ...
                #   ...
            else:
                print("Well folder NOT found for well: ", barcode, "|", well.well_key)
        # END OF LOOP THAT CREATES A DICT FOR EACH PLATE ==============================
        # Save features of all wells of current plate ----------------------
        if len(plate_wells_features_dict_for_mean) > 0:
            dft = convert_features_dict_to_df(plate_wells_features_dict_for_mean)
            dft.to_csv(merge_results_folder+'/'+str(barcode)+'-mean.csv')            
            plate_dict_for_mean.update(plate_wells_features_dict_for_mean)
            del dft
            test_list.append(plate_wells_features_dict_for_mean) # SOME TEST:
        else:
            print("Nothing merged from wells mean values of this plate")
        
        #===============================================================
        if len(plate_wells_features_dict_for_ask) > 0:
            dft = convert_features_dict_to_df(plate_wells_features_dict_for_ask)
            dft.to_csv(merge_results_folder+'/'+str(barcode)+'-ask_positive.csv')            
            plate_dict_for_ask.update(plate_wells_features_dict_for_ask)
            del dft
            
        else:
            print("Nothing merged from wells ask_positive values of this plate")
        #=============================================================================
        if len(plate_wells_features_dict_for_tnfa) > 0:
            dft = convert_features_dict_to_df(plate_wells_features_dict_for_tnfa)
            dft.to_csv(merge_results_folder+'/'+str(barcode)+'-tnfa_positive.csv')            
            plate_dict_for_tnfa.update(plate_wells_features_dict_for_tnfa)
            del dft
            
        else:
            print("Nothing merged from wells tnfa_positive values of this plate")

        # -------------------------------------------------------------------------
    except Exception as e:
        print ("")
        print (">> Plate-loop FAILED at: ---------------------")
        print (">> barcode:", barcode)
        print ("exception: ", e)
        print ("")

# Save the big files!
a = convert_features_dict_to_df(plate_dict_for_mean)
b = convert_features_dict_to_df(plate_dict_for_ask)

b.rename(columns={'rates':'ask_positive_rates'}, inplace=True)
c = convert_features_dict_to_df(plate_dict_for_tnfa)

c.rename(columns={'rates':'tnfa_positive_rates'}, inplace=True)
#========================================================================================================
# In the case we want to add the positive rates to the result.
#result = pd.merge(a,b['ask_positive_rates'],c['tnfa_positive_rates'])
#To save data as binary form
print("Saving to .data file ...")
with open(merge_all_results_folder+'/plate_well_features_combined_for_mean.data', 'wb') as file:
    pickle.dump(a, file)
print("Saving to .csv ...")
a.to_csv(merge_all_results_folder+'/plate_well_features_combined_for_mean2.csv')

time_end = time.time()
print("Elapsed", np.round(time_end-time_started, 2), "seconds")
