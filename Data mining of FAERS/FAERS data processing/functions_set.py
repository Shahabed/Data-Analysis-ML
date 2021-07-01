#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 13:01:25 2020

@author: Shahabedin Chatraee Azizabadi
"""
import pandas as pd
import os
import glob


#>>>Function to screen for the ADR reporter qualification. This function should be applied on demographic data setwhich has a role of metadat<<<<<<
def reporter_qual(demo_data, qualification):
    #Qualification can be choseen as--- MD Physician---PH Pharmacist ----OT Other health-professional LW Lawyer--- CN Consumer--or some/all of them
    demo_repo_scr=demo_data[demo_data.occp_cod.isin(qualification)].copy()
    
    return demo_repo_scr

# EXAMPLE:filt_demo=reporter_qual(df_demographic,['MD','PH'])

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Function to screen the drug based on the drug characterization

def drug_character(drug_data, character):
    # Drug characterization: PS Primary Suspect Drug ---SS Secondary Suspect Drug ---C Concomitant----I Interacting
    drug_char_scr=drug_data[drug_data.role_cod.isin(character)].copy()
    return drug_char_scr

#EXAMPLE: filt_drug=drug_character(df_drug,['PS'])
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Function to join the data frem three data frame: Demographic, Drug and reaction

def ADR_data_connector(df_demographic,df_drug,df_reaction):
    demographic=reporter_qual(df_demographic,['MD','PH'])
    
    join_list=[]
    try:
        for record in demographic.itertuples():
           primary_id=record.primaryid
           case_id=record.caseid
           occp_code=record.occp_cod
           
           #each primary_id is connected to some drug name, we first take the data frame for drug
           drug=drug_character(df_drug,['PS'])
           #now we can filter it for the above primary_id
           drug_of_this_primaryid=drug[drug.primaryid==primary_id]
           for row in drug_of_this_primaryid.itertuples():
               
               drug_name=row.drugname
               product_ai=row.prod_ai
               
               reaction=df_reaction
               reaction_of_this_primaryid=reaction[reaction.primaryid==primary_id]
               
               for rows in reaction_of_this_primaryid.itertuples():
                   prefered_reaction_term=rows.pt
                   
                   # Join values from the three tables into one list
                   join_list.append([primary_id, case_id, occp_code, drug_name,product_ai,prefered_reaction_term])
     
            
    except Exception as e:
       print ("")
       print (">> ADR-loop FAILED at: ---------------------")
       print ("exception: ", e)
       print ("")
     # make a datafarame from it
    col_names =  ['primary_id','case_id', 'occp_code', 'drug_name','product_ai','prefered_reaction_term']
    join_table = pd.DataFrame(join_list, columns=col_names)           
        
    return join_table
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
