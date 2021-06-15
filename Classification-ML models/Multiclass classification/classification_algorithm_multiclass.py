#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 11:09:23 2020

@author:Shahabedin Chatraees Azizabadi
Classification algorithm for ADRs prediction
"""
import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm,naive_bayes,linear_model
from sklearn import metrics
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# First reading the output result of classification_data_preprocessing
#data=pd.read_csv('/Volumes/TOSHIBA/immunix_project/ADRs project/Classification/data_processed_for_classification.csv')
data=pd.read_csv('/Volumes/TOSHIBA/immunix_project/ADRs project/Classification/new_data_processed_for_classifi_KPCA.csv')

def maxEnt_classifier(X_train, X_test, y_train, y_test):
    # Making  an instance of the classification Model
    maxent = linear_model.LogisticRegression(penalty='l2', C=1.0,max_iter=100,dual=False)
    maxent.fit(X_train, y_train)
    #That is a matrix with the shape (n_classes, n_features):Coefficient of the features in the decision function can be obtain as follow:
    cof=maxent.coef_
    #Predict class labels for samples in X
    y_predicted = maxent.predict(X_test)
    #>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    con_mat=metrics.confusion_matrix(y_test,y_predicted)
    # Here we can compute the f1 function
    f1= metrics.f1_score(y_test, y_predicted, average=None) 
    Accuracy=metrics.accuracy_score(y_test, y_predicted)
    return con_mat,cof,Accuracy,f1

def random_forest_classifier(X_train, X_test, y_train, y_test):
    
    Randomf = RandomForestClassifier(n_estimators=20,criterion = 'entropy', random_state=42)
    Randomf.fit(X_train, y_train)
    #cof2=regressor.coef_
    y_pred = Randomf.predict(X_test)
    #dev_acc = accuracy_score(y_test, y_pred)
    con_mat=metrics.confusion_matrix(y_test,y_pred)
    class_report=metrics.classification_report(y_test,y_pred)
    Accuracy=metrics.accuracy_score(y_test, y_pred)
    return con_mat,class_report,Accuracy

def SVM_classifier(X_train, X_test, y_train, y_test):
    svclassifier = svm.SVC(kernel='poly', degree=3, C=1,decision_function_shape='ovo')
    svclassifier.fit(X_train, y_train)
    y_pred2 = svclassifier.predict(X_test)
    con_mat2=metrics.confusion_matrix(y_test,y_pred2)
    Accuracy2=metrics.accuracy_score(y_test, y_pred2)
    return con_mat2,Accuracy2
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def naive_bay(X_train, X_test, y_train, y_test,method):
    #nvb=naive_bayes.GaussianNB()
    nv=getattr(naive_bayes,method)
    nvb=nv()
    nvb.fit(X_train, y_train)
    y_pred = nvb.predict(X_test)
    con_mat=metrics.confusion_matrix(y_test,y_pred)
    Accuracy=metrics.accuracy_score(y_test, y_pred)
    f1= metrics.f1_score(y_test, y_pred, average=None)
    return con_mat,Accuracy,f1
#>>>>>>>>>>>evaluation of classifiers<<<<<<<<<<<< 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<
time_started = time.time()
#features_matrix=data.loc[:,'2_percentile_ascspecks_AreaShape_Area':]
# Feature matrix in the case of manifold learning application
features_matrix_after_manifold=data.loc[:,'feature1':]
labels=data['prefered_reaction_term']
# label encoding and feature matrix scaling
labelencoder = LabelEncoder()
labels=labelencoder.fit_transform(labels)
sc = StandardScaler()
scaler = MinMaxScaler()
features_matrix_non_negative=scaler.fit_transform(features_matrix_after_manifold)
(X, y) = (features_matrix_non_negative, labels)
# #Herein, we need to split data to train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
#>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Testing maxEnt
#cof,dev_acc,Accuracy,f1=maxEnt_classifier(X_train, X_test, y_train, y_test)
#>>>>>>>>>>>>>>>>>>>>>
#Testing Random forest
con_mat,class_report,Accuracy=random_forest_classifier(X_train, X_test, y_train, y_test)
#>>>>>>>>>>>>>>>>
# Testing SVM
#con_mat,Accuracy,f1=naive_bay(X_train, X_test, y_train, y_test,"GaussianNB")
time_end = time.time()
print("Elapsed", np.round(time_end-time_started, 2), "seconds")