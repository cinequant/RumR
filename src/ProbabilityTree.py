#-*- coding: utf-8 -*-
from __future__ import division
from guppy import hpy
import MySQLdb
import re
import Joker
import Features
import FeaturesTree
import cPickle
import math
import string
import sys
import time

class ProbabilityTree:
    other=Joker.other
    
    def __init__(self):
        self.probability=0
        self.edges={}
        self.feature_index=0
        
    def write_tree(self, feats_tree, lamb):
        for key in feats_tree.edges.keys():
            if (feats_tree.get(key)!=None):
                self.edges[key]=ProbabilityTree()
                self.edges[key].write_tree(feats_tree.get(key),lamb)
            else:
                feature_index=feats_tree.feature_index
                self.probability=math.exp(lamb[feature_index])
                
            
    def write_weights(self):
        for branch1 in self.edges.values():
            
            for branch2 in branch1.edges.values():
                sum=0
                for branch3 in branch2.edges.values():
                    sum+=branch3.probability
                for branch3 in branch2.edges.values():
                    branch3.probability=branch3.probability/sum
                
    def new_other(self):
        for key in self.edges.keys():
            if (key.__class__==object):
                self.other=key
                print self.other
                print 'we have a new other object'            
        
    def classifier_word(self, word, previous_word, stars):
        try:
            a=self.edges[stars].edges[previous_word].edges[word].probability
        except:
            try:
                a=self.edges[stars].edges[previous_word].edges[self.other].probability
            except:
                try:
                    a=self.edges[stars].edges[self.other].edges[word].probability
                except:
                    a=self.edges[stars].edges[self.other].edges[self.other].probability      
        return a
    
    def classifier_message(self, message):
        db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
        cursor=db.cursor()
        cursor.execute("""SELECT * FROM `rafael`.`Significance_of_the_words` ORDER BY `rafael`.`Significance_of_the_words`.`Divergence_KL` ASC LIMIT 0,1""")
        Ps=cursor.fetchone()
        result={5.0-i/2:Ps[i+1] for i in range(10)}
        #message=string.replace(message,'’', '\'')
        words=re.findall('[^\s\',;.`’!?()/«»]+|[;!?.«»]',message)
        for i in range(len(words)):
            if (i!=0):
                for star in result.keys():
                    result[star]=result[star]*self.classifier_word(words[i],words[i-1],star)
            else:
                for star in result.keys():
                    result[star]=result[star]*self.classifier_word(words[0],None,star)
        somme=sum(result.values())
        for key in result.keys():
            result[key]=result[key]/somme
        return result
    
    def classifier_message_SQL_1000(self, message):
        db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
        cursor=db.cursor()
        cursor.execute("""SELECT * FROM `rafael`.`Significance_of_the_words` ORDER BY `rafael`.`Significance_of_the_words`.`Divergence_KL` ASC LIMIT 0,1""")
        p_stars=cursor.fetchone()
        result={5.0-i/2:p_stars[i+1] for i in range(10)}
        #message=string.replace(message,'’', '\'')
        words=re.findall('[^\s\',;.`’!?()/«»]+|[;!?.«»]',message)
        for i in range(len(words)):
            cursor.fetchall()
            if (i!=0):
                for star in result.keys():
                    cursor.execute("""SELECT `Probability` FROM `rafael`.`Probability Tree` WHERE `word`="%s" AND `Previous Word`="%s" AND `Stars`="%s" """%(words[i],words[i-1],star))
                    try: 
                        proba=cursor.fetchone()[0]
                    except:
                        cursor.execute("""SELECT `Probability` FROM `rafael`.`Probability Tree` WHERE `word`="%s" AND `Previous Word`="%s" AND `Stars`="%s" """%(words[i],'<object object at 0x16c50b0>',star))
                        try:
                            proba=cursor.fetchone()[0]
                        except:
                            (words[i],words[i-1],star)
                            cursor.execute("""SELECT `Probability` FROM `rafael`.`Probability Tree` WHERE `word`="%s" AND `Previous Word`="%s" AND `Stars`="%s" """%('<object object at 0x16c50b0>','<object object at 0x16c50b0>',star))
                            proba=cursor.fetchone()[0]
                    result[star]=result[star]*proba
            else:
                for star in result.keys():
                    cursor.execute("""SELECT `Probability` FROM `rafael`.`Probability Tree` WHERE `word`="%s" AND `Previous Word`="%s" AND `Stars`="%s" """%(words[i],None,star))
                    try: 
                        proba=cursor.fetchone()[0]
                    except:
                        cursor.execute("""SELECT `Probability` FROM `rafael`.`Probability Tree` WHERE `word`="%s" AND `Previous Word`="%s" AND `Stars`="%s" """%(words[i],'<object object at 0x16c50b0>',star))
                        try:
                            proba=cursor.fetchone()[0]
                        except:
                            (words[i],words[i-1],star)
                            cursor.execute("""SELECT `Probability` FROM `rafael`.`Probability Tree` WHERE `word`="%s" AND `Previous Word`="%s" AND `Stars`="%s" """%('<object object at 0x16c50b0>','<object object at 0x16c50b0>',star))
                            proba=cursor.fetchone()[0]
                    result[star]=result[star]*proba
        somme=sum(result.values())
        for key in result.keys():
            result[key]=result[key]/somme
        return result

    def classifier_message_SQL_10000(self, message):
        db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
        cursor=db.cursor()
        cursor.execute("""SELECT * FROM `rafael`.`Significance_of_the_words` ORDER BY `rafael`.`Significance_of_the_words`.`Divergence_KL` ASC LIMIT 0,1""")
        p_stars=cursor.fetchone()
        result={5.0-i/2:p_stars[i+1] for i in range(10)}
        #message=string.replace(message,'’', '\'')
        words=re.findall('[^\s\',;.`’!?()/«»]+|[;!?.«»]',message)
        words.append(None)
        for i in range(len(words)-1):
            cursor.fetchall()
            if True:
                for star in result.keys():
                    cursor.execute("""SELECT `son_id` FROM `rafael`.`Probability Tree 10000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(star, words[i-1]))
                    try:
                        branch_id=cursor.fetchone()[0]
                        cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree 10000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,words[i]))
                        try: 
                            proba=cursor.fetchone()[0]
                        except:
                            cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree 10000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,'<object object at 0x16c50b0>'))
                            proba=cursor.fetchone()[0]
                    except:
                        cursor.execute("""SELECT `son_id` FROM `rafael`.`Probability Tree 10000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(star,'<object object at 0x16c50b0>'))
                        branch_id=cursor.fetchone()[0]
                        try:
                            cursor.execute("""SELECT `Probability` FROM `rafael`.`Probability Tree 10000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,word[i]))
                            proba=cursor.fetchone()[0]
                        except:
                            cursor.execute("""SELECT `Probability` FROM `rafael`.`Probability Tree 10000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,'<object object at 0x16c50b0>'))
                            proba=cursor.fetchone()[0]
                    result[star]=result[star]*proba
        somme=sum(result.values())
        for key in result.keys():
            result[key]=result[key]/somme
        return result


    def write_model_tree(self, size):
        tree_file_name="Features Tree version "+str(size)+" features"
        weights_file_name="Final Weights threshold 0.1 version "+str(size)+" features"
        feats_tree=cPickle.load(open(tree_file_name))
        wei=cPickle.load(open(weights_file_name))
        self.write_tree(feats_tree,wei)
        self.write_weights()
        self.new_other()

    def main_1000(self):
        print 'searching tree\n'
        feats_tree=cPickle.load(open("Features Tree version 1000 features"))
        print 'tree: OK! \n'
        wei=cPickle.load(open("Final Weights threshold 0.1 version 1000 features"))
        print 'weights ok!'
        proba_tree=ProbabilityTree()
        proba_tree.write_tree(feats_tree,wei)
        proba_tree.write_weights()
        proba_tree.new_other()
        message=raw_input("Entrer votre message :")
        D=proba_tree.classifier_message(message)
        print D
        
    def main_1000(self, message):
        self.write_model_tree(1000)
        D=self.classifier_message(message)
        return D
    
    def main_5000(self, message):
        self.write_model_tree(5000)
        D=self.classifier_message(message)
        return D 
    
    def main_10000(self, message):
        self.write_model_tree(10000)
        D=self.classifier_message(message)
        return D
    
    def main_SQL_1000(self, message):
        self.write_model_tree(1000)
        D=self.classifier_message_SQL(message)
        return D
        

'''tree=ProbabilityTree()
#print h.heap()
t0=time.time()
D=tree.main_SQL_1000('ceci est un message')
print D 
t1=time.time()
print t1-t0'''
