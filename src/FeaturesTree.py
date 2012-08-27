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
import pickle
import cPickle


class FeaturesTree:
    historic_size=2
                
    def __init__(self):
        self.features=set()
        self.edges={Joker.other:None}
        self.occurrences=0
        self.feature_index=0
        
    def __str__(self):
        print "printing Features Tree"
        stt=''
        count=0
        for key_1 in self.edges.keys():
            #stt=stt+'\n'+str((key_1, self.edges[key_1].occurrences, self.edges[key_1].features)) #
            value_1=self.edges[key_1]
            for key_2 in value_1.edges.keys():
                value_2=value_1.edges[key_2]
                #stt=stt+'\n'+str((key_1, key_2, value_2.occurrences, value_2.features)) #
                '''if (value_2.occurrences==0) and (key_1.__class__!=object):
                    raise ValueError('a coisa tah preta : '+str((key_1,key_2)))'''
                for key_3 in value_2.edges.keys():
                    stt=stt+'\n'+str((key_1, key_2, key_3, value_2.edges[key_3].occurrences, value_2.edges[key_3].feature_index)) #
                    count+=value_2.edges[key_3].occurrences
        print count
        return stt            

    def __getitem__(self,key):
        return self.edges.__getitem__(key)
    
    def new_generation(self, sel, i):
        #creating branches
        if (i==0):
            for feature in self.features:
                t=feature[i]
                if ((t.__class__==object) & (self.edges[Joker.other]==None)):
                    self.edges[Joker.other]=FeaturesTree()
                elif ((t not in self.edges) & (t.__class__!=object)):
                    self.edges[t]=FeaturesTree()
        elif (i>=1) and (i<=2):
            #print 'let us check : '+str(len(self.edges))
            for feature in sel:         
                t=feature[i]
                if ((t.__class__==object) & (self.edges[Joker.other]==None)):
                    self.edges[Joker.other]=FeaturesTree()
                elif ((t not in self.edges) & (t.__class__!=object)):
                    self.edges[t]=FeaturesTree()
            #print 'let us check again : '+str(len(self.edges))        
        else:
            raise ValueError("not a correct generation number: "+str(i))  
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
        ''' construit l arbre'''
        '''for increase the depth of the tree you need to increase the number of for loops'''
        self.features=set(sel)
        self.new_generation(sel, 0)
        for branch1_key in self.edges.keys():
            try:
                self.edges[branch1_key].new_generation(sel, 1)
            except:
                print branch1_key
                raise ValueError('vai tomar no cu')
            branch1=self.edges[branch1_key]
            for branch2_key in branch1.edges.keys():
                branch2=branch1.edges[branch2_key]
                if (branch2==None):
                    self.edges[branch1_key].edges[branch2_key]=FeaturesTree()
                self.edges[branch1_key].edges[branch2_key].new_generation(sel, 2)
                #join more generations here for a deeper tree
    
    def get_edges(self):
        '''access to the dictionary of FeaturesTree's children'''
        return self.edges
    
    def get(self,x):
        return self.edges.__getitem__(x)
    
    def remove_other(self):
        try:
            self.edges.pop(Joker.other)
        except:
            for key in self.edges.keys():
                if (key.__class__==object):
                    Joker.other=key
            self.edges.pop(Joker.other)            
      
    def remove_features(self):
        '''excluding .features to quickly save our tree as Pickle'''
        self.features.clear()
        for branch_key in self.edges.keys():
            branch=self.edges[branch_key]
            if (branch!=None):
                branch.remove_features()
            
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
    
    def normalized_features(self, sel):
        result={sel[i]:i+1 for i in range(len(sel))}
        result[None]=0
        return result
    
    def collect_normalized_features_index(self, sel):
        '''For normalized features, feature_index is a tuple of the active features. 
           The set of features indexes tuples is also the set of second generation vertexes of the AlgorithmTreeNorm
        '''
        normalized_features=self.normalized_features(sel)
        result={}
        index=0
        for branch1_key in self.edges.keys():
            branch1=self.edges[branch1_key]
            for branch2_key in branch1.edges.keys():
                branch2=branch1.edges[branch2_key]
                for branch3_key in branch2.edges.keys():
                    branch3=branch2.edges[branch3_key]
                    if (branch3==None):
                        branch3=FeaturesTree()
                        self.edges[branch1_key].edges[branch2_key].edges[branch3_key]=branch3
                    S=set()
                    for element in branch3.features:
                        S.add(normalized_features[element])
                    if len(S)<3:
                        S.add(0)
                    branch3.feature_index=tuple(S)
                    if branch3.feature_index not in result.values():
                        result[index]=branch3.feature_index
                        index+=1
        return result            
                        

    def count_occurrences(self):
        '''\tilde{p} calculation; writes occurrence'''
        print 'start count_occurrences'
        iterator=IteratorWords.IteratorWords()
        count=0
        real_count=0
        for i in iterator:
            real_count+=1
            try:
                self.edges[i.stars].occurrences+=1
                star=i.stars
            except:
                self.edges[Joker.other].occurrences+=1
                star=Joker.other
                raise ValueError(str((i.word, i.words[1], i.star)))
                
                            
            if (i.words[1] in self.edges[star].edges.keys()):
                self.edges[star].edges[i.words[1]].occurrences+=1
                if (i.word in self.edges[star].edges[i.words[1]].edges.keys()):
                    self.edges[star].edges[i.words[1]].edges[i.word].occurrences+=1
                    count+=1
                else:
                    if (self.edges[star].edges[i.words[1]].edges[Joker.other]==None):
                        self.edges[star].edges[i.words[1]].edges[Joker.other]=FeaturesTree()
                    self.edges[star].edges[i.words[1]].edges[Joker.other].occurrences+=1
                    count+=1
            else:
                try:
                    self.edges[star].edges[Joker.other].occurrences+=1
                except:
                    self.edges[star].edges[Joker.other]=FeaturesTree()
                    self.edges[star].edges[Joker.other].occurrences+=1
                if (i.word in self.edges[star].edges[Joker.other].edges.keys()):
                    self.edges[star].edges[Joker.other].edges[i.word].occurrences+=1
                    count+=1
                else:
                    if (self.edges[star].edges[Joker.other].edges[Joker.other]==None):
                        self.edges[star].edges[Joker.other].edges[Joker.other]=FeaturesTree()
                    self.edges[star].edges[Joker.other].edges[Joker.other].occurrences+=1
                    count+=1
            if (count!=real_count):
                print (star, i.words[1], i.word)
        print 'end count_occurrences :'+str(count)
                    
    def count_occurrences_by_primary_tree(self, primary_tree):
        print 'start count_occurrences_by_primary_tree'
        count=0
        for key_1 in primary_tree.edges.keys():
            self.edges[key_1].occurrences=primary_tree.edges[key_1].occurrences
            value_1=self.edges[key_1]
            primary_value_1=primary_tree.edges[key_1]
            for key_2 in primary_value_1.edges.keys():
                primary_value_2=primary_value_1.edges[key_2]
                if (key_2 in value_1.edges.keys()):
                    value_2=value_1.edges[key_2]
                    value_2.occurrences+=primary_value_2.occurrences
                else:
                    value_2=value_1.edges[Joker.other]
                    value_2.occurrences+=primary_value_2.occurrences
                for key_3 in primary_value_2.edges.keys():
                    if key_3 in value_2.edges.keys():
                        value_2.edges[key_3].occurrences+=primary_value_2.edges[key_3].occurrences
                        count+=primary_value_2.edges[key_3].occurrences
                    else:
                        value_2.edges[Joker.other].occurrences+=primary_value_2.edges[key_3].occurrences
                        count+=primary_value_2.edges[key_3].occurrences
        print 'count = '+str(count)
        
        
    def to_zero_occurrences(self):
        for key_1 in self.edges.keys():
            value_1=self.edges[key_1]
            value_1.occurrences=0
            for key_2 in value_1.edges.keys():
                value_2=value_1.edges[key_2]
                value_2.occurrences=0
                for key_3 in value_2.edges.keys():
                    value_3=value_2.edges[key_3]
                    value_3.occurrences=0
                    
    def previous_words(self):
        '''set of all the words of the second generation'''        
        return set(self.edges[5.0].edges.keys())
    
    def current_words(self):
        '''set of all the words of the third generation'''        
        return set(self.edges[5.0].edges['.'].edges.keys()) 
    
    def add_feature(self, feature_to_add):
        s=feature_to_add[0]
        w_0=feature_to_add[1]
        w_1=feature_to_add[2]
        set_of_words_0=self.previous_words()
        set_of_words_1=self.current_words()
        #adding feature_to_add
        self.features.add(feature_to_add)
        if s.__class__!=object:
            self.edges[s].features.add(feature_to_add)
        else:
            for value_1 in self.edges.values():
                value_1.features.add(feature_to_add)
        
        #adding branches and giving its features
        if (w_0.__class__==object) or (w_0 in set_of_words_0):
            boo_0=True
            for value_1 in self.edges.values():
                if feature_to_add in value_1.features:
                    for key_2 in value_1.edges.keys():
                        if (key_2==w_0) or (w_0.__class__==object):
                            value_1.edges[key_2].features.add(feature_to_add)
        else:
            boo_0=False
            for value_1 in self.edges.values():
                new_branch=FeaturesTree()
                value_1.edges[w_0]=new_branch
                for feature in value_1.features:
                    if (feature[1].__class__==object) or (feature[1]==w_0):
                        new_branch.features.add(feature)
                for word in set_of_words_1:
                    new_branch.edges[word]=FeaturesTree()
                    for feature in new_branch.features:
                        if feature[2]==word:
                            new_branch.edges[word].features.add(feature)
                
                
            
        if (w_1.__class__==object) or (w_1 in set_of_words_1):
            boo_1=True
            for value_1 in self.edges.values():
                if feature_to_add in value_1.features:
                    for value_2 in value_1.edges.values():
                        if feature_to_add in value_2.features:
                            for key_3 in value_2.edges.keys():
                                if (key_3==w_1) or (w_1.__class__==object):
                                    value_2.edges[key_3].features.add(feature_to_add)
                    
        else:
            boo_1=False
            for value_1 in self.edges.values():
                for value_2 in value_1.edges.values():
                    new_branch=FeaturesTree()
                    value_2.edges[w_1]=new_branch
                    for feature in value_2.features:
                        if (feature[2]==w_1):
                            new_branch.features.add(feature)
                        
        return (boo_0, boo_1)

    def remove_feature(self, feature_to_remove, boo_0, boo_1):
        s=feature_to_remove[0]
        w_0=feature_to_remove[1]
        w_1=feature_to_remove[2]
        #removing feature
        self.features.remove(feature_to_remove)
        for key_1 in self.edges.keys():
            if key_1==s or s.__class__==object:
                value_1=self.edges[key_1]
                value_1.features.remove(feature_to_remove)
                for key_2 in value_1.edges.keys():
                    value_2=value_1.edges[key_2]
                    if key_2==w_0 or w_0.__class__==object:
                        value_2.features.remove(feature_to_remove)
                        for key_3 in value_2.edges.keys():
                            if key_3==w_1:
                                value_2.edges[key_3].features.remove(feature_to_remove)
        #removing w_0
        if not boo_0:
            for value_1 in self.edges.values():
                value_1.edges.pop(w_0) 
                       
        if not boo_1:
            for value_1 in self.edges.values():
                for value_2 in value_1.edges.values():
                    value_2.edges.pop(w_1)
                    
            
        
'''
tree=FeaturesTree()
tree.add_feature((1,11,112,Joker.other,123))
tree.add_feature((1,11,111,Joker.other,123))
print tree.edges
print tree.edges[1].edges
print tree.edges[1].edges[11].edges
print tree.edges[1].edges[11].edges[111].edges
print tree.edges[1].edges[11].edges[111].edges[Joker.other].edges
print tree.edges[1].edges[11].edges[111].edges[Joker.other].edges[123].edges
'''
'''
tree=FeaturesTree()
Sel=pickle.load(open("3 selected features file"))
tree.write_tree(Sel)
#tree.count_occurrences()
print tree.edges.keys()
tree.count_occurrences()
tree.collect_normalized_features_index(Sel)
#print Sel
#pickle.dump(tree, open("Features Tree version 80 features", "w"))
print str(tree)
'''
'''for key in tree.edges.keys():
    print 'key = '+str(key)
    print tree.edges[key].edges.keys()
    print
    for key_2 in tree.edges[key].edges.keys():
        print 'key 2 = '+str(key_2)
        print tree.edges[key].edges[key_2].edges.keys()
        print '\n'
        for key_3 in tree.edges[key].edges[key_2].edges.keys():
            print 'key 3 = '+str(key_3)'''