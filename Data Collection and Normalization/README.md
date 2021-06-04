# Introduction:
# 1.Data Collection algorithm.py
The first algorithm to run is "Data Collection algorithm.py". This algorithm handles the complex database where the raw data(which is already aggregated) are stored. It collects and combine the separately stored sets of futures. These features-sets are stored separate directory and files based on their barcodes and well-keys. 
# 2.run_normalization.py
The normalization algorithm, "run_normalization.py", uses the collected and combined data as its input. The renown Z-score formula is used as a normalization method. 

# For the function zscore:
 # NOTE:
     When out=None, locations within the returned array where the condition is False will remain uninitialized,
     and therefore could lead to unexpected random values appearing in those locations!
     'uninitialized' here means it could be an unexpected random value

     Usual code:
     norms = (well_features - means) / stds
     This could have unexpected results depending on the numpy.errstate settings
     If the error handling setting is so, division by zero throws an exception
# 3.function_common.py
The "function_common" contains a set of function which are called in both above algorithms. 
