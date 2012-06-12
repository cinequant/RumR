#-*- coding: utf-8 -*-
'''
Created on Apr 18, 2012

@author: rafael
'''
import Joker
import IteratorWords
import FeaturesTree
import pickle
import numpy
import time
import cPickle

any_word=Joker.any_word


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
        if (count==10000):
            count=0
            print features[" "]
        #for each iterated word, three refreshed features    
        '''##first feature: stars number
        try:
            features[(i.stars)] +=1
            positions[(i.stars)].add(i.global_index)
        except:
            features[(i.stars)]=1
            positions[(i.stars)]=set([i.global_index])'''
        ##second feature: stars number+word
        try:
            features[(i.stars, any_word, i.word)]+=1
            positions[(i.stars, any_word, i.word)].add(i.global_index)
        except:
            features[(i.stars, any_word, i.word)]=1
            positions[(i.stars, any_word, i.word)]=set([i.global_index])
        ##third feature: stars number+word+previous word
        try:
            features[(i.stars, i.words[1], i.word)]+=1
            positions[(i.stars, i.words[1], i.word)].add(i.global_index)
        except:
            features[(i.stars, i.words[1], i.word)]=1
            positions[(i.stars, i.words[1], i.word)]=set([i.global_index])
        ##fourth feature: word+previous word    
        try:
            features[(any_word, i.words[1], i.word)]+=1
            positions[(any_word, i.words[1], i.word)].add(i.global_index)
        except:
            features[(any_word, i.words[1], i.word)]=1
            positions[(any_word, i.words[1], i.word)]=set([i.global_index])               
    return [features,positions]


def historic(): 
    print "start historic()"
    result={}
    Iter=IteratorWords.IteratorWords()
    for i in Iter:
        try:
            result[(any_word, i.words[1])]+=1
        except:
            result[(any_word, i.words[1])]=1
        try:
            result[(i.stars, any_word)]+=1
        except:
            result[(i.stars, any_word)]=1
        try:
            result[(i.stars,i.words[1])]+=1
        except:
            result[(i.stars,i.words[1])]=1   
    print "end historic()"
    return result

#insertion dicotomique
def insertion(tup,values,L,first,last):
    '''as used in select_features'''
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
    for index in range(n):
        result[index]=result[index][0]        
    return result
    
'''feat=write_features()
#recording our features in a file
pickle.dump(feat,open("features file","w"))
print "file ok"
pickle.load(open("features files"))    
print "the end"'''
        
'''feat=write_features()
D=feat[0]
hist=historic()
print 'ok!'
print len(hist)
print 'ok'         
#Sel=select_features(D,100)
#print Sel'''

'''Feat=write_features()
c_Sel=select_features(Feat[0],10000)
#recording our features in a file
cPickle.dump(c_Sel,open("10000 selected features file with cPickle","w"))'''


'''
#using our features file
Sel=pickle.load(open("10000 selected features file"))
print 'Sel ok!'
print
print 'creating our features tree: representation of all possible triple (x,y) '
tree=FeaturesTree.FeaturesTree()
tree.write_tree(Sel)
print 'tree: OK!'
#pickle.dump(tree,open("Tree with 10000 selected features file","w"))
#print tree.get_features()
print
print 'counting the empirical distributions'
tree.count_occurences()
print 'finish counting'
t0=time.time()
print 'start new_features'
S=tree.new_features()
print 'end of new_features'
t1=time.time()
t=t1-t0
print 'temps d execution de new_features avec un dict :'+str(t)
print 'ok!'
n=len(S)
print n
lamb=numpy.linspace(0,0,n)
print
print 'calculating conditional probability for lambda equals to zero'
tree.p_lambda(lamb,S,n)'''