#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 23:34:44 2017

@author: apple
"""

import json
import os
import logging
import json
import os
import logging
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import math
from scipy.stats import logistic



class RankRest(): 
     
     def load_reviews(self):
             self.reviews = []
             with open('Chinese.txt') as fh:
                 for line in fh.readlines():
                    if not line: break
                    self.reviews.append({'text': line.strip()})
                   # '-mz0Zr0Dw6ZASg7_ah1R8A' 

             with open('Chinese.review_info.txt') as fh:
                    lineno = 0
                    for line in fh.readlines():
                         if not line: break
                         rate, vote, rest = line.split('\t')
                         vote = json.loads(vote)
                        # self.reviews[lineno].update({'rate': rate})
                        # self.reviews[lineno].update({'vote': vote})
                       #  self.reviews[lineno].update({'rest': rest.rstrip()})
                         self.reviews[lineno]['rate'] = rate
                         self.reviews[lineno]['vote'] = vote
                         self.reviews[lineno]['rest'] = rest.rstrip()
                         lineno+=1               
                
     def rest_to_review(self):
         
         self.rest_review={}
        
         for review in self.reviews:
            # print review['rest']
             if review['rest'] not in self.rest_review:
                   self.rest_review[review['rest']] = []
             self.rest_review[review['rest']].append(review)
        # print self.rest_review['-mz0Zr0Dw6ZASg7_ah1R8A']
        
     def rest_to_score(self,dish_list):
        
         rest_score={}
         for rest, reviews in self.rest_review.items():
              score = 0
              denom = 0
              rate_all=0
              for review in reviews:
                    text=review['text'].decode('utf-8').lower()
                    rate=review['rate']
                    vote=review['vote']['useful']
                    review_count=0
                    rate_all+=int(rate)
                 
                    if rate=='5' or rate=='4':
                       for dish in dish_list:
                           if dish in text:
                              review_count+=1
                    
                    for sent in sent_tokenize(text):
                        for dish in dish_list:
                           if dish in sent: 
                              score += (1+vote)*int(rate)
                              denom += 1+vote 
                              
              ave_rate=rate_all/float(len(reviews))
                                      
              if denom==0:
                 rest_score[rest]=0
              else:
                 #rest_score[rest]=math.log(1+float(score/denom))*math.log(ave_rate)*logistic.cdf(review_count)
                 rest_score[rest]=math.log(1+float(score/denom))*logistic.cdf(review_count)
                 #rest_score[rest]=review_count
                
                 
         with open(os.path.join('/Users/apple/Desktop/data_mining_capstone/output', 'rest_id2rest_name.json')) as fh:
            rest_id2rest_name = json.load(fh)
            #for rest in rest_score.keys():
             #    print rest_id2rest_name[rest]
         rest_pos_score={}         
         for rest in rest_score.keys():
             if rest_score[rest]>0:
                 rest_pos_score[rest_id2rest_name[rest]]=rest_score[rest]
     
         with open(os.path.join('/Users/apple/Desktop/data_mining_capstone/output', '%s_rest2score2'% dish_list), 'w') as fh:
            for rest, score in sorted(rest_pos_score.iteritems(),key=lambda(k,v):(v,k),reverse=True):
                fh.write(rest+"\t"+str(score)+"\n")
            
   #  print rest+":"+str(rest_score[rest])+'\n'
               
     #1MRWXUsIvKNwt5SdLxqhZA:1.60943791243

     #xzEhmFvpuS_MlmMNTh2egg:1.38629436112          
               
               
   
def main():
    restcount=RankRest()
    restcount.load_reviews()
    restcount.rest_to_review()
    restcount.rest_to_score(['dim sum'])


        
if __name__ == '__main__':
    
    main()
