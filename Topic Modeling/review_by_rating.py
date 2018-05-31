#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 17:11:48 2017

@author: apple
"""

f1 = open("review_sample_100000.txt")
f2 = open("review_ratings_100000.txt")

dict={}

#for line in f1:
    
   # print (line.rstrip()+" "+f2.readline().strip()+'\n')

for line in f1:
    dict[line.rstrip()]=f2.readline().strip()
    
#print dict
text_positive=[]
rating_positive=[]

text_negative=[]
rating_negative=[]

text_neutral=[]
#rating_neutral=[]
for text in dict.keys():
    if dict[text]=='4' or dict[text]=='5' :
       text_positive.append(text)  
       rating_positive.append(dict[text])
    if dict[text]=='1' or dict[text]=='2' :
       text_negative.append(text)  
       rating_negative.append(dict[text])
    if dict[text]=='3':  
       text_neutral.append(text)  
       #rating_neutral.append(dict[text])
        

#print text_positive, rating_positive
#print text_negative, rating_negative
#print text_neutral
        

with open ("review_sample_100000_positive.txt", 'w') as f:
   f.write('\n'.join(text_positive).encode('ascii','ignore') )
            
with open ("review_ratings_100000_positive.txt", 'w') as f:
   f.write('\n'.join(rating_positive).encode('ascii','ignore') )


with open ("review_sample_100000_negative.txt", 'w') as f:
   f.write('\n'.join(text_negative).encode('ascii','ignore') )
            
with open ("review_ratings_100000_negative.txt", 'w') as f:
   f.write('\n'.join(rating_negative).encode('ascii','ignore') )


with open ("review_sample_100000_neutral.txt", 'w') as f:
   f.write('\n'.join(text_neutral).encode('ascii','ignore') )


