# The goal of the classification:
* Classification of adverse reactions. We want to predict, based on our feature set, what adverse reaction (ADR) or category of adverse reaction each drug results in. 
# Introduction:
The first attempt is to binary classify the drug (or chemical compound) based on the feature set, collected from the screening data. The drug’s  possible reactions will be classified in six categories of ADRs, one can predict a drug belongs (or do not belong) to a category of ADR. 
The second approach is to use multiclass classification methods. Here again, we use the six categories of ADR and predict in which category of ADR a drug's reactions might belong. The description of the multiclass approach is described in a separate README. 

# 1. Classification algorithm_binary
Three functions are defined in this script. The functions `naive_bay`and `Binary_sup_vec_machine`are two classification models that we use here. The function 
`other_eval_methods` is for the additional  evaluation metrics which can be used for the above classification models. These additional metrics give a better insight to the performance of the classifier. The algorithm `additional_functions_for_binary` is also called in for the other useful functions that is used here. 
# 2. Additional  function for the binary classification
The first function is `import_ADRs_list` that can be used to import a list of categorize ADRs which can later be set as a threshold. The function `binary_column` is defined to add a binary column as the label vector based on the ADRs_list. For the spliting of the data to the train/test , the splitting  of the design matrix and the label vector, the `spliting_for_classifier` is defined. Finally, for plotting  the confusion matrix based on different classifiers which is given as input,`plot_confusion_matrix` is provided. 

# 3. manifold_learning
The function `VIF_computation` is developed for the computation of the variance inflation factor. It has a purpose to find high level of multicollinearity between independent variables (the set of features). Four functions, `KPCA_al`,`PCA_al`,`isomap_al`and`local_lin_embed` are defined representing four different manifold learning methods.   

# 4. k_fold_cross_validation
Herein, there is a function `cross_va_scor`that gives a general score of cross- validation for the binary support  vector machine (SVM). the main function is 
`k_fold_cross`, which designed to calculated the classification metrics for each fold.
