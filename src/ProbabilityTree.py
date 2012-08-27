#-*- coding: utf-8 -*-
from __future__ import division
import MySQLdb
import re
import Joker
import Features
import FeaturesTree
import pickle
import cPickle
import math
import numpy
import string
import sys
import time
   

def classifier_message_SQL_1001(message):
    db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    cursor=db.cursor()
    cursor.execute("""SELECT * FROM `rafael`.`Significance_of_the_words` ORDER BY `rafael`.`Significance_of_the_words`.`Divergence_KL` ASC LIMIT 0,1""")
    p_stars=cursor.fetchone()
    result={5.0-i/2: p_stars[i+1] for i in range(10)} #p_stars[i+1]
    #message=string.replace(message,'’', '\'')
    words=re.findall('[^\s\',;.`’!?()/«»]+|[;!?.«»]',message)
    words.append(None)
    for i in range(len(words)-1):
        cursor.fetchall()
        for star in result.keys():
            matches=cursor.execute("""SELECT `son_id` FROM `rafael`.`Probability Tree 1000 Normalized Features` WHERE `edge_id`="%s" AND `key`="%s" """%(2*star, words[i-1]))
            if (matches.__float__()>1):
                print 'EITA PORRA'    
            try:
                branch_id=cursor.fetchone()[0]
                cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree 1000 Normalized Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,words[i]))
                if (matches.__float__()>1):
                    print 'EITA PORRA'
                try: 
                    proba=cursor.fetchone()[0]
                except:
                    try:
                        cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree 1000 Normalized Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,'<object '))
                    except:
                        print 'pau na linha 90'
                    if (matches.__float__()>1):
                        print 'EITA PORRA'
                    proba=cursor.fetchone()[0]
                        
            except:
                try:
                    cursor.execute("""SELECT `son_id` FROM `rafael`.`Probability Tree 1000 Normalized Features` WHERE `edge_id`="%s" AND `key`='<object' """%(2*star))
                except:
                    print 'pau na linha 100'
                    print 2*star
                branch_id=cursor.fetchone()[0]
                try:
                    cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree 1000 Normalized Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,words[i]))
                    proba=cursor.fetchone()[0]
                except:
                    cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree 1000 Normalized Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,'<object '))
                    proba=cursor.fetchone()[0]
            result[star]=result[star]*proba
        somme=sum(result.values())
        for key in result.keys():
            result[key]=result[key]/somme
        return result

def classifier_message_SQL_super(message):
    t0=time.time()
    db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    cursor=db.cursor()
    cursor.execute("""SELECT * FROM `rafael`.`Significance_of_the_words` ORDER BY `rafael`.`Significance_of_the_words`.`Divergence_KL` ASC LIMIT 0,1""")
    p_stars=cursor.fetchone()
    result={5.0-i/2: p_stars[i+1] for i in range(10)} #p_stars[i+1]
    partial={5.0-i/2: 0 for i in range(10)}
    #message=string.replace(message,'’', '\'')
    words=re.findall(u'[^\s\',;.`’!?()/«»]+|[;!?.«»]',message)
    words.append(None)
    for i in range(len(words)-1):
        cursor.fetchall()
        for star in result.keys():
            matches=cursor.execute("""SELECT `son_id` FROM `rafael`.`Probability Tree Super Normalized Features` WHERE `edge_id`="%s" AND `key`="%s" """%(2*star, words[i-1]))
            '''if (matches.__float__()>1):
                print 'EITA PORRA'  '''  
            try:
                branch_id=cursor.fetchone()[0]
                cursor.fetchall()
                cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree Super Normalized Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,words[i]))
                if (matches.__float__()>1):
                    print 'EITA PORRA'
                    print matches.__float__()
                    print (branch_id,words[i-1],words[i])
                try: 
                    proba=cursor.fetchone()[0]
                except:
                    try:
                        cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree Super Normalized Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,'<object object at 0x13b90a0> '))
                    except:
                        print 'pau na linha 90'
                    if (matches.__float__()>1):
                        print 'EITA PORRA'
                        print (branch_id,words[i-1],words[i])
                    proba=cursor.fetchone()[0]
                    cursor.fetchall()
                
            except:
                try:
                    cursor.execute("""SELECT `son_id` FROM `rafael`.`Probability Tree Super Normalized Features` WHERE `edge_id`="%s" AND `key`='<object object at 0x13b90a0> ' """%(2*star))
                except:
                    print 'pau na linha 100'
                    print 2*star
                branch_id=cursor.fetchone()[0]
                cursor.fetchall()
                try:
                    cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree Super Normalized Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,words[i]))
                    proba=cursor.fetchone()[0]
                except:
                    cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree Super Normalized Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,'<object object at 0x13b90a0> '))
                    proba=cursor.fetchone()[0]
            result[star]=result[star]*proba
            partial[star]=proba
        #print (words[i-1], words[i])
        #print partial
        somme=sum(result.values())
        for key in result.keys():
            result[key]=result[key]/somme
    t1=time.time()
    print 'time ='+str(t1-t0)
    return result

