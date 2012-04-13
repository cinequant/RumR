#-*- coding: utf-8 -*-
'''
Created on Apr 10, 2012

@author: rafael
'''

from __future__ import division
import MySQLdb
import re
import operator
import math



def count_words(myTable):
    #replace vector for dict(hashmap for python)
    dictionary={}
    for comment in myTable:
        p=re.findall('\w+|[,;.!?]', comment)
        for word in p:
            if word not in dictionary: 
                dictionary.insert(word,1)
            else: 
                dictionary[word]=dictionary.get(word)+1
                print dictionary[word]
               
        
        
def test():
    s=" No meio do caminho tinha uma pedra tinha uma pedra no meio do caminho tinha uma pedra no meio do caminho tinha uma pedra. Nunca me esquecerei desse acontecimento na vida de minhas retinas tao fatigadas. Nunca me esquecerei que no meio do caminho tinha uma pedra tinha uma pedra no meio do caminho no meio do caminho tinha uma pedra"
    p=re.findall('\w+|[,;.!?]', s)
    p=p+p
    print p
    myTable=[s,s,s]
    count_words(myTable)
    
def get_cursor(stars):
    db=MySQLdb.connect("cinequant.com","rafael","nqq2612","rafael",use_unicode=True,charset="utf8")
    cursor=db.cursor()
    query="""SELECT `review` FROM `rafael`.`cinefrance_moviereviews` WHERE `rating`=%s"""%stars
    cursor.execute(query)
    return cursor    

def get_labeled_comments(stars):
    cursor=get_cursor(stars)
    dictionary={"total of comments":cursor.rowcount}
    for t in cursor.fetchall():
        p=re.findall('[^\s,;.!?]+|[,;.!?]', t[0])
        for word in p:
            word=word.lower()
            if word in dictionary: #
                dictionary[word]=dictionary.get(word)+1
                #print dictionary[word]
            else: 
                dictionary[word]=1
                
    '''for duple in sorted(dictionary.iteritems(),key=operator.itemgetter(1),reverse=True):
        if duple[1]>50:
            print duple'''
    return dictionary        
    
def feature_one_word(comment,words):
    features=[]
    index=0
    for word in words:
        if re.search(word, comment):
            features[index]=1
        else:
            features[index]=0
        index=index+1            
    return features

'''def feature_two_words(comment,phrases):
    features=[]
    index=0
    for phrase in phrases:
        if re.search(word, comment):
            features[index]=1
        else:
            features[index]=0
        index=index+1            
    return features'''

#doit-on compter plusieurs fois un mot qui apparait plus d'une fois par message ?
##OUI
def frequency_of(cle):
    print 'How many times did the word '+cle+' appears in average in comments with:'
    for i in (5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5):
        print object.__str__(i)+' stars'
        D=get_labeled_comments(i)
        if cle in D:
            print D[cle] / D["total of comments"]
        else:
            print 0    
        print
    
def density_of(cle):
    P=[0,0,0,0,0,0,0,0,0,0]
    Q=[0,0,0,0,0,0,0,0,0,0]
    index=0
    for i in (5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5):
        D=get_labeled_comments(i)
        Q[index]=D["total of comments"]
        if cle in D:
            P[index]=D[cle] 
        else:
            P[index]=0
        index=index+1
    Sp=sum(P)
    Sq=sum(Q)
    while (index>0):
        index=index-1
        P[index]=P[index]/Sp
        Q[index]=Q[index]/Sq
    print "density function of appearance of the word "+cle+" :"
    print P
    print
    print "density function of rating of a comment :"
    print Q
    print 
    return [P,Q]

def divergence_KL(cle):
    dens=density_of(cle)
    DKL=0
    index=0
    while (index<len(dens[0])):
        DKL=DKL+dens[0][index]*math.log(dens[0][index]/dens[1][index])
        index=index+1
    print "Significance of the word "+cle+" :"
    print DKL
#test()    
cle=u"depardieu"
divergence_KL(cle)