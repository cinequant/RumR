#-*- coding: utf-8 -*-
'''
Created on Apr 10, 2012

@author: rafael
'''

from __future__ import division
import MySQLdb
import re
import operator
import numpy 
import string

        
def safe_x_log_x(x):
    l=numpy.log(x)
    l[numpy.isneginf(l)]=0
    return numpy.dot(x,l)        
        
def test():
    s="Je n'ai pas oublié, voisine de la ville, Notre blanche maison, petite mais tranquille ; Sa Pomone de plâtre et sa vieille Vénus Dans un bosquet chétif cachant leurs membres nus, Et le soleil, le soir, ruisselant et superbe, Qui, derrière la vitre où se brisait sa gerbe, Semblait, grand oeil ouvert dans le ciel curieux, Contempler nos dîners longs et silencieux, Répandant largement ses beaux reflets de cierge Sur la nappe frugale et les rideaux de serge." 
    p=re.findall('[^\s\',;.!?/()«»\’]+|[;!?«»]', s)
    p=p+p
    print p
    myTable=[s,s,s]
    count_words(myTable)

def count_words(myTable):
    #replace vector for dict(hashmap for python)
    dictionary={}
    for comment in myTable:
        T=string.replace(comment, '’', '\'')
        p=re.findall('[^\s\',;.!?()/«»]+|[;!?«»]', T)
        for word in p:
            if word not in dictionary: 
                dictionary.insert(word,1)
            else: 
                dictionary[word]=dictionary.get(word)+1
                print dictionary[word]
               
    
def get_reviews_cond_stars(stars):
    db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    cursor=db.cursor()
    query="""SELECT `review` FROM `rafael`.`cinefrance_moviereviews` WHERE `rating`=%s"""%stars
    cursor.execute(query)
    myTable=cursor.fetchall()
    return myTable    


def get_labeled_comments(stars):
    table=get_reviews_cond_stars(stars)
    dictionary={}
    for t in table:
        T=string.replace(t[0], '’', '\'')
        p=re.findall('[^\s\',;.!?()/«»]+|[;!?«»]', T)
        for i in range(len(p)):
            word=p[i].lower()
            if i==0:
                previous_word=None
            else:
                previous_word=p[i-1].lower()
            if (word, previous_word) in dictionary: #
                dictionary[(word, previous_word)]+=1
                #print dictionary[word]
            else: 
                dictionary[(word, previous_word)]=1
    dictionary[('total', 'of words')]=sum(dictionary.values())        
    #for duple in sorted(dictionary.iteritems(),key=operator.itemgetter(1),reverse=True):
        #if duple[1]>10:
            #print duple
    return dictionary
    
def test_get_labeled_comments():
    table=get_labeled_comments(3.0)
    print len(table)
    print table[('total', 'of words')]
    print table
    
def get_all_labeled_comments():
    D=[{},{},{},{},{},{},{},{},{},{}]
    index=0
    for i in (5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5):
        D[index]=get_labeled_comments(i)
        index=index+1
    return D

def all_words(): 
    '''get a dict with all the words that appear in the comments''' 
    db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    cursor=db.cursor()
    cursor.execute("""SELECT `review` FROM `rafael`.`cinefrance_moviereviews`""")   
    dictionary={}
    count_words=0
    for t in cursor.fetchall():
        T=string.replace(t[0], '’', '\'')
        p=re.findall('[^\s\',;.!?()/«»]+|[;!?«»]', T)
        count_words+=len(p)
        for word in p:
            word=word.lower()
            if word in dictionary: 
                dictionary[word]=dictionary.get(word)+1
            else: 
                dictionary[word]=1
    print "I got all the words!"
    print len(dictionary)
    print 'count_words ='+str(count_words)
    print
    dictionary["total of words"]=sum(dictionary.values())
    print dictionary["total of words"]
    print
    return dictionary


def all_good_words():
    '''get a dict with all the words that appear at least 10 times in the comments'''
    dic=all_words()
    new_dictionary={d:dic[d] for d in dic.keys() if dic[d]>9}
    print "good words:"
    print len(new_dictionary)        
    return new_dictionary            
    
def all_sequence_of_words(): 
    '''get a dict with all the couples of two words that appear in the comments''' 
    db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    cursor=db.cursor()
    cursor.execute("""SELECT `review` FROM `rafael`.`cinefrance_moviereviews`""")   
    dictionary={}
    count_words=0
    for t in cursor.fetchall():
        T=string.replace(t[0], '’', '\'')
        p=re.findall('[^\s\',;.!?()/«»]+|[;!?«»]', T)
        count_words+=len(p)
        for i in range(len(p)):
            word=p[i].lower()
            if (i==0):
                previous_word=None
            else:
                previous_word=p[i-1].lower()
            if (word,previous_word) in dictionary: 
                dictionary[(word,previous_word)]+=1
            else: 
                dictionary[(word,previous_word)]=1
    print "I got all the sequence of words!"
    print len(dictionary)
    print 'count_words = '+str(count_words)
    dictionary[("total", "of words")]=sum(dictionary.values())
    return dictionary


def all_good_sequence_of_words():
    '''get a dict with all the couples of two words that appear at least 10 times in the comments'''
    dic=all_sequence_of_words()
    new_dictionary={d:dic[d] for d in dic.keys() if dic[d]>19}
    print "good sequence of words:"
    print len(new_dictionary)        
    return new_dictionary            

def test_all_good_sequence_of_words():
    all_words()
    vocab=all_sequence_of_words()
    j=0
    count=0
    count_2=0
    cle='de'
    '''vocab.pop(("total", "of words"))
    vocab[("total", "of words")]=sum(vocab.values())'''
    print vocab[("total", "of words")]
    print vocab[("est", "c")]
    for key in vocab.keys():
        if key[1]==cle:
            count+=vocab[key]
        if key[0]==cle:
            count_2+=vocab[key]    
    print count
    print count_2    
        

