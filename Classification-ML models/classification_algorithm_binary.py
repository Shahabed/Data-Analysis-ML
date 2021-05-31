#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:11:17 2020

@author: Shahabedin chatraee Azizabadi
The binary classifier: Naive Bayes and SVM
"""

import pandas as pd
import numpy as np
import additional_functions_for_binary
from sklearn import naive_bayes
from sklearn import svm
from sklearn.preprocessing import LabelEncoder,MinMaxScaler
from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt

#Importing the necessary dataframes for the classification
# data_in=pd.read_csv('/Volumes/TOSHIBA/immunix_project/ADRs project/Classification/data_processed_for_classification.csv')
data_in=pd.read_csv('/Volumes/TOSHIBA/immunix_project/ADRs project/Classification/new_data_processed_for_classifi_KPCA_.csv')
pred_test_data=pd.read_excel('/Volumes/TOSHIBA/immunix_project/ADRs project/Classification/binary_classifier/prediction_testing/ADR Prediction__set2.xlsx')
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Here we impliment the Naive Bayes classifier. This the the centeral function in this algorithem
def naive_bay(X_train, X_test, y_train, y_test,method):
    #nvb=naive_bayes.GaussianNB()
    nv=getattr(naive_bayes,method)
    nvb=nv()
    nvb.fit(X_train, y_train)
    y_pred = nvb.predict(X_test)
    con_mat=metrics.confusion_matrix(y_test,y_pred)
    Accuracy=metrics.accuracy_score(y_test, y_pred)
    f1= metrics.f1_score(y_test, y_pred)
    return con_mat,Accuracy,f1,y_pred
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Alternatively, we design Binary support vector machine
def Binary_sup_vec_machine(X_train, X_test, y_train, y_test):
    svm_cla=svm.SVC()
    svm_cla.fit(X_train,y_train)
    y_pred = svm_cla.predict(X_test)
    con_mat=metrics.confusion_matrix(y_test,y_pred)
    Accuracy=metrics.accuracy_score(y_test, y_pred)
    f1= metrics.f1_score(y_test, y_pred)
    
    return con_mat,Accuracy,f1,y_pred

#Here we impliment a function to compute othe evaluation metrics by using the Y_pred

def other_eval_methods(y_test, y_pred):
    
    #compute the percision
    perc=metrics.precision_score(y_test, y_pred)
    #compute the recall
    reca=metrics.recall_score(y_test, y_pred)
    #compute the Matthews correlation coefficient (MCC),its other name is phi coefficient
    matt_corr=metrics.matthews_corrcoef(y_test, y_pred)# A balance measure between -1 and 1
    #compute the AUC
    auc_roc=metrics.roc_auc_score(y_test, y_pred)
    
    return perc,reca,matt_corr,auc_roc


#>>>>>>>>>>>>>>>>>>>>>>START OF COMPUTATION<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>                    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

ADRs_df=additional_functions_for_binary.import_ADRs_list('2_drugs filter for _Itis-Ending_ADR.xlsx')
ADRs_df=ADRs_df.head(25)# The number 25 comes from the fact that we have chosed the drug names if the 
# number of ADRs related to this drug name is  larger thatn 3.
data=additional_functions_for_binary.binary_column(data_in,ADRs_df)
#Now we can determin the design matrix and label vector
'''features_matrix=data.loc[:,'2_percentile_ascspecks_AreaShape_Area':]
scaler = MinMaxScaler()
features_matrix_non_negative=scaler.fit_transform(features_matrix)'''
# Obtaining the design matrix after manifold learning
features_matrix_after_manifold=data.loc[:,'feature1':]
scaler = MinMaxScaler()
features_matrix_non_negative=scaler.fit_transform(features_matrix_after_manifold)

labels=data['binary_rate']

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# A binary encoder should be applied for the binary classifier
#First read a list for the mapping of 
labelencoder = LabelEncoder()
labels=labelencoder.fit_transform(labels)
# #>>>>>>>>>>>> 1.BINARY CLASSIFICATION, INCLUDING NEGATIVE VALUES<<<<<<<<<<<<<<<<<<<<<<<<<<

# # #Herein, we need to split data to train and test
#X_train, X_test, y_train, y_test = spliting_for_classifier(features_matrix,labels)
# #>>>>>>>>>>Implimenting the classification function<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# con_mat,Accuracy,f1=naive_bay(X_train, X_test, y_train, y_test)
#>>>>>>>>>>>>>><<BINARY CLASSIFICATION WITH NON-NEGATIVE VALUES<<<<<<<<<<<<<<<<<<<<
#X_train, X_test, y_train, y_test = additional_functions_for_binary.spliting_for_classifier(features_matrix_non_negative,labels)
# con_mat,Accuracy,f1=naive_bay(X_train, X_test, y_train, y_test,method="BernoulliNB")

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#For the prediction test we train the entire data 
X_train=features_matrix_non_negative
y_train=labels
X_test,y_test,_=additional_functions_for_binary.input_for_pred(pred_test_data,data)
#>>>>>>>>>>>>><<SVM Impelimentation<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
con_mat,Accuracy,f1,_=Binary_sup_vec_machine(X_train, X_test, y_train, y_test)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#A loop for different methods in naivve bayes classifier
# methods=["GaussianNB","MultinomialNB","ComplementNB","BernoulliNB"]
# result_list=[]
# confm_list=[]
# for method in methods:
#     _,Accuracy,f1,_=naive_bay(X_train, X_test, y_train, y_test,method)
#     #We can have additional evaluation measures for or classification 
#     #First, we compute the Y_pred
#     _,_,_,y_pred=naive_bay(X_train, X_test, y_train, y_test,method)
#     #Now we can compute the other evaluation metrics
#     perc,reca,matt_corr,auc_roc=other_eval_methods(y_test, y_pred)
    
#     result_list.append([Accuracy,f1,perc,reca,matt_corr,auc_roc])

# col=['Accuracy','f1','percision','recall','MCC','ROC_AUC']
# result_df=pd.DataFrame(result_list,columns=col)
# result_df.insert(loc=0, column='methods', value=methods)
#result_df.to_csv('NB_classsification_result_Itis_Ending_ADR.csv')
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''# Obtaining the confusion matrix for different naive bayes mehods 
for method in methods:
    conf_mat ,_,_ =naive_bay(X_train, X_test, y_train, y_test,method)
    confm_list.append(conf_mat)
  
# with open("test.txt", "w") as fp:
#     json.dump(confm_list, fp)    
for cf_matrix in confm_list:
    group_names = ['True Neg','False Pos','False Neg','True Pos']
    group_counts = ["{0:0.0f}".format(value) for value in
                    cf_matrix.flatten()]
    group_percentages = ["{0:.2%}".format(value) for value in
                          cf_matrix.flatten()/np.sum(cf_matrix)]
    labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in
              zip(group_names,group_counts,group_percentages)]
    labels = np.asarray(labels).reshape(2,2)
    sns.heatmap(cf_matrix, annot=labels, fmt='', cmap='Blues') 
'''
#>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#Obtaining prediction data frame
# _,_,pred_df=additional_functions_for_binary.input_for_pred(pred_test_data,data)
# _,_,_,y_pred=naive_bay(X_train, X_test, y_train, y_test,"ComplementNB")
# pred_df['y_pred']=y_pred
# pred_df.to_csv('set2_(auto-)immune_ADR.csv')
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Ploting the result of the binary classification
#1. Plotting the accuracy and f1 for naive bayes's methods
# x=result_df['methods']
# y1=result_df['Accuracy']
# y2=result_df['f1']
# plt.plot(x, y1, 'b',linewidth=4.0) # 
# plt.plot(x, y2, 'g',linewidth=4.0) # 
# plt.title('Binary_NB_Itis-Ending_ADR_manifold_lle')
# plt.xlabel('NB_methods',fontsize=13)
# plt.ylabel('Accuracy and f1 Ratios',fontsize=13)
# plt.legend(['Accuracy','f1'],loc="upper left",fontsize=11)
# plt.show()
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#2. Plotting the confusion matrix for the best method in naive bayes
# cf_matrix ,_,_,_ =naive_bay(X_train, X_test, y_train, y_test,"BernoulliNB")
cf_matrix ,_,_,_ =Binary_sup_vec_machine(X_train, X_test, y_train, y_test)
group_names = ['True Neg','False Pos','False Neg','True Pos']
group_counts = ["{0:0.0f}".format(value) for value in
                cf_matrix.flatten()]
group_percentages = ["{0:.2%}".format(value) for value in
                      cf_matrix.flatten()/np.sum(cf_matrix)]
labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in
          zip(group_names,group_counts,group_percentages)]
labels = np.asarray(labels).reshape(2,2)
sns.heatmap(cf_matrix, annot=labels, fmt='', cmap='Blues')
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#3. Plotting the other evaluation metrics
# x=result_df['methods']
# y3=result_df['percision']
# y4=result_df['recall']
# y5=result_df['MCC']
# y6=result_df['ROC_AUC']
# plt.plot(x, y3, 'c',linewidth=4.0) # 
# plt.plot(x, y4, 'm',linewidth=4.0) # 
# plt.plot(x, y5, 'y',linewidth=4.0) # 
# plt.plot(x, y6, 'r',linewidth=4.0) # 
# plt.title('Binary_NB_(auto-)immune_drug_ADR')
# plt.xlabel('NB_methods',fontsize=13)
# plt.ylabel('Evaluation metrics',fontsize=13)
# plt.legend(['percision','recall','MCC','ROC_AUC'],loc="upper left",fontsize=11)
# plt.show()