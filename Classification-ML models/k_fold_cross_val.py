#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 21:06:17 2021

@author: Shahabedin Chatraee Azizabadi

K-fold Cross-validation of classification algorithm
"""
import time
import numpy as np
from sklearn.model_selection import KFold, cross_val_score
import pandas as pd
import additional_functions_for_binary
from sklearn.preprocessing import LabelEncoder,MinMaxScaler
from sklearn import svm, metrics,naive_bayes
import matplotlib.pyplot as plt
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#----------------cross-validated metric---------------------------------------------------
def cross_va_scor(features_matrix_non_negative, labels):
    clf = svm.SVC(kernel='rbf', C=1, random_state=42)
    scores = cross_val_score(clf, features_matrix_non_negative, labels, cv=5)
    
    return scores
#>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#-------cross-validation with k-fold


def k_fold_cross(X,y, model,k):
    
    try:
        
        kf = KFold(n_splits=k,random_state=None)
        acc_score = []
        f1_co=[]
        perc_co=[]
        for train_index , test_index in kf.split(X):
            X_train , X_test = X.iloc[train_index,:],X.iloc[test_index,:]
            y_train , y_test = y[train_index] , y[test_index]
             
            model.fit(X_train,y_train)
            pred_values = model.predict(X_test)
             
            acc = metrics.accuracy_score(pred_values , y_test)
            f1=metrics.f1_score(pred_values , y_test)
            perc=metrics.precision_score(pred_values , y_test)
            acc_score.append(acc)
            f1_co.append(f1)
            perc_co.append(perc)
        avg_acc_score = sum(acc_score)/k     
       
    except Exception as e:
         print ("")
         print (">> The cross validation process:: FAILED ------------------------")
         print (">> model:", model)
         print ("exception: ", e)
         print ("")        
         #return pd.DataFrame()
    return avg_acc_score,acc_score,f1_co,perc_co
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<
# A function for different methods in Näive Bayes: The goal is to produce different models with these methods 

def Naive_B_methods():
    model_list=[]
    methods=["GaussianNB","MultinomialNB","ComplementNB","BernoulliNB"]
    for method in methods:
        nv=getattr(naive_bayes,method)
        nvb=nv()
        model_list.append(nvb)
    
    return model_list


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<
time_started = time.time()
# Uplaod the the data set for cross-validation
data_in=pd.read_csv('/Volumes/TOSHIBA/immunix_project/ADRs project/Classification/new_data_processed_for_classifi_KPCA_.csv')

ADRs_df=additional_functions_for_binary.import_ADRs_list('5_drugs filter for _inflammation_ADR.xlsx')
ADRs_df=ADRs_df#.head(25)# The number 25 comes from the fact that we have chosed the drug names if the 
# number of ADRs related to this drug name is  larger thatn 3.
data=additional_functions_for_binary.binary_column(data_in,ADRs_df)
#Now we can determin the design matrix and label vector
'''features_matrix=data.loc[:,'2_percentile_ascspecks_AreaShape_Area':]
scaler = MinMaxScaler()
features_matrix_non_negative=scaler.fit_transform(features_matrix)'''
# Obtaining the design matrix after manifold learning
features_matrix_after_manifold=data.loc[:,'feature1':]
scaler = MinMaxScaler()
features_matrix_non_negative=pd.DataFrame(scaler.fit_transform(features_matrix_after_manifold),columns = features_matrix_after_manifold.columns)

labels=data['binary_rate']

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# A binary encoder should be applied for the binary classifier
#First read a list for the mapping of 
labelencoder = LabelEncoder()
labels=labelencoder.fit_transform(labels)
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# here, we can test different models of Binary classifier by defining these models
# The first model is support vector machine 
svm_cla=svm.SVC()
# The second model is Näive Bayes: As we have several methods but regarding the prvious result
# we chose  GaussianNB and ComplementNB

NVB=naive_bayes.ComplementNB()

av_acc,acc,f1,perc=k_fold_cross(features_matrix_non_negative,labels,svm_cla,5)
# Plotting of the k-fold cross validation 
x=['trial1','trial2','trial3','trial4','trial5']
y1=acc
y2=f1
y3=perc
plt.plot(x, y1, 'b',linewidth=4.0) # 
plt.plot(x, y2, 'g',linewidth=4.0) # 
plt.plot(x, y3, 'r',linewidth=4.0) # 
plt.title('Binary_SVM_Inflamation_ADR_manifold')
plt.xlabel('k-fold trial',fontsize=13)
plt.ylabel('Accuracy, f1 and precision Ratios',fontsize=13)
plt.legend(['Accuracy','f1','precision'],loc="upper left",fontsize=11)
plt.show()

time_end = time.time()
print("Elapsed", np.round(time_end-time_started, 2), "seconds")
