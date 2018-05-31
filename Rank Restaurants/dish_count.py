#! /usr/bin/env python2

import json
import os
import logging

class IndexYelpReviews():
    
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

    def index_dish2review(self, dish_path):
        dish2review = {}
        dish2counts={}
        with open(dish_path) as fh:
            for line in fh.readlines():
                dish = line.strip()
                dish2review[dish] = []
            

        for idx, review in enumerate(self.reviews):
            text = review['text'].lower()
            for dish in dish2review:
                if dish not in text: continue
                dish2review[dish].append(idx)
                
            for dish, review in dish2review.items():
                dish2counts[dish]=len(review)
           
                

        with open('dish2review', 'w') as fh:
            for dish, review in dish2review.items():
                fh.write('%s\t%s\n' % (dish, ' '.join([str(i) for i in review])))
                
        with open('dish2allcounts', 'w') as fh:
            for dish, count in sorted(dish2counts.iteritems(),key=lambda(k,v):(v,k),reverse=True):
                fh.write(dish+"\t"+str(count)+"\n")
            
            


if __name__ == '__main__':
    indexer = IndexYelpReviews()
    indexer.load_reviews()
    #indexer.index_dish2review('./resource/chinese_dn_annotations.txt')
    indexer.index_dish2review('Chinese_dish_names.txt')

