#-*- coding: utf-8 -*-
from __future__ import division
import Joker
import FeaturesTree
#import AlgorithmTreeNorm
import cPickle
import time
import MySQLdb
import math

def test_add_feature():
    '''tree=cPickle.load(open("Features Tree version 3 features"))
    #changing Joker.other
    for key in tree.edges.keys():
        if (key.__class__==object):
            Joker.other=key
            print 'new joker :'+str(Joker.other)'''
    Sel=cPickle.load(open("3 selected features file"))
    print Sel
    tree=FeaturesTree.FeaturesTree()
    tree.write_tree(Sel)
    tree.collect_normalized_features_index(Sel)
    for key in tree.edges.keys():
        if (key.__class__==object):
            Joker.other=key
            
    for feature in Sel:
        for element in feature:
            if element.__class__==object:
                element=Joker.other
                
    stt= str(tree)
    print stt
    t0=time.time()
    #tree.to_zero_occurrences()
    feature_to_add=(5.0, '.', '.')
    Sel.append(feature_to_add)
    print Sel
    boo=tree.add_feature(feature_to_add)
    tree.collect_normalized_features_index(Sel)
    t1=time.time()
    print tree
    #tree.count_occurrences()
    t2=time.time()
    tree.remove_feature(feature_to_add, boo[0], boo[1])
    tree.collect_normalized_features_index(Sel)
    t3=time.time()
    sttt=str(tree)
    print sttt
    print stt==sttt
    print t1-t0
    print t3-t2

def test_feats_to_proba():
    Sel=cPickle.load(open("1000 selected features file"))
    L=cPickle.load(open("Final Weights threshold 0.01 version 1000 features"))
    t0=time.time()
    feats_tree=FeaturesTree.FeaturesTree()
    feats_tree.write_tree(Sel)
    norm_feats=feats_tree.collect_normalized_features_index(Sel)
    tuples=feats_tree.normalized_features(Sel)
    n=len(tuples)
    ####Ot=tree.remove_other()
    algo_tree=AlgorithmTreeNorm.AlgorithmTreeNorm(0)
    algo_tree.write_tree(feats_tree,n, norm_feats.values())
    
    '''added_proba_tree=ProbabilityTree.ProbabilityTree()
    added_proba_tree.write_tree(tree, L)
    added_proba_tree.write_weights()'''
    t1=time.time()
    print t1-t0
    #new feature and weight to add
    '''feature_to_add=(5.0, 'pas', 'pas')
    alpha=0.5
    
    Sel.append(feature_to_add)
    L[len(L)]=alpha
    print L
    print Sel
    added_proba_tree=ProbabilityTree.ProbabilityTree()
    added_proba_tree.write_tree(tree, L)
    added_proba_tree.write_weights()
    print added_proba_tree'''
    
