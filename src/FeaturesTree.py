#-*- coding: utf-8 -*-
'''
Created on May 10, 2012

@author: rafael
'''
from __future__ import division
import numpy
import Joker
import IteratorWords
import sets
import time
import math
import string

class FeaturesTree:
    historic_size=2
                
    def __init__(self):
        self.features=set()
        self.edges={Joker.other:None}
        self.occurrences=0 
        self.feature_index=0

    def __getitem__(self,key):
        return self.edges.__getitem__(key)
    
    def new_generation(self,i):
        #creating branches
        for feature in self.features:
            t=feature[i]
            if ((t.__class__==object) & (self.edges[Joker.other]==None)):
                self.edges[Joker.other]=FeaturesTree()
            elif ((t not in self.edges) & (t.__class__!=object)):
                self.edges[t]=FeaturesTree()
       
        #giving its own features        
        for feature in self.features:
            t=feature[i]
            if (t.__class__==object): #feature[i]=any_word or any_number
                for tree in self.edges.values():
                    if (tree==None):
                        tree=FeaturesTree()
                    tree.features.add(feature)
            elif (t in self.edges.keys()): #feature[i]=word that appears in a selected feature
                self.edges[t].features.add(feature)
            else:
                self.edges[Joker.other].features.add(feature)    
                
        
    def write_tree(self,sel):
        '''number of 'for' loops is equal to historic_size'''
        self.features=set(sel)
        self.new_generation(0)
        for branch1_key in self.edges.keys():
            self.edges[branch1_key].new_generation(1)
            branch1=self.edges[branch1_key]
            for branch2_key in branch1.edges.keys():
                branch2=branch1.edges[branch2_key]
                if (branch2==None):
                    self.edges[branch1_key].edges[branch2_key]=FeaturesTree()
                self.edges[branch1_key].edges[branch2_key].new_generation(2)
    
    def get_edges(self):
        return self.edges
    
    def get(self,x):
        return self.edges.__getitem__(x)
    
    def remove_other(self):
        self.edges.pop(Joker.other)
      
    def remove_features(self):
        '''excluding .features to quickly save our tree'''
        self.features.clear()
        self.features=None
        for branch_key in self.edges.keys():
            branch=self.edges[branch_key]
            if (branch!=None):
                branch.remove_features()
            
    def p_lambda(self,vector,new_feats,n):
        '''construction of the conditional probability for lambda=vector'''
        if (len(vector)!=n):
            print 'not a good length for lambda! Try again'
        else:
            for branch1 in self.edges.values():
                for branch2 in branch1.edges.values():
                    if (branch2!=None):
                        Z=0
                        for branch3 in branch2.edges.values():
                            if (branch3!=None):
                                branch3.conditional_probability=math.exp(vector[new_feats[sets.ImmutableSet(branch3.features)]])
                                Z+=branch3.conditional_probability
                        for branch3 in branch2.edges.values():
                            if (branch3!=None):
                                branch3.conditional_probability=branch3.conditional_probability/Z
                        if (branch2.edges[Joker.other]!=None):
                            print branch2.edges[Joker.other].conditional_probability 
                            print        
    
    def new_features(self):
        '''list where we correspond each new feature (subset of features set) to its index; writes .feature_index'''
        result={sets.ImmutableSet(set()): 0}
        index=1
        for branch1_key in self.edges.keys():
            branch1=self.edges[branch1_key]
            for branch2_key in branch1.edges.keys():
                branch2=branch1.edges[branch2_key]
                for branch3_key in branch2.edges.keys():
                    branch3=branch2.edges[branch3_key]
                    if (branch3==None):
                        branch3=FeaturesTree()
                        self.edges[branch1_key].edges[branch2_key].edges[branch3_key]=branch3
                    S=sets.ImmutableSet(branch3.features)
                    try:
                        branch3.feature_index=result[S]
                    except:
                        if (branch1_key!=Joker.other):
                            result[S]=index
                            branch3.feature_index=index
                            index+=1
                        else:
                            branch3.feature_index=0    
        return result

    def collect_new_features(self,new_features_dictionary):
        for branch1_key in self.edges.keys():
            branch1=self.edges[branch1_key]
            for branch2_key in branch1.edges.keys():
                branch2=branch1.edges[branch2_key]
                for branch3_key in branch2.edges.keys():
                    branch3=branch2.edges[branch3_key]
                    if (branch3==None):
                        branch3=FeaturesTree()
                        self.edges[branch1_key].edges[branch2_key].edges[branch3_key]=branch3
                    S=branch3.features
                    SS=sets.ImmutableSet(S)
                    try:
                        branch3.feature_index=new_features_dictionary[SS]
                    except:
                        for element in S:
                            L=list()
                            for i in range(len(element)):
                                if (element[i].__class__==object):
                                    print 
                                    L.append(Joker.other)
                                else:
                                    L.append(element[i])
                            if (element!=tuple(L)):
                                S.remove(element)
                                S.add(tuple(L))
                        SS=sets.ImmutableSet(S)
                        branch3.feature_index=new_features_dictionary[SS] 
        

    def count_occurrences(self):
        '''\tilde{p} calculation; writes occurrence'''
        print 'start count_occurrences'
        iterator=IteratorWords.IteratorWords()
        for i in iterator:
            self.edges[i.stars].occurrences+=1
            if (i.words[1] in self.edges[i.stars].edges.keys()):
                self.edges[i.stars].edges[i.words[1]].occurrences+=1
                if (i.word in self.edges[i.stars].edges[i.words[1]].edges.keys()):
                    self.edges[i.stars].edges[i.words[1]].edges[i.word].occurrences+=1
                else:
                    if (self.edges[i.stars].edges[i.words[1]].edges[Joker.other]==None):
                        self.edges[i.stars].edges[i.words[1]].edges[Joker.other]=FeaturesTree()
                    self.edges[i.stars].edges[i.words[1]].edges[Joker.other].occurrences+=1
            else:
                self.edges[i.stars].edges[Joker.other].occurrences+=1
                if (i.word in self.edges[i.stars].edges[Joker.other].edges.keys()):
                    self.edges[i.stars].edges[Joker.other].edges[i.word].occurrences+=1
                else:
                    if (self.edges[i.stars].edges[Joker.other].edges[Joker.other]==None):
                        self.edges[i.stars].edges[Joker.other].edges[Joker.other]=FeaturesTree()
                    self.edges[i.stars].edges[Joker.other].edges[Joker.other].occurrences+=1
                    
            self.edges[Joker.other].occurrences+=1
            if (i.words[1] in self.edges[Joker.other].edges.keys()):
                self.edges[Joker.other].edges[i.words[1]].occurrences+=1
                if (i.word in self.edges[Joker.other].edges[i.words[1]].edges.keys()):
                    self.edges[Joker.other].edges[i.words[1]].edges[i.word].occurrences+=1
                else:
                    if (self.edges[Joker.other].edges[i.words[1]].edges[Joker.other]==None):
                        self.edges[Joker.other].edges[i.words[1]].edges[Joker.other]=FeaturesTree()
                    self.edges[Joker.other].edges[i.words[1]].edges[Joker.other].occurrences+=1
            else:
                self.edges[Joker.other].edges[Joker.other].occurrences+=1
                if (i.word in self.edges[Joker.other].edges[Joker.other].edges.keys()):
                    self.edges[Joker.other].edges[Joker.other].edges[i.word].occurrences+=1
                else:
                    if (self.edges[Joker.other].edges[Joker.other].edges[Joker.other]==None):
                        self.edges[Joker.other].edges[Joker.other].edges[Joker.other]=FeaturesTree()
                    self.edges[Joker.other].edges[Joker.other].edges[Joker.other].occurrences+=1                    
                    
            
    def write_probability(self,lamb):
        '''The features field, before valued as None, will give us the conditional probability'''
        for key in self.edges.keys():
            if (self.get(key)!=None):
                self.edges[key].write_probability(lamb)
            else:
                index=self.feature_index
                self.features=math.exp(lamb[index])
                
        for branch1_key in self.edges.keys():
            branch1=self.edges[branch1_key]
            for branch2_key in branch1.edges.keys():
                branch2=branch1.edges[branch2_key]
                sum=0
                for branch3 in branch2.edges.values():
                    sum+=branch3.features
                for branch3_key in branch2.edges.keys():
                    branch3=branch2.edges[branch3_key]
                    branch3.features=branch3.features/sum    
                    
                    
                    
    def classifier_word(self, word, previous_word, stars):
        a=self.edges[stars].edges[previous_word].edges[word].probability
        b=self.edges[Joker.other].edges[previous_word].edges[word].probability
        return a/b
    
    def classifier_message(self, message):
        db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
        cursor=db.cursor()
        cursor.execute("""SELECT * FROM `rafael`.`Significance_of_the_words` ORDER BY `rafael`.`Significance_of_the_words`.`Divergence_KL` ASC LIMIT 0,1""")
        Ps=cursor.fetchone()
        result={5.0-i/2:Ps[i+1] for i in range(10)}
        words=re.findall('[^\s\',;.!?()/«»]+|[;!?.«»]',message) #string.replace(message,'’', '\'')
        for i in range(len(words)):
            if (i!=0):
                for star in result.keys():
                    result[star]=result[star]*classifier_word(words[i],words[i-1],star)
            else:
                for star in result.keys():
                    result[star]=result[star]*classifier_word(words[i],None,star)
        return result

        
'''tree=FeaturesTree()
tree.add_feature((1,11,112,Joker.other,123))
tree.add_feature((1,11,111,Joker.other,123))
print tree.edges
print tree.edges[1].edges
print tree.edges[1].edges[11].edges
print tree.edges[1].edges[11].edges[111].edges
print tree.edges[1].edges[11].edges[111].edges[Joker.other].edges
print tree.edges[1].edges[11].edges[111].edges[Joker.other].edges[123].edges'''