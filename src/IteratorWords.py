#-*- coding: utf-8 -*-
'''
Created on Apr 19, 2012

@author: rafael
'''
import MySQLdb
import string
import re

class IteratorWords:
    def __init__(self):
        self.global_index=0
        self.word_count=2
        db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
        self.cursor=db.cursor()
        self.fetch=None
        self.cursor.execute("""SELECT * FROM `rafael`.`cinefrance_moviereviews`""")
        self.message=[]
        self.word_index=0
        self.word=None
        self.stars=None
        self.words=[None for j in range(self.word_count+1)]
        
    def __iter__(self):
        return self
    
    def next(self):
        if (len(self.message)==0)|(self.word_index==len(self.message)):
            self.fetch=self.cursor.fetchone()
            if (self.fetch==None):
                raise StopIteration
            self.message=re.findall('[^\s\',;.!?()/«»]+|[;!?.«»]',string.replace(self.fetch[3],'’', '\''))
            self.stars=self.fetch[2]
            self.word_index=1
            [self.words.append(None) for j in range(self.word_count)]
            [self.words.pop(0) for j in range(self.word_count)]
        else:
            self.word_index +=1
        if (len(self.message)!=0):
            self.word=self.message[self.word_index-1].lower()
            self.words.append(self.word)
            self.words.pop(0)
            self.global_index +=1
        return self
        
        
'''DDD= IteratorWords()
#cle=u"bien"
p=0      
for i in DDD:
    if (i.words[1]=='touchante') & (i.stars==0.5):
        print 'epa!'
        p=i.global_index
        print i.word
    #print "mot = {0}, mot précedent = {1}, mot d'avant = {2}, étoiles = {3}".format(i.word,i.words[1],i.words[0],i.stars)
print p
print "c'est la fin !"'''