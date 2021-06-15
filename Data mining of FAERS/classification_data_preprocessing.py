#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 13:31:52 2020

@author: Shahabedin Chatraee Azizabadi
Data processing for classification: Here we creat X(design matrix) and Y(label) vectors, encode Y vector and creat binary data set for binary classifier 
"""
import pandas as pd
import numpy as np
import time
import jellyfish

#Import the similarity table

sim_tab=pd.read_csv('/Volumes/TOSHIBA/immunix_project/ADRs project/adrs_computation/similarity_table_complete_data__0.9.csv',index_col=0)

#Import the screening data

screen_data=pd.read_csv('/Users/chatraees/Desktop/feature_reduction_correlation_matrix_0.9_ratio.csv',index_col=0)



# Removing the mismatches from  the similarity table based on the review and report from the experts°°°°Also removing the duplicate matches which are not adding 
# any learning weights to our prediction function( Model )
def remove_duplicates(df):
    #First we remove the duplicate matches 
    df1=df.drop_duplicates( subset=[ "barcode","compound_drug", "adrs_drug","prefered_reaction_term"], keep="first", inplace=False)
    df1=df1.reset_index()
    
    return df1
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def remove_mismatches(df,mis_list):
    #a=remove_duplicates(df)
    # first one should define a list of mismatches called mis_list
    a= df[~pd.Series(list(zip(df['compound_drug'], df['adrs_drug']))).isin(mis_list)]
    #alternative script
    #a=df[~df[['compound_drug','adrs_drug']].apply(tuple, 1).isin(mis_list)]
    return a
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#Function for creating X and Y vectors: we should add the set of features:concatenating

def class_data_set(similarity_table,screen_data):
    
    # align indices
    df1 = similarity_table.set_index(['barcode','well_key'])
    df2 = screen_data.set_index(['barcode','well_key'])
    
    # calculate & apply '''mask'''
    df2 = df2[df2.index.isin(df1.index)].reset_index()
    df3 = df1.merge(df2, on=['barcode','well_key'], how='inner')
    #df3=df3.reset_index(0).reset_index(drop=True)
    return df3
#>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# The following function can deal with the missing values like NaN, Inf,etc. DATA IMPUTATION. It is for the case when we have missing values in our data
#!!!!!!!!!!With the current data base we don't need this function, as the data base is dimensinaly reduced. So, it is already imputed!!!!!!!!!!!!
def data_imputation(df):
    df=df.replace([np.inf, -np.inf], np.nan)
    df=df.dropna(axis=1,how='all')
    df=pd.DataFrame(df).fillna(df.mean())
  
    return df
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#First define the mis_list contains the mismatches discovered from experts in pharmocology 
time_started = time.time()


mis_list=[('Rifaximin','RIFAMPICIN'),('Ganciclovir','ACICLOVIR'),('Ganciclovir','Aciclovir'),('Aciclovir','GANCICLOVIR'),('Mecarbinate','RECOMBINATE'),('Lincomycin HCl','VANCOMYCIN HCL')
          ,('Famciclovir','ACICLOVIR'),('Famciclovir','Aciclovir'),('Mesalamine','MESALAZINE Unk'),('Mesalamine','MESALAZINE'),('Ciclopirox','CICLOSPORIN')
          ,('Coumarin','COUMADINE'),('Coumarin','COUMADIN'),('Nilvadipine','NICARDIPINE'),('Valganciclovir HCl','Valaciclovir'),('Vinblastine sulfate','VINCRISTINE SULFATE.')
          ,('Cefuroxime sodium','CEFOTAXIME SODIUM'),('Ropivacaine HCl','BUPIVACAINE HCL'),('Clopidol','CLOPIDOGREL')
          ,('Procaine','PROPECIA'),('Remodelin','REMODULIN')]


#First remove the duplicated association
a=remove_duplicates(sim_tab)
# To remove the mismatches
b=remove_mismatches(a,mis_list)
# To concatenating two data frames
df2=class_data_set(b,screen_data)
#Droping an additional index column: using drop.i indexing
df2=df2.drop(df2.columns[2], axis=1)
df2.to_csv('data_processed_for_classification.csv')
time_end = time.time()
print("Elapsed", np.round(time_end-time_started, 2), "seconds")


