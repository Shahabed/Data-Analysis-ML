#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Shahabedin Chatraee Azizabadi
"""
import numpy as np
import pickle
import functions_common
import pandas as pd
import time

def median_absolute_deviation(df):    
    # Formula: median ( abs( a - median(a)) )
    meds = df.median()
    diffs = df - meds
    res = diffs.abs().median()
    return res
    
def zscore(well_features, means, stds):
    x = (well_features - means)
    y = stds
    
    norms = np.zeros_like(x, dtype=float)
    norms.fill(np.inf) # Now, we will know that Inf means std was zero (division by zero)
    np.divide(x, y, where=y!=0, out=norms)    
      
    return norms

#==========================================================================

merge_all_results_folder = "/---/all-plate-well-features-combined"

if True: # Load aggregated per well values
    print("Loading aggregated data from file ...")    
    aggregated_data_df = pd.read_csv(merge_all_results_folder+'/plate_well_features_combined_for_percentile.csv')
    print("aggregated_data_df memory usage =", functions_common.get_dataframe_memory_usage(aggregated_data_df),'MB')

norm_func = zscore # can be any other function

if True: # NORMALIZATION LOOP --------------    
    # 1. Compute aggregate values per plate: ---------------
    aggregated_data_ref_vals = functions_common.get_reference_selection(aggregated_data_df)
    plate_means = aggregated_data_ref_vals.groupby('barcode').mean()
    plate_stds = aggregated_data_ref_vals.groupby('barcode').std()
    #test: plot_mean_vs_norm_scatter(mue, sigma, 'mue', 'sigma')
    # Were some plates discarded by filtering?: Compare barcodes of Agg-data vs from Agg-Ref-data
    if len(aggregated_data_ref_vals.barcode.unique()) != len(aggregated_data_df.barcode.unique()):
        print("WARNING! Number of barcoes is not equal between Agg-data and Agg-Reference-data")

    
    # 2. Compute something for wells per plate   ------------------
    print("Normalizing ...")
    start = time.time()

    per_plate_g = aggregated_data_df.groupby('barcode') # The loaded aggregated data. Indexes are ordinal numbers.
    barcodes = list(per_plate_g.groups.keys())
    
    all_indices = []
    all_zscores = None
    
    for barcode in barcodes:
        # Find wells of this plate and their agg values:
        #   Note: Below, we use only the values starting from the '2_percentile_ascspecks_AreaShape_Area' column onwards
        wells_features = per_plate_g.get_group(barcode).loc[:, '2_percentile_ascspecks_AreaShape_Area':]
                
        if barcode in plate_stds.index.values:
            # Get aggregate values of this plate, per each feature:
            means = plate_means.loc[barcode, '2_percentile_ascspecks_AreaShape_Area':]        
            stds = plate_stds.loc[barcode, '2_percentile_ascspecks_AreaShape_Area':]
            
            # Compute z-scores:
            #   Note: We convert to array before calculating, to speed up
            zscores = norm_func(wells_features.values, means.values, stds.values) # computes z-score values of all feature colums

            # Keep:
            #   array method:
            if all_zscores is None:
                all_zscores = zscores
            else:
                all_zscores = np.append(all_zscores, zscores, axis=0)
            all_indices = np.append(all_indices, wells_features.index.values, axis = 0)            
        else:
            print('WARNING! This plate(',barcode,') does not exist in reference means and stds')
    
    # How long did it take?
    print('Elapsed', round(time.time() - start, 2), 'seconds')
    
    # Convert to dataframe fomat
    per_well_results = pd.DataFrame(data=all_zscores, index=all_indices.astype(int), columns=wells_features.columns)
    normalized_data_df = aggregated_data_df.loc[:,'barcode':'treatment'].join(per_well_results, how='inner')
    
    # Save to file
    print("Saving to dat file ...") # Note: binary file is much faster
    with open(merge_all_results_folder+'/wells_zscore_vals.data', 'wb') as file:
        pickle.dump(normalized_data_df, file)
