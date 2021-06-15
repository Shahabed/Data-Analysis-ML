#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 15:19:01 2021

@author: Shahbedin Chatraee Azizabadi
Additional function for the binary classification 
"""
from sklearn import metrics
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder

# we can import a list of categorize ADRs which can be used later as a threshold
def import_ADRs_list(name):
    full_name='/list of important ADRs/'+name
    df=pd.read_excel(full_name)
    ADRs_df=df[['compound_drug','Unique concatenate(prefered_reaction_term)']]
    #For the infection list use the following script as the structure of this dataframe differs from the others
    #ADRs_df=df[['compound_drug','Concatenate(prefered_reaction_term)']]
    
    return ADRs_df
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#A function to add a binary column as the label vector based on the ADRs_list
def binary_column(data,ADRs_df):
    ADRs_list=ADRs_df['Unique concatenate(prefered_reaction_term)'].values.tolist()
    #For the infection list use the following script for the same reason mentioned above
    #ADRs_list=ADRs_df['Concatenate(prefered_reaction_term)'].values.tolist()
    drug_list=ADRs_df['compound_drug'].values.tolist()
    binary_list=[]    
    try:
        for d in data.itertuples():
            drug1=d.compound_drug
            adr=d.prefered_reaction_term
            #if any(drug1 in s for s in ADRs_list):
            #if drug1 in drug_list and any(adr in s for s in ADRs_list):    
            if drug1 in drug_list:    
                binary='YES'
                binary_list.append(binary)
            else:
                binary='NO'
                    #saving to the lists#
            
                binary_list.append(binary)           
    
    except Exception as e:
       print ("")
       print (">> evaluation-loop FAILED at: ---------------------")
       print ("exception: ", e)
       print ("")       
    #data['binary_rate']=binary_list
    data.insert(0,'binary_rate',binary_list)
        
    return data
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#A function for the spliting of the design matrix and the label vector
def spliting_for_classifier(features_matrix,labels):
    
    (X, y) = (features_matrix, labels)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    
    return X_train, X_test, y_train, y_test
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# The input of the function is the test data set provided by the experimentalist to examine the generalization of the 
# classification algorithm, how good the algorithm generalize. Also we have the main data set
# to match and extract the necessary information for creating the X_test and y_test, the test data set is just the name 
# of drugs and ADRs and does not contain the information(feature set and labels) for the  processing of the  classification.
def input_for_pred(pred_test,data):
    #  We match the test data set with the main data set and extract part of the data with contains the 
    # Drug_ADR names.
    data_for_pred=data[data['barcode'].isin(pred_test['Barcode']) & data['well_key'].isin(pred_test['R1_Well'])| data['well_key'].isin(pred_test['R2_Well'])| data['well_key'].isin(pred_test['R3_Well'])]#| data['well_key'].isin(pred_test['R1_Well'])| data['well_key'].isin(pred_test['R1_Well'])]
    data_for_pred=data_for_pred.reset_index()
    # For the case that we have the data without manifold learning
    #xtest=data_for_pred.loc[:,'2_percentile_ascspecks_AreaShape_Area':]
    # For the case we have applied manifold learning on the input data
    xtest=data_for_pred.loc[:,'feature1':]
    scaler = MinMaxScaler()
    X_test=scaler.fit_transform(xtest)
    labels=data_for_pred['binary_rate']
    labelencoder = LabelEncoder()
    y_test=labelencoder.fit_transform(labels)
    pred_df=data_for_pred[['barcode','well_key','InChI_Key','compound_drug']]
    y_t=y_test.tolist()
    pred_df['y_test']=y_t
    
    return X_test,y_test,pred_df
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><

# A function for ploting confusion matrix based on the different classifiers which is given as input
def plot_confusion_matrix(clf, X_test, y_test):
    
    ax=metrics.plot_confusion_matrix(clf, X_test, y_test)
    
    return ax
