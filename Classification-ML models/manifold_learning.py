#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 16:23:39 2021

@author: Shahabedin Chatraee Azizabadi

Manifold learning for the classification problelm
"""
import pandas as pd
from sklearn.decomposition import PCA,KernelPCA
from sklearn.manifold import Isomap,LocallyLinearEmbedding
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
#First step is to read the dataset and select the feature matrix

data_in=pd.read_csv('/Volumes/TOSHIBA/immunix_project/ADRs project/Classification/data_processed_for_classification.csv')


design_matrix=data_in.loc[:, '2_percentile_ascspecks_AreaShape_Area':]

#--Multicolinearity measure:VIF. WE impliment the VIF to compare the level of multicolinearity. generaly gives a value for
#-- each feature. 
def VIF_computation(X):
    
    vif = pd.DataFrame()  
    vif["features"] = X.columns # Here we choose the column labels of the data frame
    vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
   
    
    return vif



# Herein, we can define different functions for the dimensionality reduction

# The kernel PCA
def KPCA_al(X):
    kpca = KernelPCA(kernel='rbf',n_components=60, fit_inverse_transform=True, gamma=10)
    X_kpca = kpca.fit_transform(X)
    
    return X_kpca

# Herein, we use the principal component analysis PCA

def PCA_al(X):
    
    pca = PCA(n_components=60)
    X_principalComponents = pca.fit_transform(X)
    return X_principalComponents


#The second candidate is Isomap

def isomap_al(X):
    embedding = Isomap(n_neighbors=61,n_components=60)
    X_transformed = embedding.fit_transform(X)#[:100])
    return X_transformed 


#The third candidate is locally linear embeding
def local_lin_embed(X):
    embedding = LocallyLinearEmbedding(n_components=60)
    # We can have modified verion of LLE where n-neighbors>n-components
    #embedding = LocallyLinearEmbedding(method = 'modified',n_neighbors=61,n_components=60)
    X_transformed = embedding.fit_transform(X)
    
    return X_transformed

#------->>>><>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<>>><<<<<<<>>><<>><<>
# First, one should transfer the result of manifold learning to a data frame
# and also, one should join back the result to the original dataframe with the meta-data 
X_kpca=KPCA_al(design_matrix)
#X_isom=isomap_al(design_matrix)
X_lle=local_lin_embed(design_matrix)

col_list = ['feature' + str(x) for x in range(1,61)]
X_df_lle = pd.DataFrame(data =X_lle,columns=col_list)
X_df_kpca=pd.DataFrame(data =X_kpca,columns=col_list)
#X_df_isom=pd.DataFrame(data =X_isom,columns=col_list)
# joining back the result to the original dataframe
new_data_classification=data_in.loc[:,'barcode':'treatment'].join(X_df_lle, how='inner')
new_data_classification.to_csv('new_data_processed_for_classifi_lle_setup.csv')

#-----testing the VIF computation-----------
X=design_matrix.head(500)
vif1=VIF_computation(X_df_kpca)
vif2=VIF_computation(X_df_lle)
# #-------------------------------------------
# # Herein, we can impliment the plotting of VIF
x=['f' + str(x) for x in range(1,61)]
y1=vif1['VIF Factor']
y2=vif2['VIF Factor']
plt.plot(x, y1, 'b',linewidth=4.0) # 
plt.plot(x, y2, 'g',linewidth=4.0) # 
plt.xticks(rotation=45, ha='right')
plt.title('VIF for LLE and kPCA results')
plt.xlabel('Features',fontsize=13)
plt.ylabel('VIF Ratios',fontsize=13)
plt.legend(['VIF_kPCA','VIF_LLE'],loc="upper left",fontsize=11)
plt.show()


