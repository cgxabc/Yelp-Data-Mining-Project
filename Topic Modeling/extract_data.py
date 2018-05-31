#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 19 22:00:16 2018

@author: apple
"""

import math
import json
import pickle
import random
import gensim
from gensim import models
from gensim.models import word2vec
from gensim import matutils
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from time import time
from nltk.tokenize import sent_tokenize
import glob
import argparse
import os

path2files = "yelp_dataset_challenge_academic_dataset/"
path2business=path2files+"yelp_academic_dataset_business.json"
path2reviews=path2files+"yelp_academic_dataset_review.json"

categories = set([])
restaurant_ids = set([])
cat2rid = {}
rest2rate = {}
rest2revID= {}
r = 'Restaurants'
with open(path2business, 'r') as f:
    for line in f.readlines():
        business_json = json.loads(line)
        bjc = business_json['categories']
       # print bjc #[u'Yelp Events', u'Local Flavor']
        if r in bjc:
            if len(bjc) > 1:
                restaurant_ids.add(business_json['business_id'])
                categories = set(bjc).union(categories) - set([r])
                stars = business_json['stars']
                rest2rate[business_json['business_id']] = stars
                for cat in bjc:
                    if cat == r:
                        continue
                    if cat in cat2rid:
                        cat2rid[cat].append(business_json['business_id'])
                    else:
                        cat2rid[cat] = [business_json['business_id']]
                    
print 'saving restaurant ratings'

with open ('restaurantIds2ratings.txt', 'w') as f:
   for key in rest2rate:
       f.write(key + " " + str(rest2rate[key]) + '\n')
## clearing from memory
rest2rate = None


with open('data_cat2rid.pickle','wb') as f:
    pickle.dump(cat2rid, f)
    
with open(path2reviews, 'r') as f:
    for line in f.readlines():
        review_json = json.loads(line)
        if review_json['business_id'] in restaurant_ids:
            if review_json['business_id'] in rest2revID:
                rest2revID[review_json['business_id']].append(review_json['review_id'])
            else:
                rest2revID[review_json['business_id']] = [review_json['review_id']]
                
with open('data_rest2revID.pickle','wb') as f:
     pickle.dump(rest2revID, f)                
                
                
###find the number of valid reviews in each (valid) category  
nz_count = 0   #number of category
valid_cats = []   
for i, cat in enumerate(cat2rid):
   cat_total_reviews = 0
   for rid in cat2rid[cat]:
       # number of reviews for each of restaurants
       if rid in rest2revID:
           cat_total_reviews += len(rest2revID[rid])
    
   if cat_total_reviews > 30:
       nz_count += 1
       valid_cats.append(cat)
       
       
print "sampling categories"

sample_rid2cat = {}
sample_size = 30   #or len(valid_cats)
#This specifies how many cuisines you would like to save
     
cat_sample = random.sample(valid_cats, sample_size) 
## restaurant id to category
for cat in cat_sample:
    for rid in cat2rid[cat]:
        if rid in rest2revID:
            if rid not in sample_rid2cat:
                sample_rid2cat[rid] = []
            sample_rid2cat[rid].append(cat)

#print sample_rid2cat                
#remove from memory
rest2revID = None

print "reading from review file..."

sample_cat2reviews = {}
sample_cat2ratings = {}
num_reviews = 0

with open(path2reviews, 'r') as f:
    for line in f.readlines():
        review_json = json.loads(line)
        rid = review_json['business_id']
        if rid in sample_rid2cat:
            num_reviews += 1
            for rcat in sample_rid2cat[rid]:
               # num_reviews += 1
                if rcat in sample_cat2reviews:
                    sample_cat2reviews[rcat].append(review_json['text'])
                    sample_cat2ratings[rcat].append(str(review_json['stars']))
                else:
                    sample_cat2reviews[rcat] = [review_json['text']]
                    sample_cat2ratings[rcat] = [str(review_json['stars'])]
 
#sampling categories     
save_categories = 0
if save_categories:  
    print 'saving categories'
    for cat in sample_cat2reviews:
        with open('categories/' + cat.replace('/','-').replace(" ", "_") + ".txt", 'w') as f:
 
            f.write(u'\n'.join(sample_cat2reviews[cat]).encode('utf-8').strip())
            
            
#print num_reviews  #225721
#sampling accumulated reviews     
save_sample = 0
if save_sample:
    print "sampling restaurant reviews"
    #save samples for restaurant reviews
    sample_size = min(20000, num_reviews)
    rev_sample = random.sample(range(num_reviews), sample_size)
    my_sample_v2 = []
    sample_ratings = []
    sorted_rev_sample = sorted(rev_sample)
    count = 0
    max_bound = 0
    sample_cat = {}
    for cat in sample_cat2reviews:
        new_max_bound = max_bound + len(sample_cat2reviews[cat])
        cat_count = 0
        while count < sample_size and sorted_rev_sample[count] < new_max_bound:
            my_sample_v2.append(sample_cat2reviews[cat][sorted_rev_sample[count] - max_bound].replace("\n", " ").strip())                 
            sample_ratings.append(sample_cat2ratings[cat][sorted_rev_sample[count] - max_bound])
            count += 1
            cat_count += 1
        max_bound = new_max_bound
        sample_cat[cat] = cat_count
        
        
    with open ("review_sample_20000.txt", 'w') as f:
        f.write('\n'.join(my_sample_v2).encode('ascii','ignore'))
        
    with open("review_ratings_20000.txt", 'w') as f:
        f.write('\n'.join(sample_ratings).encode('ascii','ignore'))
    
    with open("review_categories_20000.txt", 'w') as f:
        for cat, count in sample_cat.items():
            f.write(cat+'\t'+str(count)+'\n')
       
       
       
       
       
       
       
       
       
       
       
       
    
                
                
                
                
                
                
                
                
                
                
                
                