def classifier_message_SQL_super_2(message):
    t0=time.time()
    db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    cursor=db.cursor()
    cursor.execute("""SELECT * FROM `rafael`.`Significance_of_the_words` ORDER BY `rafael`.`Significance_of_the_words`.`Divergence_KL` ASC LIMIT 0,1""")
    p_stars=cursor.fetchone()
    result={5.0-i/2: p_stars[i+1] for i in range(10)} #p_stars[i+1]
    partial={5.0-i/2: 0 for i in range(10)}
    #message=string.replace(message,'’', '\'')
    words=re.findall(u'[^\s\',;.`’!?()/«»]+|[;!?.«»]',message)
    words.append(None)
    for i in range(len(words)-1):
        cursor.fetchall()
        for star in result.keys():
            matches=cursor.execute("""SELECT `son_id` FROM `rafael`.`Probability Tree Super Normalized Features over 2000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(2*star, words[i-1]))
            '''if (matches.__float__()>1):
                print 'EITA PORRA'  '''  
            try:
                branch_id=cursor.fetchone()[0]
                cursor.fetchall()
                cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree Super Normalized Features over 2000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,words[i]))
                if (matches.__float__()>1):
                    print 'EITA PORRA'
                    print matches.__float__()
                    print (branch_id,words[i-1],words[i])
                try: 
                    proba=cursor.fetchone()[0]
                except:
                    try:
                        cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree Super Normalized Features over 2000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,'<object object at 0x1ce10a0>'))
                    except:
                        print 'pau na linha 90'
                    if (matches.__float__()>1):
                        print 'EITA PORRA'
                        print (branch_id,words[i-1],words[i])
                    proba=cursor.fetchone()[0]
                    cursor.fetchall()
                
            except:
                try:
                    cursor.execute("""SELECT `son_id` FROM `rafael`.`Probability Tree Super Normalized Features over 2000 Features` WHERE `edge_id`="%s" AND `key`='<object object at 0x1ce10a0>' """%(2*star))
                except:
                    print 'pau na linha 100'
                    print 2*star
                branch_id=cursor.fetchone()[0]
                cursor.fetchall()
                try:
                    cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree Super Normalized Features over 2000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,words[i]))
                    proba=cursor.fetchone()[0]
                except:
                    cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree Super Normalized Features over 2000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,'<object object at 0x1ce10a0>'))
                    proba=cursor.fetchone()[0]
            result[star]=result[star]*proba
            partial[star]=proba
        #print (words[i-1], words[i])
        #print partial
        somme=sum(result.values())
        for key in result.keys():
            result[key]=result[key]/somme
    t1=time.time()
    print 'time ='+str(t1-t0)
    return result


def classifier_message_SQL_super_alternative(message):
    db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    cursor=db.cursor()
    cursor.execute("""SELECT * FROM `rafael`.`Significance_of_the_words` ORDER BY `rafael`.`Significance_of_the_words`.`Divergence_KL` ASC LIMIT 0,1""")
    p_stars=cursor.fetchone()
    result={5.0-i/2: 0 for i in range(10)} #p_stars[i+1]
    #message=string.replace(message,'’', '\'')
    words=re.findall(u'[^\s\',;.`’!?()/«»]+|[;!?.«»]',message)
    words.append(None)
    for i in range(len(words)-1):
        cursor.fetchall()
        result_word={5.0-i/2: 1 for i in range(10)}
        for star in result.keys():
            matches=cursor.execute("""SELECT `son_id` FROM `rafael`.`Probability Tree Super Normalized Features over 2000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(2*star, words[i-1]))
            if (matches.__float__()>1):
                print 'EITA PORRA'    
            try:
                branch_id=cursor.fetchone()[0]
                cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree Super Normalized Features over 2000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,words[i]))
                if (matches.__float__()>1):
                    print 'EITA PORRA'
                try: 
                    proba=cursor.fetchone()[0]
                except:
                    try:
                        cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree Super Normalized Features over 2000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,'<object object at 0x1ce10a0>'))
                    except:
                        print 'pau na linha 90'
                    if (matches.__float__()>1):
                        print 'EITA PORRA'
                    proba=cursor.fetchone()[0]
                        
            except:
                try:
                    cursor.execute("""SELECT `son_id` FROM `rafael`.`Probability Tree Super Normalized Features over 2000 Features` WHERE `edge_id`="%s" AND `key`='<object object at 0x1ce10a0>' """%(2*star))
                except:
                    print 'pau na linha 100'
                    print 2*star
                branch_id=cursor.fetchone()[0]
                try:
                    cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree Super Normalized Features over 2000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,words[i]))
                    proba=cursor.fetchone()[0]
                except:
                    cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree Super Normalized Features over 2000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,'<object object at 0x1ce10a0>'))
                    proba=cursor.fetchone()[0]
            result_word[star]=proba
        biggest_probability=max(result_word.values())
        for label in result_word.keys():
            if (result_word[label]==biggest_probability):
                result[label]+=1
        
    somme=sum(result.values())
    for key in result.keys():
        result[key]=result[key]/somme
    return result

def show_distribution(stars, previous_word, cursor):
    cursor.execute("""SELECT `son_id` FROM `rafael`.`Probability Tree Super Normalized Features` WHERE `edge_id`="%s" AND `key`="%s" """%(2*stars, previous_word))
    son_id=cursor.fetchone()[0]
    matches=cursor.execute("""SELECT * FROM `rafael`.`Probability Tree Super Normalized Features` WHERE `edge_id`="%s" """%son_id)
    print 'historic : '+str((stars, previous_word))
    for i in range(matches.__int__()):
        match=cursor.fetchone()
        word=match[1]
        proba=match[3]
        print 'historic : '+str((stars, previous_word))
        print 'word :'+str(word)+' -> '+str(proba)

def test_database():
    db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    print 'connection ok!'
    cursor=db.cursor()
    matches=cursor.execute("""SELECT `rating`,`review`  FROM `rafael`.`cinefrance_moviereviews` LIMIT 0,1000""")
    print 'ok!'
    green=0
    yellow=0
    red=0
    mean_green=0
    mean_yellow=0
    mean_red=0
    weird=0
    errors=[]
    mean_errors=[]
    length=int(matches.__float__())
    for i in range(length):
        variable_test=cursor.fetchone()
        rating=variable_test[0]
        review=variable_test[1]
        notations=classifier_message_SQL_super_2(review)
        print notations
        notations_probabilities=notations.values()
        try:
            biggest_probability=max(notations_probabilities)
            notations_probabilities.remove(biggest_probability)
        except:
            notations={5.0-i/2:0.1 for i in range(10)}
            weird+=1
            biggest_probability=max(notations.values())
        label=None
        for key in notations.keys():
            if (notations[key]==biggest_probability):
                label=key
        mean_label=0
        for key in notations.keys():
            mean_label+=key*notations[key]
        print '1: biggest probability'
        print (label, rating)
        print (notations[label], notations[rating])
        errors.append(abs(label-rating))
        if (abs(label-rating)<=0.5):
            green+=1
        elif (abs(label-rating)<=1.0):
            yellow+=1
        else:
            red+=1
        print '2: average notation'
        print (mean_label, rating)
        mean_errors.append(abs(mean_label-rating))
        if (abs(mean_label-rating)<=0.5):
            mean_green+=1
        elif (abs(mean_label-rating)<=1.0):
            mean_yellow+=1
        else:
            mean_red+=1
    print 'biggest probability :'
    avarage=0
    var=0
    for error in errors:
        avarage+=error
        var+=error*error
    avarage=avarage/len(errors)
    print 'avarage = '+str(avarage)
    var=var/len(errors)
    print 'variance = '+str(var)
    print 'green = '+str(green)+', yellow ='+str(yellow)+', red = '+str(red)  
    print 'average notation :'
    avarage=0
    var=0
    for error in mean_errors:
        avarage+=error
        var+=error*error
    avarage=avarage/len(mean_errors)
    print 'avarage = '+str(avarage)
    var=var/len(mean_errors)
    print 'variance = '+str(var)
    print 'green = '+str(mean_green)+', yellow ='+str(mean_yellow)+', red = '+str(mean_red)            

def current_words():
    '''give us the total of possible current words of a SQL table'''
    db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    print 'connection ok!'
    cursor=db.cursor()
    cursor.execute("""SELECT * FROM `rafael`.`cinefrance_moviereviews` LIMIT 200,300""")
    

class ProbabilityTree:
    other=Joker.other
    
    def __init__(self):
        self.probability=0
        self.occurrences=0
        self.edges={}
        self.feature_index=0
    
    def __str__(self):
        print "printing Probability Tree"
        stt=''
        count_2=0
        count_3=0
        for key_1 in self.edges.keys():
            value_1=self.edges[key_1]
            for key_2 in value_1.edges.keys():
                value_2=value_1.edges[key_2]
                count_2+=value_2.occurrences
                for key_3 in value_2.edges.keys():
                    value_3=value_2.edges[key_3]
                    count_3+=value_3.occurrences
                    stt=stt+'\n'+str((key_1, key_2, key_3, value_2.probability, value_3.probability, value_2.occurrences, value_3.occurrences)) #
        stt=stt+'\n count_2 ='+str(count_2)
        stt=stt+'\n count_3 ='+str(count_3)
        return stt     
    
    def write_tree(self, feats_tree, lamb):
        #same structure of a Features Tree, but with .probability=P(w_i|w_{i-1},s)
        #for each leaf (s,w_{i-1}, w_i})
        #print 'lambda ='+str(lamb)
        for key_1 in feats_tree.edges.keys():
            self.edges[key_1]=ProbabilityTree()
            proba_tree_1=self.edges[key_1]
            for key_2 in feats_tree.edges[key_1].edges.keys():
                proba_tree_1.edges[key_2]=ProbabilityTree()
                proba_tree_2=proba_tree_1.edges[key_2]
                proba_tree_2.occurrences=feats_tree.edges[key_1].edges[key_2].occurrences #.probability = historic empirical probability
                for key_3 in feats_tree.edges[key_1].edges[key_2].edges.keys():
                    proba_tree_2.edges[key_3]=ProbabilityTree()
                    proba_tree_3=proba_tree_2.edges[key_3]
                    proba_tree_3.occurrences=feats_tree.edges[key_1].edges[key_2].edges[key_3].occurrences
                    feature_index=feats_tree.edges[key_1].edges[key_2].edges[key_3].feature_index #.probability = word probability conditionned by the historic
                    if (type(feature_index)==int):
                        proba_tree_3.probability=math.exp(lamb[feature_index])
                    elif (type(feature_index)==tuple):
                        proba_tree_3.feature_index=feature_index
                        normalizer=(4-len(feature_index))/3
                        proba_tree_3.probability=1
                        for i in feature_index:
                            if (i==0):
                                proba_tree_3.probability*=math.exp(lamb[i]*normalizer)
                            else:
                                proba_tree_3.probability*=math.exp(lamb[i]/3)
        '''for key in feats_tree.edges.keys():
            if (feats_tree.get(key)!=None):
                self.edges[key]=ProbabilityTree()
                self.edges[key].write_tree(feats_tree.get(key),lamb)
            else:
                feature_index=feats_tree.feature_index
                if (type(feature_index)==int):
                    raise ValueError('tomar no cu')
                    self.probability=math.exp(lamb[feature_index])
                elif (type(feature_index)==tuple):
                    normalizer=(4-len(feature_index))/3
                    self.probability=1
                    for i in feature_index:
                        if (i!=0):
                            self.probability*=math.exp(lamb[i]*3)
                        else:        
                            self.probability*=math.exp(lamb[i]/normalizer)
                    print  '''
            
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
    
    def refresh_weights(self, new_lamb):
        for value_1 in self.edges.values():
            for value_2 in value_1.edges.values():
                for value_3 in value_2.edges.values():
                    value_3.probability=1
                    feature_index=value_3.feature_index
                    if (type(feature_index)==tuple):
                        normalizer=(4-len(feature_index))/3
                        for i in feature_index:
                            if (i==0):
                                value_3.probability*=math.exp(new_lamb[i]*normalizer)
                            else:
                                value_3.probability*=math.exp(new_lamb[i]/3)
                    elif (type(feature_index)==int):
                        value_3.probability=math.exp(new_lamb[feature_index])
                    else:
                        raise ValueError('wtf?')
        self.write_weights()
                        
    '''def add_feature(self, features_tree, feature_to_add):
        boo=features_tree.add_feature(feature_to_add)'''
    
    def loglikehood(self):
        result=0
        for key_1 in self.edges.keys():
            value_1=self.edges[key_1]
            for key_2 in value_1.edges.keys():
                value_2=value_1.edges[key_2]
                for key_3 in value_2.edges.keys():
                    value_3=value_2.edges[key_3]
                    p1=value_3.occurrences
                    p2=value_3.probability
                    result+=p1*math.log(p2)
        return result
        
    def test_max_loglikehood(self, epsilon, lamb):
        n=len(lamb)
        print n
        new_lamb=dict(lamb)
        old_loglikehood=self.loglikehood()
        count=0
        for i in range(n):
            new_lamb[i]+=epsilon
            self.refresh_weights(new_lamb)
            new_loglikehood=self.loglikehood()
            if (old_loglikehood<new_loglikehood):
                count+=1
            new_lamb[i]-=epsilon
        print 'fudeu '+str(count)+' vezes'    
        
        
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
                    proba=self.classifier_word(words[i],words[i-1],star)
                    print 'proba for '+str((words[i],words[i-1],star))+' : '+str(proba)
                    result[star]=result[star]*proba
            else:
                for star in result.keys():
                    proba=self.classifier_word(words[0],None,star)
                    print 'proba for '+str((words[0],None,star))+' : '+str(proba)
                    result[star]=result[star]*proba
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
                            cursor.execute("""SELECT `Probability` FROM `rafael`.`Probability Tree 10000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,words[i]))
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
        weights_file_name="Final Weights threshold 0.1 version "+str(size)+" features" #
        feats_tree=cPickle.load(open(tree_file_name))
        wei=cPickle.load(open(weights_file_name))
        print "features : "+str(feats_tree.features)
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
        
    def main_3(self, message):
        self.write_model_tree(3)
        print "Keys: "+str(self.edges.keys())
        D=self.classifier_message(message)
        return D
    
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
    
    def main_SQL_super(self, message):
        #self.write_model_tree(1000)
        D=self.classifier_message_SQL_super(message)
        return D
