# The goal of the classification:
* Classification of adverse reactions. We want to predict, based on our feature set, what adverse reaction (ADR) or category of adverse reaction each drug result in or belongs to. 
# Introduction:
The first attempt is to binary classify the drug (or chemical compound) based on the feature set, collected from the screening data. The drug’s  possible reactions will be classified in six categories of ADRs, one can predict a drug belongs (or do not belong) to a category of ADR. 
The second approach is to use multiclass classification methods. Here again, we use the six categories of ADR and predict in which category of ADR a drug's reactions might belong.
