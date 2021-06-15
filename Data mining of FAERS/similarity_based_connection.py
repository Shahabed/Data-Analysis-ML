#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:22:02 2020

@author: Shahabedin Chatraee Azizabadi

The similarity matching algorithem finds the maching pairs between ADR reports and existing compound data used on assays.
The output is the a data frame with information from both above tables where they drug names have matched. 
"""
import pandas as pd
import numpy as np
import time
import jellyfish
import matplotlib.pyplot as plt
import sys

# The first step is to upload the compounds and ADR-report data frames 

compound_data=pd.read_csv('compunds_screening_d.csv',index_col=0)
adrs_data=pd.read_csv('/test_dataframe_result.csv',index_col=0)

#Here in we creat two lists out of drug name in compund data and adrs data: the content od columns are series should be converted to list
# drug_compound_data=compound_data['Product Name'].tolist()

# drug_adrs_data=adrs_data['drug_name'].tolist()

#>>>>>>>>>>>>>>We define a function to measure the similarity distance between two strings of the  drug names. 
#Also some data formating process are implimented.  <<<<<<<<<<<<<<<<<<<<

def similarity_distance(s1,s2,function_name):
       
 # Herein, we first apply the formating, string into uppercase, on two strings   
    s1=s1.upper()
    s2=s2.upper()
    #get module variable by name, so we can change the function for measuring the distance between two strings. The functaion_name can var:
    # 1. levenshtein_distance ;;;;2. damerau_levenshtein_distance 3.hamming_distance;; 4.jaro_similarity;;5. jaro_winkler_similarity 
    var=getattr(jellyfish, function_name)
    
    distance_score= var(s1,s2) 
    
    return distance_score
#________>>>>>>>>>>>_________<<<<<<<<<<<<<<

#______::::;;;>>>>>>>>>>>>>>> Here, we define a function to match between the two strings of drug names in two data frames.<<<<<<<<<<<<<<<<<<<

def get_similarity_table(compound_data,adrs_data,score):
    pairs_list=[]
    try:
        #for s1 in compound_data['product_name']:
        for s in compound_data.itertuples():
            s1=s.product_name
            barcode=s.barcode
            well_key=s.well_key
            Target=s.Target
            InChI_Key=s.Molecule_InChI_Key
            #for s2 in adrs_data['drug_name']:
            for record in adrs_data.itertuples():
                s2=record.drug_name
                primary_id=record.primary_id
                prefered_reaction_term=record.prefered_reaction_term
                product_ai=record.product_ai
                distance_score=similarity_distance(s1,s2,function_name="jaro_winkler_similarity")
                matching_rate=similarity_distance(s1,s2,function_name="match_rating_comparison")
                if (distance_score>score):
                    ''' Conclusively, the Match rating comparison should be added as an additional condition in similarity algorithm.'''
                    if matching_rate is True:
                        pairs_list.append([barcode,well_key,Target,InChI_Key,s1,s2,primary_id,prefered_reaction_term,product_ai,distance_score,matching_rate])
                        sys.stdout.write('.'); sys.stdout.flush(); 
                
    except Exception as e:
       print ("")
       print (">> Similarity-loop FAILED at: ---------------------")
       print ("exception: ", e)
       print ("")           
                
    colu_mns=['barcode','well_key','Target','InChI_Key','compound_drug','adrs_drug','primary_id','prefered_reaction_term','product_ai','distance','m_rate']
    pairs_table=pd.DataFrame(pairs_list, columns=colu_mns) 
    pairs_table=pairs_table.sort_values(by=['barcode','well_key'])
    return pairs_table
#<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<

#We define a function to evaluate how good the distance function has worked: Match Rating Approach 
def evaluation_function(similarity_table):
    
    df=similarity_table[['compound_drug','adrs_drug','distance']]
    
    df = df.drop_duplicates(subset = ["compound_drug"])
    eval_list=[]
    haming_list=[]
   
    try:
        for re in df.itertuples():
            
            st1=re.compound_drug
            st1=st1.upper()
            st2=re.adrs_drug
            #using Match Rating Approach
            matching_rate=jellyfish.match_rating_comparison(st1, st2)
            haming=jellyfish.hamming_distance(st1, st2)
            #dld=jellyfish.damerau_levenshtein_distance(st1, st2)
            
            #saving to the lists#
            eval_list.append(matching_rate)
            haming_list.append(haming)
            #dld_list.append(dld)
    
    except Exception as e:
       print ("")
       print (">> evaluation-loop FAILED at: ---------------------")
       print ("exception: ", e)
       print ("")       
    df['matching_rate']=eval_list
    df['haming']=haming_list
    
    
    return df


# A function to find the ration of true negative 
def ratio_true_negative():
    score_list=[j for j in np.arange(0.8,0.96,0.01)]
    ratio_list=[]
    try:
        for i in score_list:
            a=get_similarity_table(compound_data,adrs_data,i)
            #the size of similarity table
            size=len(a)
            b=evaluation_function(a)
            # Converting Nan in mathing_rate to boolean False
            b=b.fillna(False)
            #calculate true negative 
            tn=(~b['matching_rate']).values.sum()
            #the size of boolian column 
            tot=b['matching_rate'].count()
            #calculate the true negative ratio
            r=tn/tot
            ratio_list.append([i,size,tn,tot,r])
    except Exception as e:
       print ("")
       print (">> ratio-loop FAILED at: ---------------------")
       print ("exception: ", e)
       print ("")       
    cul=['similarity_ratio','size_of_similarity_table','number_of_false_ratio','total_number_of_ratios','true_negative']
    ratio_table=pd.DataFrame(ratio_list,columns=cul)
    return ratio_table


start = time.time()

a=get_similarity_table(compound_data,adrs_data,0.89)
a.to_csv("similarity_table.csv")

''' The rest of algorith is for testing and ploting 

b=evaluation_function(a)
## Map booliand column to 0 and 1
b=b.fillna(False)
b["matching_rate"] = b["matching_rate"].astype(int)


#Creating ratio table to compare the match rates for different similarity_ratios
c=ratio_true_negative()

b.to_csv('eval_table.csv')
c.to_csv("ratio_table.csv")

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'ploting the match_rates for different similarity ratios'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
c=pd.read_csv("ratio_table.csv")
fig, ax1 = plt.subplots()
x = c['similarity_ratio']
y1 = c['true_negative']
y2 = c['size_of_similarity_table']

ax2 = ax1.twinx()

ax1.set_ylabel('true_negative_ratios',fontsize=13)
ax1.set_xlabel('similarity_ratio',fontsize=13)
ax2.set_ylabel('size_of_similarity_table',fontsize=13)


ax1.plot(x, y1, 'r-',label="true_negative_ratios")
ax2.bar(x, y2,width=0.001,label="size_of_similarity_table")
plt.legend(loc="upper right")
'''

time_end = time.time()
print("Elapsed", np.round(time_end-start, 2), "seconds")
#>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#a=get_similarity_table(compound_data,adrs_data,0.8)


# # ## a.to_csv("similarity_table.csv")

# b=evaluation_function(a)

# ##b['index_col'] = b.index
# ## A new index column is created 
# b['new_col'] = range(1, len(b) + 1)

# ## Map booliand column to 0 and 1
# b=b.fillna(False)
# b["matching_rate"] = b["matching_rate"].astype(int)

# b.to_csv('eval_table.csv')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
##Ploting regarding the cases showing the jaro-winkler similarity and match rating comparison

# b=pd.read_csv("eval_table.csv")
# ## plt.scatter(b['new_col'], b['distance'])
# ## plt.show()


# fig, ax1 = plt.subplots()
# x = b['new_col']
# y1 = b['distance']
# y2 = b['haming']
# y3=b['matching_rate']

# # #3D PLOting
# # threedee = plt.figure().gca(projection='3d')
# # threedee.scatter(x, y1, y2,cmap='hot',c=y1)
# # threedee.set_xlabel('Index')
# # threedee.set_ylabel('H-L')
# # threedee.set_zlabel('Close')
# # plt.show()
# #ax2 = ax1.twinx()
# ax3 = ax1.twinx()


# a1=ax1.plot(x, y1, 'g.')
# #a2=ax2.plot(x, y2, 'b+')
# ax3.plot(x, y3, 'r.')
# ax1.set_ylabel('similarity_distance',fontsize=13)
# ax1.set_xlabel('matching_case_number',fontsize=13)
# ax3.set_ylabel('matching_rate',fontsize=13)

#plt.legend([a1,a2],["plot 1", "plot 2"])


