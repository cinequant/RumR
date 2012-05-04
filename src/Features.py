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
    '''why a dictionary: faster insertions'''
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
        #for each iterated word, five refreshed features    
        '''##first feature: stars number
        try:
            features[(i.stars)] +=1
            positions[(i.stars)].add(i.global_index)
        except:
            features[(i.stars)]=1
            positions[(i.stars)]=set([i.global_index])'''
        ##second feature: stars number+word
        try:
            features[(i.stars, i.word)] +=1
            positions[(i.stars, i.word)].add(i.global_index)
        except:
            features[(i.stars, i.word)]=1
            positions[(i.stars, i.word)]=set([i.global_index])
        ##third feature: stars number+word+previous word
        try:
            features[(i.stars, i.words[1], i.word)] +=1
            positions[(i.stars, i.words[1], i.word)].add(i.global_index)
        except:
            features[(i.stars, i.words[1], i.word)]=1
            positions[(i.stars, i.words[1], i.word)]=set([i.global_index])
        ##fourth feature: word+previous word    
        try:
            features[(i.words[1], i.word)] +=1
            positions[(i.words[1], i.word)].add(i.global_index)
        except:
            features[(i.words[1], i.word)]=1
            positions[(i.words[1], i.word)]=set([i.global_index])               
    return [features,positions]

#insertion dicotomique
def insertion(tup,values,L,first,last):
    if (values[tup]>=values[L[first][0]]):
        L.insert(first,(tup,values[tup]))
    elif (values[tup]<=values[L[last][0]]):
        L.insert(last+1,(tup,values[tup]))
    elif (last-first==1):
        L.insert(last,(tup,values[tup]))
    elif (values[tup]>=values[L[(first+last)/2][0]]):
        insertion(tup,values,L,first,(first+last)/2) 
    else:
        insertion(tup,values,L,(first+last)/2,last)
        
def historic():
    print "start historic()"
    result={}
    Iter=IteratorWords.IteratorWords()
    for i in Iter:
        try:
            result[(i.words[1])] +=1
        except:
            result[(i.words[1])]=1
        try:
            result[(i.stars)] +=1
        except:
            result[(i.stars)]=1
        try:
            result[(i.words[1],i.stars)] +=1
        except:    
            result[(i.words[1],i.stars)]=1        
    print "end historic()"
    return result      

def select_features(features,n):
    '''takes a dictionary of features and selects the n with the biggest number of appearances'''
    '''why a list: need to have an order'''
    try:
        del features[" "]
    #set of select features 
    except:
        print 'o.O'
    result=[]
    for key in features.keys():
        if (len(result)==0):
            result.append((key,features[key]))
        insertion(key,features,result,0,len(result)-1)
        if (len(result)>n):
            result.pop(-1)    
    return result

def parameters(sel):
    n=len(sel)
    weights=numpy.arange(n)
    
    
'''feat=write_features()
#recording our features in a file
pickle.dump(feat,open("features file","w"))
print "file ok"
pickle.load(open("features files"))    
print "the end"           '''  
        
feat=write_features()
hist=historic()
print 'ok!'
D=feat[0]
print 'ok'         
Sel=select_features(D,100)
print Sel