'''
tree=ProbabilityTree()
#print h.heap()
t0=time.time()
D=tree.main_SQL_1000("J'ai revu Avatar dernièrement. La première partie est extraordinaire : c'est l'arrivée de Jake sur Pandora, son initiation à l'Avatar, son incursion virtuelle chez les Na'vi, son rapprochement avec Neytiri, son apprentissage de la culture Na'Vi. La deuxième partie est, à mon avis bien sûr, désolante. On retrouve le cliché classique du film américain qui consiste à présenter les bons cows-boys et les méchants Indiens, ou les bons Nordistes et les méchants Sudistes, ou les bons soldats américains et les mauvais Vietnamiens. Dans Avatar, on retrouve ce même cliché désolant : ces bons américains présomptueux qui se croient nantis d'une mission divine pour s'accaparer en toute impunité, de la matière première énergétique de Pandora en faisant fi des autochtones qualifiés de sous-civilisés. Au seul nom du désir de possession du minerai, ces bons américains usent sans vergogne des armes pour éliminer les Na'vi gênants. La troisième partie est bien sûr cornélienne. Le /bon américain/ est amoureux de la /mauvaise Na'vi/ et il est pris entre le devoir de sa position de militaire et l'amour qu'il a à la fois pour Neytiri et à la fois pour la culture Na'Vi. Ici, on a affaire, comme d'habitude dans ce genre de scénario, à un groupe de bons américains défiant l'ordre établi. Et rapidement, après moults épisodes sanglants, les très méchants sont éliminés un par un et les bons Na'Vi, malgré toutes les pertes humaines et matériels qu'ils ont subies, retrouvent la sérénité qu'ils connaissaient avant l'arrivée des étrangers. Encore que le film, dans sa conclusion, reste discret sur le devenir de la station américaine sur Pandora après le cuisant échec qu'elle aura connue. Tout ça nous amène à un super long métrage qui passe sans qu'on s'en rende compte, tant sont prenantes les séquences de réel et de virtuel qui se succèdent à un rythme infernal. Un bon film en définitive au point de vue des images, du son et de l'histoire si l'on fait fi néanmoins des clichés stéréotypés décrits auparavant.")
print D 
t1=time.time()
print t1-t0
'''
'''
tree=ProbabilityTree()    
D=tree.main_SQL_super("wahoo ro qu'elle film james cameron nous a offert un magnifique cadeau sa étais un veritable chef d'oeuvre. vivement les prochain.")
tree.print_tree()
print D
'''
'''
tree=pickle.load(open("Features Tree version 3 features"))
#print tree
L=cPickle.load(open("Final Weights threshold 0.01 version 3 features"))
#L=numpy.linspace(0,0,4)
#L[1]+=math.log(2)
#L[2]+=math.log(3)
proba_tree=ProbabilityTree()
proba_tree.new_other()
#tree.remove_other()
proba_tree.write_tree(tree, L)
proba_tree.write_weights()
print L

print proba_tree
llh = proba_tree.loglikehood()
print llh
proba_tree.test_max_loglikehood(0.5, L)
'''
'''L=numpy.linspace(0,0,1001)
proba_tree=ProbabilityTree()
proba_tree.write_tree(tree, L)
proba_tree.write_weights()
print proba_tree.loglikehood()
proba_tree.test_max_loglikehood(2.0, L)
'''
'''db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
cursor=db.cursor()
star=2.0
previous_word=u'<object object at 0x25420a0>'
show_distribution(star, previous_word, cursor) ''' 
#message="C'est surement le meilleur film que je n'ai jamais vu jusqu'à maintenant. Je ne me lasse jamais de voir et revoir ce film. Un ce chef d'oeuvre."
#print classifier_message_SQL_super_2(message)
test_database()