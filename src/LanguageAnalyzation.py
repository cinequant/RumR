'''
Created on Apr 10, 2012

@author: rafael
'''
import MySQLdb
import re
import string

def countWords(myTable):
    allWords=[]
    values=[]
    for comment in myTable:
        p=re.findall('\w+|[,;.!?]', comment)
        for word in p:
            if values.__contains__(word)==False:
                values.insert(0,word)
        allWords=allWords+p
    for value in values:
        n=allWords.count(value)
        print [value, n]
        
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
    #countWords
    #modif
    allWords=[]
    values=[]
    for t in cursor.fetchall():
        print t[0]
        print t
        p=re.findall('[^\s,;.!?]+|[,;.!?]', t[0])
        print p
        for word in p:
            if values.__contains__(word)==False:
                values.insert(0,word)
                print "insertion : OK!"
        allWords=allWords+p
    for value in values:
        n=allWords.count(value)
        if n>10:
            print [value, n]
    
    
    
    
#test()    
getLabeledComments(5)
