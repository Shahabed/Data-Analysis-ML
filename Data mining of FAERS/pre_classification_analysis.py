#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Shahabedin Chatraee Azizabadi
"""
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

df=pd.read_csv('/similarity_table_complete_data__0.9.csv',index_col=1)
df1=df.drop_duplicates( subset=[ "compound_drug", "adrs_drug" ,"prefered_reaction_term"], keep="first", inplace=False)

# The first function is to find ranking between the reported effects 
def ranking_adrs(df):
    #a=df.groupby(['adrs_drug','prefered_reaction_term'], as_index=False).count()
    df=df.drop_duplicates( subset=[ "compound_drug", "adrs_drug","prefered_reaction_term"], keep="first", inplace=False)
    a=df.groupby(['prefered_reaction_term'], as_index=False).count()
    a=a.rename(columns={'Unnamed: 0':'count'})
    a=a[['prefered_reaction_term','count']].sort_values(by=['count'], ascending=False)
   

    return a

#>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Function for counting unique rows : is it going to show anything important here?

def count_unique_rows(df,column_name):
    
    l=len(df[column_name].drop_duplicates())
    
    return l
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#Additional function for representing association between ADR and corresponding drugs. Also, ploting this association 

def ADRs_drug_association(df):
    count_series =df1.groupby(['prefered_reaction_term', 'compound_drug']).size()
    new_df = count_series.to_frame(name = 'size').reset_index()
    new_df=new_df.sort_values(by=['size'], ascending=False)
    return new_df

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# There is a need to create a table with unique drugs which are similarly matched 

def unique_drug_matching(df):
    
    #c=np.unique(df[['product_name', 'adrs_drug']].values)
    df=df[['compound_drug','adrs_drug','primary_id']]
    c=df.drop_duplicates( subset=[ "compound_drug", "adrs_drug" ], keep="first", inplace=False, )
    
    return c
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#A function to a drug matching between two databases for one specific ADR
def drug_related_to_one_Adrs(df,adrs):
    df=df[['compound_drug','adrs_drug','prefered_reaction_term']]
    k=df.loc[df['prefered_reaction_term'] == adrs]
    k=k.drop_duplicates( subset=[ "compound_drug", "adrs_drug" ], keep="first", inplace=False)
    
    return k
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#A function for finding a ranking between compound drugs 

def ranking_compond_drugs(df):
    
    df=df.drop_duplicates( subset=[ "compound_drug", "adrs_drug","prefered_reaction_term"], keep="first", inplace=False)
    f=df.groupby(['compound_drug'], as_index=False).count()
    f=f.rename(columns={'Unnamed: 0':'count'})
    f=f[['compound_drug','count']].sort_values(by=['count'], ascending=False)
    
    
    return f
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# A function for finding the compound drugs withe same ADRs 
def compound_drugs_with_same_ADR(df1,reaction):
    #w = df1[df1.duplicated(['prefered_reaction_term'], keep=False)]
    w = df1.sort_values(by ='prefered_reaction_term' )
    w=w[['OrderID','InChI_Key','compound_drug','prefered_reaction_term']]
    if reaction:
        x=w.loc[w['prefered_reaction_term'] == reaction]
        
    else:
        x='empty'
    
    return w,x
#>>>>>>>><IMPLIMENTATION>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
start = time.time()
a=ranking_adrs(df)

b=a.head(30)
#>>>>>>>>>>>>>>>A direct script for the ploting the ADRs ranking>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<
np.random.seed(19680801)
plt.rcdefaults()
fig, ax = plt.subplots()

#Creat the x and y vectors for ploting 
ADRs=b["prefered_reaction_term"].tolist()
y_pos = np.arange(len(ADRs))
x_pos=b["count"].tolist()

ax.barh(y_pos, x_pos, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(ADRs,rotation=45)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Number of associated drugs')
ax.set_title('ADRS-drug association ranking')

plt.show()
#>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# l=count_unique_rows(df,"compound_drug")

# c=unique_drug_matching(df)
# h=ADRs_drug_association(df1)
# c.to_csv('Unique_drugs_matching.csv',index=False)
# h.to_csv('Adrs_drug_Association.csv')
# #ploting association between drugs in two databases
# k=drug_related_to_one_Adrs(df,'Anaemia')
# k.to_csv('drug_related_to_one_Adrs.csv')
# f=ranking_compond_drugs(df)
w,x=compound_drugs_with_same_ADR(df1,'Abdominal discomfort')
w.to_csv('compound_drugs_with_same_ADRs_new_information.csv')
# x.to_csv('compound_drugs_with_one_ADR.csv')
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>Ploting the ranking of compound drugs >>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
f1=f.head(30)
fig,ax = plt.subplots(1,1)
x = f1['compound_drug']
y1 = f1['count']
x_pos = range(len(x))
ax.set_ylabel('prefered_reaction_term_count',fontsize=13)
ax.set_xlabel('compound_drug',fontsize=13)
ax.bar(x, y1, label="Number of unique ADR")
fig.autofmt_xdate()
plt.legend(loc="upper right")
#>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<
time_end = time.time()
print("Elapsed", np.round(time_end-start, 2), "seconds")
