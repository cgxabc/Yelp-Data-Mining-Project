#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 18:12:41 2017

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


cuisine_list=[]
cuisine_sim={}
with open('cuisine_indices.txt') as f:
    for line in f:
        cuisine_list+=[line.rstrip()]
#print cuisine_list
        
with open('cuisine_sim_matrix.csv','r') as f:
    reader = csv.reader(f)
    data_as_list = list(reader)
  #  for i in range(0,50):
      #  for j in range(0,50):
          #  cuisine_sim[cuisine_list[i]+cuisine_list[j]]=data_as_list[i][j]
#print cuisine_sim[cuisine_list[2]+cuisine_list[3]]
#print data_as_list[0][49]
##data_as_list[0] corresponds to the first row
        
            
            
def generateHeatmap(idfConfig):
	raw_data = go.Data([go.Heatmap(z = data_as_list, x = cuisine_list, y = cuisine_list, colorscale = 'Hot')])
	layout = go.Layout(title = 'cuisine_similarity_' + idfConfig, xaxis = dict(ticks = ''), yaxis = dict(ticks = ''),font=dict(size=10))
	fig = go.Figure(data = raw_data, layout = layout)
	url = py.plot(fig, filename = 'cuisine_similarity_' + idfConfig, validate = True)
    
    
def main():    
  generateHeatmap('LDA+TFIDF')
  #print data_as_list

if __name__ == '__main__':
    main()