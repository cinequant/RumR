#-*- coding: utf-8 -*-
'''
Created on Apr 18, 2012

@author: rafael
'''
import IteratorWords
import pickle
import numpy

def write_features():
    '''returns a dictionary where the keys are the different features and its keys are how any times it appears'''
    features={" ":0}
    positions={}
    Iter=IteratorWords.IteratorWords()
    count=0
    for i in Iter:
        features[" "] +=1
        count+=1
        if (count==100):
            count=0
            print features[" "]
        #for each iterated word, four refreshed features 
        ##first feature: stars number
        try:
            features[(i.stars)] +=1
            positions[(i.stars)].add(i.global_index)
        except:
            features[(i.stars)]=1
            positions[(i.stars)]=set([i.global_index])
        ##second feature: stars number+word
        try:
            features[(i.stars, i.word)] +=1
            positions[(i.stars, i.word)].add(i.global_index)
        except:
            features[(i.stars, i.word)]=1
            positions[(i.stars, i.word)]=set([i.global_index])
        ##third feature: stars number+word+previous word
        try:
            features[(i.stars, i.word, i.words[1])] +=1
            positions[(i.stars, i.word, i.words[1])].add(i.global_index)
        except:
            features[(i.stars, i.word, i.words[1])]=1
            positions[(i.stars, i.word, i.words[1])]=set([i.global_index])
        '''##fourth feature: word+previous word    
        try:
            features[(i.stars, i.word, i.words[1])] +=1
            positions[(i.stars, i.word, i.words[1])].add(i.global_index)
        except:
            features[(i.word, i.words[1])]=1
            positions[(i.word, i.words[1])]=set([i.global_index])'''               
    return [features,positions]

#insertion dicotomique
def insertion(tup,values,L,first,last):
    if (values[tup]>=values[L[first]]):
        L.insert(first,tup)
    elif (values[tup]<=values[last]):
        L.insert(last+1,tup)
    elif (values[tup]>=values[(first+last)/2]):
        insertion(tup,values,L,first,(first+last)/2) 
    else:
        insertion(tup,values,L,(first+last)/2,last)            

def select_features(features,n):
    '''takes a dictionary of features and selects the n with the biggest number of appearances'''
    try:
        del features[" "]
    #set of select features 
    except:
        print 'o.O'
    result=[]
    for key in features.keys():
        if (len(result)==0):
            result.append(key)
        insertion(key,features,result,0,len(result)-1)
        if (len(result)>n):
            result.pop(-1)    


'''feat=write_features()
#recording our features in a file
pickle.dump(feat,open("features file","w"))
print "file ok"
pickle.load(open("features files"))    
print "the end"           '''  
        
feat=pickle.load(open("features file"))
print 'ok!'
D=feat[0]
print 'ok'         
Sel=select_features(D,10)
print Sel  
