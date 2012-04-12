'''
Created on Apr 10, 2012

@author: rafael
'''
import MySQLdb
import re
import operator

def countWords(myTable):
    allWords=[]
    #replace vector for dict(hashmap for python)
    dictionary=dict(one=1, two=2)
    for comment in myTable:
        p=re.findall('\w+|[,;.!?]', comment)
        for word in p:
            if word not in dictionary: #
                dictionary.insert(word,1)#
            else: 
                dictionary[word]=dictionary.get(word)+1
                print dictionary[word]
               # dictionary.get(k)=dictionary.get(word)+1
        #do a sort
        
        
def test():
    s=" No meio do caminho tinha uma pedra tinha uma pedra no meio do caminho tinha uma pedra no meio do caminho tinha uma pedra. Nunca me esquecerei desse acontecimento na vida de minhas retinas tao fatigadas. Nunca me esquecerei que no meio do caminho tinha uma pedra tinha uma pedra no meio do caminho no meio do caminho tinha uma pedra"
    p=re.findall('\w+|[,;.!?]', s)
    p=p+p
    print p
    myTable=[s,s,s]
    countWords(myTable)
    

def getLabeledComments(stars):
    db=MySQLdb.connect("cinequant.com","rafael","nqq2612","rafael",use_unicode=True,charset="utf8")
    cursor=db.cursor()
    query="""SELECT `review` FROM `rafael`.`cinefrance_moviereviews` WHERE `rating`=%s"""%stars
    cursor.execute(query)
    dictionary={}
    for t in cursor.fetchall():
        p=re.findall('[^\s,;.!?]+|[,;.!?]', t[0])
        for word in p:
            if word in dictionary: #
                dictionary[word]=dictionary.get(word)+1
                print dictionary[word]
            else: 
                dictionary[word]=1
                
    '''for duple in sorted(dictionary.iteritems(),key=operator.itemgetter(1),reverse=True):
        if duple[1]>50:
            print duple'''
    return dictionary        
    
        #n=allWords.count(value)
        #if n>10:
         #   print [value, n]
    
    
    
    