def test_features_selection():
    #features selected by default 
    Sel=cPickle.load(open("1000 selected features file"))
    #changing Joker.other
    for feature in Sel:
        if feature[0].__class__==object:
            Joker.other=feature[0]
            print 'new Joker.other = '+str(Joker.other)
            break
    #set of candidates of features
    features_set=set([(5.0, 'dans','sa'),(4.0, Joker.other,'surtout'),(Joker.other, 'faire', 'passer')]) ####
    
    #construction of the features tree
    features_tree=FeaturesTree.FeaturesTree()
    features_tree.write_tree(Sel)
    features_tree.remove_other()
    tuples=features_tree.collect_normalized_features_index(Sel)
    norm_feats=features_tree.normalized_features(Sel)
    #stt=str(features_tree)
    Lamb=cPickle.load(open("Final Weights threshold 0.01 version 1000 features"))
    my_table={} #keys: values of loglikehood of features; values: tuple with the respective feature and its weight 
    print 'Sel = '+str(Sel)
    print 'features_set = '+str(features_set)
    for feature in features_set:
        boo=features_tree.add_feature(feature)
        features_tree.count_occurrences()
        '''sss=str(features_tree)
        time.sleep(30)
        print sss'''
        new_Sel=list(Sel)
        new_Sel.append(feature)
        tuples=features_tree.collect_normalized_features_index(new_Sel)
        norm_feats=features_tree.normalized_features(new_Sel)
        N=len(norm_feats)
        #print new_Sel
        #print norm_feats
        algo_tree=AlgorithmTreeNorm.AlgorithmTreeNorm(0)
        #print norm_feats.values()
        algo_tree.write_tree(features_tree, N, tuples.values())
        new_Lamb=dict(Lamb)
        new_Lamb[len(Lamb)]=0
        #print new_Lamb
        algo_tree.write_weights(new_Lamb)
        #print algo_tree
        iteration=algo_tree.weight_selection(features_tree)
        weight=iteration[0]
        llk=iteration[1]
        my_table[llk]=(feature,weight)
        features_tree.remove_feature(feature, boo[0], boo[1])
        features_tree.to_zero_occurrences()
        #sttt=str(features_tree)
        #print 'good tree : '+str(stt==sttt)
        print 'can do it'
    selected= my_table[max(my_table.keys())]
    Sel.append(selected[0])
    features_set.remove(selected[0])
    Lamb[len(Lamb)]=selected[1]
    print Sel
    print features_set
    print Lamb

def test_features_selection_2():
    Sel=cPickle.load(open("1000 selected features file"))
    for feature in Sel:
        if feature[0].__class__==object:
            Joker.other=feature[0]
            print 'new Joker.other = '+str(Joker.other)
            break
    print 'Sel ok!'
    #set of candidates of features
    features_set=set([(5.0, 'dans','sa'),(4.0, Joker.other,'surtout'),(Joker.other, 'faire', 'passer')]) ####
    print
    print 'creating our features tree: representation of all possible triple (x,y) '
    tree=FeaturesTree.FeaturesTree()
    tree.write_tree(Sel)
    print 'tree: OK!\n'
    print 'counting the empirical distributions'
    tree.count_occurrences()
    print 'start normalized_features'
    tuples=tree.collect_normalized_features_index(Sel) #dict with the second generation algo_tree
    #tree.edges[Joker.other]=Ot
    print 'end of normalized_features'
    norm_feats=tree.normalized_features(Sel)
    n=len(norm_feats) #number of normalized features
    print str(n)+' normalized features'

    print 'tree saved\n'
    #print 'EXCLUDING OTHERS!'


    print tree.edges.keys()
    print 'saving tree\n'
    #cPickle.dump(tree, open("Features Tree version 1000 features","w"))
    Ot=tree.remove_other()
    print tree.edges.keys()
    Lamb=cPickle.load(open("Final Weights threshold 0.01 version 1000 features"))
    my_table={} #keys: values of loglikehood of features; values: tuple with the respective feature and its weight 
    for feature in features_set:
        boo=tree.add_feature(feature)
        tree.count_occurrences()
        '''sss=str(features_tree)
        time.sleep(30)
        print sss'''
        new_Sel=list(Sel)
        new_Sel.append(feature)
        tuples=tree.collect_normalized_features_index(new_Sel)
        norm_feats=tree.normalized_features(new_Sel)
        N=len(norm_feats)
        #print new_Sel
        #print norm_feats
        algo_tree=AlgorithmTreeNorm.AlgorithmTreeNorm(0)
        #print norm_feats.values()
        algo_tree.write_tree(tree, N, tuples.values())
        
        new_Lamb=dict(Lamb)
        new_Lamb[len(Lamb)]=0
        #print new_Lamb
        #algo_tree.write_weights(new_Lamb)
        for i in range(len(new_Lamb)):
            algo_tree.update_weight(i, new_Lamb[i])
        #print algo_tree
        try:
            iteration=algo_tree.new_weight_selection(tree)
        except:
            print 'deu merda'
            for value_1 in algo_tree.edges.values():
                for key_2 in value_1.edges.keys():
                    value_2=value_1.edges[key_2]
                    for key_3 in value_2.edges.keys():
                        if value_2.edges[key_3].weight<0:
                            print (key_2, key_3, value_2.edges[key_3].weight)
            raise ValueError('pronto')
        weight=iteration[0]
        llk=iteration[1]
        my_table[llk]=(feature,weight)
        tree.remove_feature(feature, boo[0], boo[1])
        tree.to_zero_occurrences()
        #sttt=str(features_tree)
        #print 'good tree : '+str(stt==sttt)
        print 'can do it'
    selected= my_table[max(my_table.keys())]
    Sel.append(selected[0])
    features_set.remove(selected[0])
    Lamb[len(Lamb)]=selected[1]
    print Sel
    print features_set
    print Lamb

