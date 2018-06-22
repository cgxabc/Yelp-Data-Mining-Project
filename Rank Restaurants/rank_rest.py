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

class Rank_Rest(): 
 ##constructed reviews which are dictionaries of text, rating, voting and rest id.     
     def load_reviews(self):
         self.reviews = []
         with open('Chinese.txt') as fh:
             for line in fh.readlines():
                 if not line: break
                 self.reviews.append({'text': line.strip()})
            # print len(self.reviews)  #38716
         with open('Chinese.review_info.txt') as fh:
             lineno = 0
             for line in fh.readlines():
                 if not line: break
                 rate, vote, rest = line.strip().split('\t')
                 vote = json.loads(vote)
                 self.reviews[lineno]['rate'] = rate
                 self.reviews[lineno]['vote'] = vote
                 self.reviews[lineno]['rest'] = rest
                 lineno += 1  
 ##constructed dictionary of rest id with associated reviews
     def rest_to_review(self):         
         self.rest_review={}        
         for review in self.reviews:
             if review['rest'] not in self.rest_review:
                   self.rest_review[review['rest']] = []
             self.rest_review[review['rest']].append(review)  
         
     def rest_to_score(self,dish_list):        
         rest_score={}
         for rest, reviews in self.rest_review.items():
              score = 0
              denom = 0
              review_dish_count = 0
              review_count = 0
              rating_all = 0
              sentiment_all = 0
              for review in reviews:  #consider each piece of review for one rest
                    text=review['text'].decode('utf-8').lower()
                    rate=review['rate']
                    vote=review['vote']['useful'] + review['vote']['funny'] + review['vote']['cool']                                       
                    for dish in dish_list:
                        if dish not in text: continue
                        review_count += 1
                        if rate == '5' or rate == '4':
                            sentiment_all += 1
                        elif rate == '2' or rate == '1':
                            sentiment_all -= 1     
                                
                    for dish in dish_list:
                       for sent in sent_tokenize(text):
                           if dish not in sent: continue
                           review_dish_count += 1
                           score += (1+vote)*int(rate)
                           denom += 1+vote    
                           
              if review_count == 0:
                 rest_score[rest] = 0
              else:
                 ave_sentiment = float(sentiment_all)/review_count
                 exp_sentiment = math.exp(ave_sentiment)
                 ave_rating = float(score)/denom  
                 rest_score[rest] = math.log(1 + review_dish_count)*ave_rating*exp_sentiment
                # rest_score[rest] = [math.log(1 + review_dish_count)*ave_rating*exp_sentiment,review_dish_count, review_count, ave_sentiment, ave_rating]                                              
         with open('rest_id2rest_name.json') as fh:
            rest_id2rest_name = json.load(fh)
           
         rest_name_score={}         
         for rest in rest_score.keys():
            if rest_score[rest] > 0:  #the score is positive 
               rest_name_score[rest_id2rest_name[rest]]=rest_score[rest]
     
         with open(os.path.join('/Users/apple/Desktop/Yelp_reviews_new/task4&5', '%s_rest2score'% '&'.join(str(dish.replace(" ","_")) for dish in dish_list)), 'w') as fh:
             for rest, score in sorted(rest_name_score.items(), key = lambda x: x[1], reverse = True):
                 fh.write(rest + "\t" + str(score) +"\n" )
            #for rest, score in sorted(rest_name_score.iteritems(),key=lambda(k,v):(v,k),reverse=True):
           # for rest, score_list in sorted(rest_name_score.items(), key = lambda x: x[1][0], reverse = True):
             #   fh.write(rest+"\t"+"\t".join(str(score_list[i]) for i in range(len(score_list)))+"\n")
   
def main():
    rest_rank=Rank_Rest()
    rest_rank.load_reviews()
    rest_rank.rest_to_review()
    rest_rank.rest_to_score(['buffet'])
        
if __name__ == '__main__':
    
    main()
