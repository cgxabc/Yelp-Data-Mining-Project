f1 = open("review_ratings_100000.txt")
f2=open("review_sample_100000.txt")
count_1=0
count_2=0
count_3=0
count_4=0
count_5=0


ratings=[]

for rating in f1:
    ratings.append(rating.rstrip())
    
#print ratings   
print len(ratings)


reviews=[]
for line in f2:
    reviews.append(line.rstrip())
    
#print reviews
print len(reviews)
    
 ##100000 

for i in range(len(ratings)):  
    
   if ratings[i]=='1':
        count_1+=1
        
   if ratings[i]=='2':
        count_2+=1   
        
   if ratings[i]=='3':
        count_3+=1
        
   if ratings[i]=='4':
        count_4+=1   
        
   if ratings[i]=='5':
        count_5+=1   
        

        
print ("rating 1 counts: "+str(count_1))   #8532
        
print ("rating 2 counts: "+str(count_2))  #9927

print ("rating 3 counts: "+str(count_3))  #16446
        
print ("rating 4 counts: "+str(count_4))   #34145

print ("rating 5 counts: "+str(count_5))  #30950
        