def test_initial_features():
    sel_0=cPickle.load(open('Initial features'))
    tree=FeaturesTree.FeaturesTree()
    tree.write_tree(sel_0)
    tree.count_occurrences()
    tree.remove_other()
    print tree
    #TEST OK!

def features_set_method():
    ll=cPickle.load(open('tableau de tous les features'))
    l=set(ll)
    sel_occurrences=cPickle.load(open('10000 selected features file'))
    db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    cursor=db.cursor()
    cursor.execute("""SELECT * FROM `rafael`.`significance_of_sequence_of_words` ORDER BY `significance_of_sequence_of_words`.`Divergence_KL` DESC LIMIT 0, 700""")
    my_table=cursor.fetchall()
    S=set()
    for t in my_table:
        for i in range(10):
            star=5.0-i/2
            if t[i+2]>0.05:
                S.add((star, t[1], t[0]))
    print len(S)
    raise ValueError('parou')
    sel_occurrences=sel_occurrences[100:900]
    sel_occurrences_set=set(sel_occurrences)
    for feat in sel_occurrences:
        if feat[1].__class__!=object:
            sel_occurrences_set.remove(feat)
    sel_occurrences=list(sel_occurrences_set)
    print len(sel_occurrences_set)
    SS= S.union(sel_occurrences_set)
    sel_0=cPickle.load(open('Initial features'))
    init=set(sel_0)
    print SS.isdisjoint(init)
    print init
    tt=[0.5, 1.0, 1.5, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    for feat in sel_occurrences:
        s=feat[0]
        w_0=feat[1]
        w_1=feat[2]
        if s.__class__!=object:
            for ss in tt:
                if (ss, w_0, w_1) in l:
                    sel_occurrences_set.add((ss, w_0, w_1))
    print len(sel_occurrences_set)
    SS= SS.union(sel_occurrences_set)
    SS=SS.union(init)
    print len(SS)
    '''for feat in sel_0:
        if feat in SS:
            SS.remove(feat)'''
    print len(SS)
    
    cPickle.dump(SS, open('Features of Wednesday 2', 'w'))
    #cPickle.load(open('Features set before selection'))
    print 'ok !'
    '''try:
        LL=[ll[i] for i in list(SS)]
    except:
        print len(LL)
    if 0 in LL:
        print 'que porra eh essa' '''
    
def features_set_method_2():
    sel_occurrences=cPickle.load(open('Features over 10 occurrences'))
    sel_occurrences.remove(' ')
    #sel_occurrences=Features[0]
    new_features=set()
    db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
    cursor=db.cursor()
    checked_tuples=set()
    
    for feat in sel_occurrences:
        try:
            w_0=feat[1]
            w_1=feat[2]
        except:
            print feat
            raise ValueError()
        if (w_1,w_0) not in checked_tuples:
            checked_tuples.add((w_1,w_0))
            if w_0.__class__!=object:
                match=cursor.execute("""SELECT * FROM `rafael`.`significance_of_sequence_of_words` WHERE `Word`="%s" AND `Previous Word`="%s" AND `Divergence_KL`>0.7"""%(w_1, w_0))
                if match.__float__()>0:
                    match_fetch=cursor.fetchone()
                    p_cond_star={5.0-i/2:match_fetch[i+2] for i in range(10)}
                    new_features.add((Joker.other, w_0,w_1))
                    for star in p_cond_star.keys():
                        if p_cond_star[star]>0:
                            new_features.add((star, w_0,w_1))
            else:
                match=cursor.execute("""SELECT * FROM `rafael`.`significance_of_the_words` WHERE `Word`="%s" AND `Divergence_KL`>0.8"""%w_1)
                if match.__float__()>0:
                    match_fetch=cursor.fetchone()
                    p_cond_star={5.0-i/2:match_fetch[i+1] for i in range(10)}
                    for star in p_cond_star.keys():
                        if p_cond_star[star]>0:
                            new_features.add((star, w_0,w_1))
    

    cPickle.dump(new_features, open('Features of 13 08', 'w'))
    print len(new_features)
    #cPickle.load(open('Features set before selection'))
    print 'ok !'
    '''try:
        LL=[ll[i] for i in list(SS)]
    except:
        print len(LL)
    if 0 in LL:
        print 'que porra eh essa' '''
    
    
def features_selection():
    sel_initial=cPickle.load(open("Initial features"))
    print 'sel_initial ok!'
    #set of candidates of features
    features_set=cPickle.load(open('Features set before selection')) ####
    #features_set.remove(' ')
    for feature in features_set:
        if feature[0].__class__==object:
            Joker.other=feature[0]
            print 'new Joker.other = '+str(Joker.other)
            break
    for feature in sel_initial:
        print feature
        if feature[0].__class__==object:
            feature=(Joker.other, feature[1], feature[2])
        if feature[1].__class__==object:
            feature=(feature[0], Joker.other, feature[2])
        
    print
    print 'creating our features tree: representation of all possible triple (x,y) '
    tree=FeaturesTree.FeaturesTree()
    tree.write_tree(sel_initial)
    print 'tree: OK!\n'
    print 'counting the empirical distributions'

    tree.count_occurrences()

    print 'start normalized_features'
    tuples=tree.collect_normalized_features_index(sel_initial) #dict with the second generation algo_tree
    #tree.edges[Joker.other]=Ot
    print 'end of normalized_features'
    norm_feats=tree.normalized_features(sel_initial)
    n=len(norm_feats) #number of normalized features
    print str(n)+' normalized features'
    
    print 'tree saved\n'
    #print 'EXCLUDING OTHERS!'
    
    #print primary_tree
    sss=[set() for i in range(10)]
    j=0
    for star in tree.edges.keys():
        for feature in features_set:
            if feature[0]==star:
                sss[j].add(feature)
                j+=1
                if j>9:
                    j=0
    Ot=tree.remove_other()
    for p in range(1000):
        for q in range(1000):
            if p!=q and (not sss[p].isdisjoint(sss[q])):
                raise ValueError('olha o problema')
    ''' 
    while len(features_set)!=0:
        sss[j].add(features_set.pop())
        j+=1
        if j>999:
            j=0'''
    '''mega_sel=list(sss[0])
    print mega_sel[0]
    primary_tree=FeaturesTree.FeaturesTree()
    primary_tree.write_tree(mega_sel)
    primary_tree.count_occurrences()
    primary_tree.collect_normalized_features_index(mega_sel)
    primary_tree.remove_other()
    print primary_tree.edges.keys()
    #raise ValueError('ops')'''
    
    print tree.edges.keys()
    print 'saving tree\n'
    #cPickle.dump(tree, open("Features Tree version 1000 features","w"))
    
    print tree.edges.keys()
    tree.to_zero_occurrences()
    Lamb=cPickle.load(open("Initial weights of initial features"))
    
    for k in range(10000):
        kmod=int(math.fmod(k,10))
        mega_sel=list(sss[kmod])
        print mega_sel[0]
        primary_tree=FeaturesTree.FeaturesTree()
        primary_tree.write_tree(mega_sel)
        primary_tree.count_occurrences()
        primary_tree.collect_normalized_features_index(mega_sel)
        primary_tree.remove_other()
        print primary_tree.edges.keys()
        my_table={} #keys: values of loglikehood of features; values: tuple with the respective feature and its weight
        for feature in sss[kmod]:
            boo=tree.add_feature(feature)
            tree.count_occurrences_by_primary_tree(primary_tree)
            '''sss=str(features_tree)
            time.sleep(30)
            print sss'''
            new_Sel=list(sel_initial)
            new_Sel.append(feature)
            tuples=tree.collect_normalized_features_index(new_Sel)
            norm_feats=tree.normalized_features(new_Sel)
            N=len(norm_feats)
            #print new_Sel
            #print norm_feats
            algo_tree=AlgorithmTreeNorm.AlgorithmTreeNorm(0)
            #print norm_feats.values()
            print N
            algo_tree.write_tree(tree, N, tuples.values())
            print algo_tree
            P={i:algo_tree.p_lambda(i) for i in range(N)}
            print 'agora tá de:'
            print sum(P.values())
            new_Lamb=dict(Lamb)
            new_Lamb[len(Lamb)]=0
            #print new_Lamb
            #algo_tree.write_weights(new_Lamb)
            print new_Lamb
            for i in range(len(new_Lamb)):
                algo_tree.update_weight(i, new_Lamb[i])
            #print algo_tree
            iteration=algo_tree.new_weight_selection(tree)
            weight=iteration[0]
            llk=iteration[1]
            my_table[llk]=(feature,weight)
            tree.remove_feature(feature, boo[0], boo[1])
            tree.to_zero_occurrences()
            #sttt=str(features_tree)
            #print 'good tree : '+str(stt==sttt)
            print 'can do it'
        selected= my_table[max(my_table.keys())]
        sel_initial.append(selected[0])
        sss[kmod].remove(selected[0])
        Lamb[len(Lamb)]=selected[1]
        print sel_initial
        print sss[kmod]
        print Lamb 
        if int(math.fmod(kmod,100))==1:
            cPickle.dump(sel_initial, open('Final selected features out of features over 12000 features', 'w'))
            cPickle.dump(Lamb, open('Final selected weights out of features over 12000 features', 'w'))
    
    
def test_count_occurrences_by_primary_tree():
    sel_initial=cPickle.load(open("Initial features"))
    for feature in sel_initial:
        if feature[0].__class__==object:
            Joker.other=feature[0]
            print 'new Joker.other = '+str(Joker.other)
            break
    print 'sel_initial ok!'
    #set of candidates of features
    features_set=cPickle.load(open('Features set before selection')) ####
    print
    print 'creating our features tree: representation of all possible triple (x,y) '
    tree=FeaturesTree.FeaturesTree()
    tree.write_tree(sel_initial)
    print 'tree: OK!\n'
    print 'counting the empirical distributions'

    tree.count_occurrences()
    
    
    print 'start normalized_features'
    tuples=tree.collect_normalized_features_index(sel_initial) #dict with the second generation algo_tree
    #tree.edges[Joker.other]=Ot
    print 'end of normalized_features'
    norm_feats=tree.normalized_features(sel_initial)
    n=len(norm_feats) #number of normalized features
    print str(n)+' normalized features'

    print 'tree saved\n'
    #print 'EXCLUDING OTHERS!'
    mega_sel=list(features_set)
    primary_tree=FeaturesTree.FeaturesTree()
    primary_tree.write_tree(mega_sel)
    primary_tree.count_occurrences()
    primary_tree.collect_normalized_features_index(mega_sel)
    primary_tree.remove_other()
    #print primary_tree
    
    #cPickle.dump(tree, open("Features Tree version 1000 features","w"))
    Ot=tree.remove_other()
    stt=str(tree)
    tree.to_zero_occurrences()
    print tree.edges.keys()
    tree.count_occurrences_by_primary_tree(primary_tree)
    sttt=str(tree)
    print stt==sttt
        
#test_add_feature()
#test_features_selection_2()
#test_initial_features()
#test_count_occurrences_by_primary_tree()
features_set_method_2()
#features_selection()