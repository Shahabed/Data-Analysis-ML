#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 11:04:38 2020

@author: Shahabedin Chatraee Azizabadi
Algorithm for the data mining of the large frequency tables of ADRs data

"""
import pandas as pd
import numpy as np
import time
import sys
'''The  method used here is Proportional Reporting Ratio'''
#First we import the joint ADRs data frame 
df=pd.read_csv("/Volumes/TOSHIBA/immunix_project/compound information with adverse effects/ADRs_data_processing/test_dataframe_result.csv").head(1000)

# A function for computation of different frequencies
#Here for all the functions we can define a class with  a group of input whci is common between them 
def frequencies_calc(df,drug, effect):
    
    #First we import the joint ADRs data frame 
    ADRs_joint=df
    N=ADRs_joint['prefered_reaction_term'].count()
    D=(ADRs_joint['drug_name'] == drug).sum()
    E=(ADRs_joint['prefered_reaction_term'] == effect).sum()
    e=(ADRs_joint['prefered_reaction_term'] != effect).sum()
    d=(ADRs_joint['drug_name'] != drug).sum()
    DE=((ADRs_joint['drug_name'] == drug)&(ADRs_joint['prefered_reaction_term'] == effect)).sum()
    dE=((ADRs_joint['drug_name'] !=  drug)&(ADRs_joint['prefered_reaction_term'] == effect)).sum()
    De=((ADRs_joint['drug_name'] == drug)&(ADRs_joint['prefered_reaction_term'] != effect)).sum()
    de=((ADRs_joint['drug_name'] != drug)&(ADRs_joint['prefered_reaction_term'] != effect)).sum()
    
    return N,D,E,e,d,DE,dE,De,de

#>>>>>>>>>>>><<<<>>>>>>>>>><<<<>>>>><<<<<<<<>>>><<<<<<<<<<>>>>>><<<<<<<
#A function for computing PRR
def PRR_algorithm(df,drug, effect):
    
    N,D,E,e,d,DE,dE,De,de=frequencies_calc(df,drug, effect)
    global PRR
    if dE*D !=0 :#Condition for denominator not to be zero
        PRR=(DE*d)/(dE*D)
        
    return PRR,DE

#<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<
#A function to compute the Chi-squared value (χ2 with Yates' correction) 

def chi_squared_algorithm(df,drug, effect):
   N,D,E,e,d,DE,dE,De,de=frequencies_calc(df,drug,effect)
   global chi_2
   #First we define the numerator
   a= N*(np.absolute((DE*de)-(dE*De))-N/2)**2
   #Second we define denominator
   b=(E*e*D*d)
   if b !=0:
       chi_2=a/b
    
    
   return chi_2


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#This function is to itterate ove the ADRs table and produce the frequency table

def Adrs_freq_table(df):
    
    ADRs_joint=df
    ADRs_joint=ADRs_joint.rename(columns = {' case_id':'case_id'})
    freq_list=[]
    try:
    
    
        for val in ADRs_joint.itertuples():
            primary_id=val.primary_id
            case_id=val.case_id
            occp_code=val.occp_code
            drug=val.drug_name
            product_ai=val.product_ai
            effect=val.prefered_reaction_term
            
            #Herein, we call the functions defined above 
            
            PRR,_=PRR_algorithm(df,drug, effect)
            #PRR,_=PRR_algorithm(str(drug), str(effect))
            
            chi=chi_squared_algorithm(df,drug, effect)
            
            _,DE=PRR_algorithm(df,drug, effect)
            
            freq_list.append([primary_id,case_id,occp_code,drug,product_ai,effect,PRR,chi,DE])
            sys.stdout.write('.'); sys.stdout.flush(); 
            
            
    except Exception as e:
       print ("")
       print (">> Data mining-loop FAILED at: ---------------------")
       print ("exception: ", e)
       print ("")                
    col_names =  ['primary_id','case_id','occp_code','drug_name','product_ai',' prefered_reaction_term',  'PRR','chi_2','DE']
    freq_table=pd.DataFrame(freq_list, columns=col_names)  
    return freq_table
#<<<<<<>>>>>>>>><<<<<<<<<<>>>>>>>>>>><<<<<<<<<<<<<<>>>>>>>><<<<<<>><
#___>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#Filtering function for finding interesting drug vs effect associations

def filt_Adrs_freq(freq_table,DE_tresh,PRR_tresh,chi_2_tresh):
    
    
    df = freq_table.loc[(freq_table['DE'] >= DE_tresh) & (freq_table['PRR'] >= PRR_tresh)& (freq_table['chi_2'] >= chi_2_tresh)]
    df=df.drop_duplicates()
       
    return df
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


time_started = time.time()

dff=Adrs_freq_table(df)
dff_fil=filt_Adrs_freq(dff,3,2,4)

dff.to_csv('frequency_table.csv')

dff_fil.to_csv('frequency_filtered_df.csv')

time_end = time.time()
print("Elapsed", np.round(time_end-time_started, 2), "seconds")
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><