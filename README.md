# Data-Analysis and ML
Herein, the state of the art algorithems for different aspect of data analysis and ML are presented. 
# Introduction:
## 1.Data Collection algorithm.py
The first algorithm to run is "Data Collection algorithm.py". This algorithm handles the complex database where the raw data(which is already aggregated) are stored. It collects and combine the separately stored sets of futures. These features-sets are stored separate directory and files based on their barcodes and well-keys. 
## NOTE: 
    Rough estimate of the size of well features of all plates combined
    179*384*1500 * 8 / (10**6) = 825 MB for all plates  -->   4.6 MB per plate
    Assumption:
    Features are loaded as float64, therefore we assume 64/8 = 8 bytes per feature


    # --- Algoritm ---:
    #    for each plate:
    #       for each well of current plate:
    #           read the desired values from the well file
    #           ...
    #       combine-wells-of-current-plate
    #    combine-...
## 2.run_normalization.py
The normalization algorithm, "run_normalization.py", uses the collected and combined data as its input. The renown Z-score formula is used as a normalization method. 

## For the function zscore:
 ## NOTE:
     When out=None, locations within the returned array where the condition is False will remain uninitialized,
     and therefore could lead to unexpected random values appearing in those locations!
     'uninitialized' here means it could be an unexpected random value

     Usual code:
     norms = (well_features - means) / stds
     This could have unexpected results depending on the numpy.errstate settings
     If the error handling setting is so, division by zero throws an exception
## 3.function_common.py
The "function_common" contains a set of functions which are called in both above algorithms. 
