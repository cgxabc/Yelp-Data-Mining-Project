#! /usr/bin/env python2

import json
import os
import logging
import math

class Dish_Reviews():
    
    def load_reviews(self):
        self.reviews = []
        with open('Chinese.txt') as fh:
            for line in fh.readlines():
                if not line: break
                self.reviews.append({'text': line.strip()})

        with open('Chinese.review_info.txt') as fh:
            lineno = 0
            for line in fh.readlines():
                if not line: break
                rate, vote, rest = line.split('\t')
                vote = json.loads(vote)
                self.reviews[lineno]['rate'] = rate
                self.reviews[lineno]['vote'] = vote
                self.reviews[lineno]['rest'] = rest.rstrip()
                lineno+=1
       # print self.reviews
    def dish_to_review(self, dish_name):
        dish_review = {}
        dish_counts={}
        dish_score = {}
        dish_sentiment = {}
        with open(dish_name) as fh:
            for line in fh.readlines():
                dish = line.strip()
                dish_review[dish] = []
                dish_sentiment[dish] = 0
                
        for lineno, review in enumerate(self.reviews):
            text = review['text'].lower()
            rate = review['rate']
            for dish in dish_review:
                if dish not in text: continue
                dish_review[dish].append(lineno)
                if rate == '5' or rate == '4':
                    dish_sentiment[dish] += 1
                elif rate == '2' or rate == '1':
                    dish_sentiment[dish] -= 1              
                
        for dish, review_no in dish_review.items():
                dish_counts[dish]=len(review_no)
                
        for dish in dish_sentiment.keys():
            if dish_counts[dish] == 0:
                dish_sentiment[dish] = 0
            else:
                dish_sentiment[dish] = float(dish_sentiment[dish])/dish_counts[dish] 
            #dish_score[dish] = math.exp(dish_sentiment[dish])*dish_counts[dish]
            dish_score[dish] = [math.exp(dish_sentiment[dish])*dish_counts[dish],dish_sentiment[dish], dish_counts[dish]]        
        with open('dish_to_review', 'w') as fh:
            for dish, review in dish_review.items():
                fh.write('%s\t%s\n' % (dish, ' '.join([str(i) for i in review])))
                
        with open('dish_to_counts', 'w') as fh:
            for dish, count in sorted(dish_counts.iteritems(),key=lambda(k,v):(v,k),reverse = True):
                fh.write(dish+"\t"+str(count)+"\n")
                
        with open('dish_to_score_full','w') as fh:
           # for dish, score in sorted(dish_score.iteritems(),key = lambda(k,v): (v,k), reverse = True):
              #  fh.write(dish +"\t"+str(score)+"\n")
           for dish, score_list in sorted(dish_score.items(), key = lambda x: x[1][0], reverse = True):
               fh.write(dish+"\t"+"\t".join(str(score_list[i]) for i in range(len(score_list)))+"\n")


if __name__ == '__main__':
    dish_rank = Dish_Reviews()
    dish_rank.load_reviews()
    dish_rank.dish_to_review('Chinese_dish_names.txt')

