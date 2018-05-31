#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 13:50:50 2017

@author: apple
"""

import os
import numpy as np
import csv
import pandas as pd
import plotly
plotly.tools.set_credentials_file(username='your_own_username', api_key='your_own_apikey')
import plotly.plotly as py
import plotly.graph_objs as go
from sklearn.cluster import KMeans, AgglomerativeClustering

cuisine_list=[]
cuisine_sim={}
with open('cuisine_indices.txt') as f:
    for line in f:
        cuisine_list+=[line.rstrip()]
#print cuisine_list
        
with open('cuisine_sim_matrix.csv','r') as f:
    reader = csv.reader(f)
    data_as_list = list(reader)
    for i in range(0,50):
        for j in range(0,50):
            cuisine_sim[cuisine_list[i]+cuisine_list[j]]=data_as_list[i][j]
#print cuisine_sim[cuisine_list[2]+cuisine_list[3]]
#print data_as_list[0][49]
##data_as_list[0] corresponds to the first row
cluster_num=7
#cluster=KMeans(n_clusters=cluster_num)
cluster = AgglomerativeClustering(n_clusters=cluster_num)
cluster.fit(data_as_list)
y=cluster.labels_.tolist()
# print y  
#[2, 3, 0, 3, 3, 4, 4, 3, 3, 3, 4, 0, 4, 4, 4, 0, 0, 5, 2, 4, 4, 4, 0, 0, 4, 4, 0, 3, 0, 1, 6, 1, 1, 1, 6, 4, 0, 2, 0, 6, 2, 4, 0, 3, 0, 4, 4, 1, 5, 6]
new_order=[]
new_index=[]
for i in range(0,cluster_num):
    list_i=[]
    for j in range(0,50):
        if y[j]==i:
          list_i.append(j)
          new_index.append(j)
    new_order.append(list_i)
        
print new_order
print new_index

new_cuisine_list = [0]*50

for i in range(0,50):
    new_cuisine_list[i]=cuisine_list[new_index[i]]

new_cuisine_group=range(cluster_num)

for i in range(0,cluster_num):
    new_cuisine_group[i]=range(len(new_order[i]))
    for j in range(0, len(new_order[i])):
        new_cuisine_group[i][j]=cuisine_list[new_order[i][j]]
        
        
print new_cuisine_group
print new_cuisine_list
        
data=[]
for i in range(0,50):
    new_row=[]
    for j in range(0,50):
        new_row.append(data_as_list[new_index[i]][new_index[j]])
    data.append(new_row)
    
def generateHeatmap(idfConfig):
	raw_data = go.Data([go.Heatmap(z = data, x = new_cuisine_list, y = new_cuisine_list, colorscale = 'Viridis')])
	layout = go.Layout(title = 'cuisine_similarity_with_%s_clusters_'%cluster_num + idfConfig, xaxis = dict(ticks = ''), yaxis = dict(ticks = ''),font=dict(size=10))
	fig = go.Figure(data = raw_data, layout = layout)
	url = py.plot(fig, filename = 'cuisine_similarity_with_%s_clusters_'%cluster_num + idfConfig, validate = True)
    
    
def main():    
  generateHeatmap('LDA+TFIDF')
  

if __name__ == '__main__':
    main()



