#doit-on compter plusieurs fois un mot qui apparait plus d'une fois par message ?
##OUI
def frequency_of(cle,D):
    '''take as arguments a key and all_labeled_comments()'''
    index=0
    print 'How many times did the word '+cle+' appears in average in comments with:'
    for i in (5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5):
        print object.__str__(i)+' stars'
        if cle in D[index]:
            print D[index][cle] / D[index]["total of words"]
        else:
            print 0    
        print
        index=index+1
    
def density_of(cle,D):
    '''take as arguments a key and all_labeled_comments()'''
    P=numpy.linspace(0.0, 0.0, num=10)
    Q=numpy.linspace(0.0, 0.0, num=10)
    index=0
    while (index<10):
        Q[index]=D[index][("total", "of words")]
        if cle in D[index]:
            P[index]=D[index][cle] 
        else:
            P[index]=0
        index=index+1
    Sp=sum(P)
    Sq=sum(Q)
    while (index>0):
        index=index-1
        P[index]=P[index]/Sp
        Q[index]=Q[index]/Sq
    #print "density function of appearance of the word "+cle+":"
    #print P
    #print 
    #print "density function of rating of a comment :"
    #print Q
    #print 
    return [P,Q]

def divergence_KL(dens):
    DKL=safe_x_log_x(dens[0])-numpy.dot(numpy.log(dens[1]),dens[0])
    #print "significance of the word "+cle+" :"
    #print DKL
    return DKL

def entropy_test():
    vocab=all_good_words()
    for word in vocab.keys():
        dens=density_of(word)
        d=divergence_KL(dens)
        print "significance of the word "+word+" :"
        if (d>0.05):
            print d

def entropy_insertion():
    vocab=all_good_words()
    new_db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    new_cursor=new_db.cursor()
    D=get_all_labeled_comments()
    for word in vocab.keys():
        dens=density_of(word,D)
        d=divergence_KL(dens)
        new_query="""INSERT INTO `rafael`.`significance_of_sequence_of_words` (`Word`,`Density 5`,`Density 4.5`,`Density 4`,`Density 3.5`,`Density 3`,`Density 2.5`,`Density 2`,`Density 1.5`,`Density 1`,`Density 0.5`,`Divergence_KL`) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")"""%(word,dens[0][0],dens[0][1],dens[0][2],dens[0][3],dens[0][4],dens[0][5],dens[0][6],dens[0][7],dens[0][8],dens[0][9],d)
        new_cursor.execute(new_query)
        print "insertion réussie"

def significance_of_sequence_of_words_insertion():
    vocab=all_good_sequence_of_words()
    new_db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    new_cursor=new_db.cursor()
    D=get_all_labeled_comments()
    for sequence in vocab.keys():
        dens=density_of(sequence,D)
        d=divergence_KL(dens)
        if (sequence[1]==None):
            new_query="""INSERT INTO `rafael`.`significance_of_sequence_of_words` (`Word`,`Previous Word`, `Density 5`,`Density 4.5`,`Density 4`,`Density 3.5`,`Density 3`,`Density 2.5`,`Density 2`,`Density 1.5`,`Density 1`,`Density 0.5`,`Divergence_KL`) VALUES ("%s",NULL,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")"""%(sequence[0],dens[0][0],dens[0][1],dens[0][2],dens[0][3],dens[0][4],dens[0][5],dens[0][6],dens[0][7],dens[0][8],dens[0][9],d)
        else:
            new_query="""INSERT INTO `rafael`.`significance_of_sequence_of_words` (`Word`,`Previous Word`, `Density 5`,`Density 4.5`,`Density 4`,`Density 3.5`,`Density 3`,`Density 2.5`,`Density 2`,`Density 1.5`,`Density 1`,`Density 0.5`,`Divergence_KL`) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")"""%(sequence[0], sequence[1], dens[0][0],dens[0][1],dens[0][2],dens[0][3],dens[0][4],dens[0][5],dens[0][6],dens[0][7],dens[0][8],dens[0][9],d)
        new_cursor.execute(new_query)
        print "insertion réussie"

def get_most_significant_words():
    db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    cursor=db.cursor()
    cursor.execute("""SELECT * FROM `significance_of_the_words` ORDER BY `significance_of_the_words`.`Divergence_KL` DESC LIMIT 0 , 930""")
    myTable=cursor.fetchall()
    for t in myTable:
        print t[0]
        print t[11]
        print 

def dictionary_db():
    dic=all_words()
    db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    cursor=db.cursor()
    #i=u"bien"
    #Query="""INSERT INTO `rafael`.`cinefrance` (`movie_id`,`all`,`r`,`iew`) VALUES ("%s", "%s");"""%(id_, url, stars ,comment);
    #query=
    #print "ok!"
    cursor.executemany("""INSERT INTO `rafael`.`dictionary 2` (`Word`,`N° of appearances`) VALUES ("%s", "%s")""", [(i,dic[i]) for i in dic.keys()])
    print "great work!"
    

    
#test()    
#cle=u"j"
#D=get_all_labeled_comments()
#dens=density_of(cle,D)
#divergence_KL(dens)
#frequency_of(cle,D)
#entropy_insertion()
#test_all_good_sequence_of_words()
#all_good_words()
get_most_significant_words()
#dictionary_db()
#D=get_all_labeled_comments()
'''print len(D)
print len(D[0])
print len(D[1])
print len(D[9])'''
#significance_of_sequence_of_words_insertion()
#test_get_labeled_comments()