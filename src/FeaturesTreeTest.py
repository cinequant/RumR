#-*- coding: utf-8 -*-
from __future__ import division
import Joker
import FeaturesTree
import cPickle

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
    #changing Joker.other
    for key in tree.edges.keys():
        if (key.__class__==object):
            Joker.other=key
            print 'new joker :'+str(Joker.other)
    stt= str(tree)
    print stt
    #tree.to_zero_occurrences()
    feature_to_add=(5.0, '.', '.')
    Sel.append(feature_to_add)
    print Sel
    boo=tree.add_feature(feature_to_add)
    tree.collect_normalized_features_index(Sel)
    print tree
    #tree.count_occurrences()
    #print tree
    tree.remove_feature(feature_to_add, boo[0], boo[1])
    sttt=str(tree)
    print stt==sttt
    
test_add_feature()
#tests are okay!!