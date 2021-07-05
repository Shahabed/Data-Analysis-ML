#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Shahabedin Chatraee Azizabadi
Object-oriented version of ADRs frequency datamining
"""
import pandas as pd
import numpy as np
import time
import sys
'''The first method used here is Proportional Reporting Ratio'''


df=pd.read_csv("/Volumes/TOSHIBA/immunix_project/compound information with adverse effects/ADRs_data_processing/test_dataframe_result.csv").head(1000)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

class frequency_compute(object):
    def __init__(self, df,drug, effect):   #the set of attributes are common between the instances of the current class
        
        self.df=df
        self.drug=drug
        self.effect=effect
        
        
        
    def frequencies_calc(self):
        
        #First we import the joint ADRs data frame 
        ADRs_joint=self.df
        N=ADRs_joint['prefered_reaction_term'].count()
        D=(ADRs_joint['drug_name'] == self.drug).sum()
        E=(ADRs_joint['prefered_reaction_term'] == self.effect).sum()
        e=(ADRs_joint['prefered_reaction_term'] != self.effect).sum()
        d=(ADRs_joint['drug_name'] != self.drug).sum()
        DE=((ADRs_joint['drug_name'] == self.drug)&(ADRs_joint['prefered_reaction_term'] == self.effect)).sum()
        dE=((ADRs_joint['drug_name'] !=  self.drug)&(ADRs_joint['prefered_reaction_term'] == self.effect)).sum()
        De=((ADRs_joint['drug_name'] == self.drug)&(ADRs_joint['prefered_reaction_term'] != self.effect)).sum()
        de=((ADRs_joint['drug_name'] != self.drug)&(ADRs_joint['prefered_reaction_term'] != self.effect)).sum()
        
        return N,D,E,e,d,DE,dE,De,de        
    
    #A function for computing PRR
    def PRR_algorithm(self):
        
        N,D,E,e,d,DE,dE,De,de=self.frequencies_calc()
        #global PRR
        if dE*D !=0 :#Condition for denominator not to be zero
            PRR=(DE*d)/(dE*D)
            
        return PRR,DE
    
    
    def chi_squared_algorithm(self):
       N,D,E,e,d,DE,dE,De,de=self.frequencies_calc()
       #global chi_2
       #First we define the numerator
       a= N*(np.absolute((DE*de)-(dE*De))-N/2)**2
       #Second we define denominator
       b=(E*e*D*d)
       if b !=0:
           chi_2=a/b
        
        
       return chi_2

    def Adrs_freq_table(self):
        
        ADRs_joint=self.df
        ADRs_joint=ADRs_joint.rename(columns = {' case_id':'case_id'})
        freq_list=[]
        
        
        for val in ADRs_joint.itertuples():
            primary_id=val.primary_id
            case_id=val.case_id
            occp_code=val.occp_code
            drug=val.drug_name
            product_ai=val.product_ai
            effect=val.prefered_reaction_term
            
            #Herein, we call the functions defined above 
            
            PRR,_=self.PRR_algorithm()
            #PRR,_=PRR_algorithm(str(drug), str(effect))
            
            chi=self.chi_squared_algorithm()
            
            _,DE=self.PRR_algorithm()
            
            freq_list.append([primary_id,case_id,occp_code,drug,product_ai,effect,PRR,chi,DE])
            sys.stdout.write('.'); sys.stdout.flush(); 
        col_names =  ['primary_id','case_id','occp_code','drug_name','product_ai',' prefered_reaction_term',  'PRR','chi_2','DE']
        freq_table=pd.DataFrame(freq_list, columns=col_names)  
        return freq_table
    
    
    def filt_Adrs_freq(freq_table,DE_tresh,PRR_tresh,chi_2_tresh):
        
        
        df = freq_table.loc[(freq_table['DE'] >= DE_tresh) & (freq_table['PRR'] >= PRR_tresh)& (freq_table['chi_2'] >= chi_2_tresh)]
        df=df.drop_duplicates()
           
        return df


time_started = time.time()

dff=frequency_compute()
#dff_fil=filt_Adrs_freq(dff,3,2,4)

#dff.to_csv('frequency_table.csv')

#dff_fil.to_csv('frequency_filtered_df.csv')

time_end = time.time()
print("Elapsed", np.round(time_end-time_started, 2), "seconds")
