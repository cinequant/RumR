from __future__ import division
import Joker
import FeaturesTree
import Features
import math
import pickle
import cPickle
import numpy
import time
import ProbabilityTree
import MySQLdb

class AlgorithmTreeNorm:
    
    def __init__(self,occurrences):
        self.empirical_probability=occurrences #won't change after its creation
        self.weight=0 #will change at each step of the Algorithm
        self.edges={}
        
        
    '''
    first generation: features vertex. edges -> keys: 1/3, 2/3 or 1. values: features_index vertex
    second generation: features_index vertex. edges -> keys:(branch1_key, branch2_key, branch3_key). values: historic vertex
    third generation: historic vertex. edges -> keys: values: 
    '''    
        
    def write_tree(self,features_tree,lenght, sel):
        #creating tree's first generation
        for i in range(lenght):
            self.edges[i]=AlgorithmTreeNorm(0)
        features_indexes_set=features_tree.collect_normalized_features_index(sel)
        #creating tree's second generation
        for feature_index in features_indexes_set:
            #here, feature_index is a tuple
            new_branch=AlgorithmTreeNorm(None)
            new_branch.weight=1
            for i in feature_index:
                self.edges[i].edges[feature_index]=new_branch   
        #creating tree's third generation              
        for branch1_key in features_tree.edges.keys():
            if True:
                branch1=features_tree.edges[branch1_key]
                for branch2_key in branch1.edges.keys():
                    branch2=branch1.edges[branch2_key]
                    new_branch=AlgorithmTreeNorm(branch2.occurrences) #new_branch represents the context x=(s,w_1). It will be used several times as second generation
                    for branch3_key in branch2.edges.keys():
                        branch3=branch2.edges[branch3_key]
                        if (branch3!=None):
                            feature_index=branch3.feature_index
                            #updating empirical_probability of the features
                            for i in feature_index:
                                if (i!=0):
                                    self.edges[i].empirical_probability+=branch3.occurrences/3
                                else:
                                    self.edges[i].empirical_probability+=branch3.occurrences*(4-len(feature_index))/3
                            new_branch.weight+=1        
                            self.edges[i].edges[feature_index].edges[(branch1_key,branch2_key,branch3_key)]=new_branch
                        else:
                            print 'breakpoint!!'
                            print branch3_key
                            print branch2_key
                            print branch1_key
                    
         
    #if we use features_tree.feature_index as an int, we use the method of New Features
    #otherwise, if we use features_tree.feature_index as a tuple, we use the method of Normalized Features     
         
    def write_weights(self,lamb):
        n=len(lamb)
        for i in range(n):
            self.edges[i].weight=lamb[i]
            for feature_index in self.edges[i].edges.keys():
                feature_index_tree=self.edges[i].edges[feature_index]
                if (i!=0):
                    normalizer=1/3
                else:
                    normalizer=(4-len(feature_index))/3
                old_weight=feature_index_tree.weight
                new_weight=old_weight*math.exp(lamb[i]*normalizer)
                feature_index_tree.weight=new_weight
            for historic_tree in self.edges[i].edges[feature_index].edges.values():
                historic_tree.weight+=new_weight-old_weight
    
    def p_lambda(self,i): #Normalized Features
        '''Probability (no empirical) of the feature i'''
        branch_i=self.edges[i]
        p_lambda_i=0
        for feature_index_tree in branch_i.edges.values():
            proba=feature_index_tree.weight
            for historic_tree in feature_index_tree.edges.values():
                p_lambda_i+=proba*historic_tree.empirical_probability/historic_tree.weight
        return p_lambda_i        
    
    def update_weight(self,i,delta_lamb):
        old_lamb=self.edges[i].weight
        new_lamb=old_lamb+delta_lamb
        self.edges[i].weight=new_lamb
        for feature_index in self.edges[i].edges.keys():
            if (i!=0):
                normalizer=1/3
            else:
                normalizer=(4-len(feature_index))/3
            old_probability=self.edges[i].edges[feature_index].weight
            new_probability=old_probability*math.exp(new_lamb*normalizer)/math.exp(old_lamb*normalizer)
            self.edges[i].edges[feature_index].weight=new_probability
            for historic_tree in self.edges[i].edges[feature_index].edges.values():
                historic_tree.weight+=new_probability-old_probability
            
            
    def weight_selection(self, tree):
        n=len(self.edges)
        P={i:self.p_lambda(i) for i in range(n)}
        P_tilde={i:self.edges[i].empirical_probability for i in range(n)}
        #booleans for saving data
        #e00=True
        e01=True
        #e02=True
        #e03=True
        norm=0
        for j in range(n):
            norm=numpy.maximum(norm,numpy.abs(P[j]-P_tilde[j]))
        while (norm>1e-04):
            for i in range(n):
                P[i]=self.p_lambda(i)
                if ((P[i]-P_tilde[i]>1e-08) | (P_tilde[i]-P[i]>1e-08)):
                    if (numpy.abs(P[i]-P_tilde[i])>norm/2):
                        print (P[i],P_tilde[i])
                    if (P[i]<0):
                        print 'uepa!'
                        print i
                        print self.edges[i].edges.keys()
                        print self.edges[i].weight
                    '''if (P[i]==0):
                        delta_lamb=0'''
                    if (P_tilde[i]==0):
                        #print 'we have a zero!'
                        #print (P[i],P_tilde[i])
                        delta_lamb=-1 #TEST!!!
                    else:
                        delta_lamb=math.log(P_tilde[i]) - math.log(P[i])
                    self.update_weight(i, delta_lamb)
            #P={i:self.p_lambda(i) for i in range(n)}
            P[0]=self.p_lambda(0)
            norm=numpy.abs(P[0]-P_tilde[0])
            print 'new norm ='+str(norm)
            #saving time
            '''if (e00 & (norm<1)):
                L={i:self.edges[i].weight for i in range(n)}
                #cPickle.dump(L, open("Final Weights threshold 1 version 1000 features","w"))
                proba_tree=ProbabilityTree.ProbabilityTree()
                proba_tree.write_tree(self, L)
                proba_tree.write_weights()
                cPickle.dump(proba_tree, open("Probability Tree threshold 1 version 10000 features","w"))
                e00=False'''
            if (e01 & (norm<0.1)):
                L={i:self.edges[i].weight for i in range(n)}
                #cPickle.dump(L, open("Final Weights threshold 0.1 version 1000 features","w"))
                proba_tree=ProbabilityTree.ProbabilityTree()
                proba_tree.write_tree(tree, L)
                proba_tree.write_weights()
                #cPickle.dump(proba_tree, open("Probability Tree threshold 0.1 version 10000 features","w"))
                #tree in the mysql db
                db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
                cursor=db.cursor()
                index_sql=10.0
                for branch1_key in proba_tree.edges.keys():
                    branch1=proba_tree.edges[branch1_key]
                    for branch2_key in branch1.edges.keys():
                        index_sql+=1
                        cursor.execute("""INSERT INTO `rafael`.`Probability Tree 1000 Normalized Features` (`edge_id`, `key`, `son_id`, `proba`) VALUES  ("%s", "%s", "%s", NULL)"""%(2*branch1_key, branch2_key, index_sql))
                        branch2=branch1.edges[branch2_key]
                        for branch3_key in branch2.edges.keys():
                            branch3=branch2.edges[branch3_key]
                            cursor.execute("""INSERT INTO `rafael`.`Probability Tree 1000 Normalized Features` (`edge_id`, `key`, `son_id`, `proba`) VALUES ("%s","%s",NULL,"%s")"""%(index_sql, branch3_key, branch3.probability))
                            
                e01=False
            '''if (e02 & (norm<0.01)):
                L={i:self.edges[i].weight for i in range(n)}
                cPickle.dump(L, open("Final Weights threshold 0.01 version 1000 features","w"))
                e02=False
            if (e03 & (norm<0.001)):
                L={i:self.edges[i].weight for i in range(n)}
                cPickle.dump(L, open("Final Weights threshold 0.001 version 1000 features","w"))
                e03=False    '''
                #print 'test: difference ='+str(P_tilde-P)
        print 'get it!'
        print 
        #L={i:self.edges[i].weight for i in range(n)}
        #cPickle.dump(L, open("Final Weights version 1000 features","w"))
                       
Sel=pickle.load(open("1000 selected features file"))
print 'Sel ok!'
print
print 'creating our features tree: representation of all possible triple (x,y) '
tree=FeaturesTree.FeaturesTree()
tree.write_tree(Sel)
print 'tree: OK!\n'
print 'start normalized_features'
norm_feats=tree.normalized_features(Sel)
#tree.edges[Joker.other]=Ot
print 'end of normalized_features'
n=len(norm_feats)
print str(n)+' new features'
print 'saving tree\n'
#cPickle.dump(tree, open("Features Tree version 1000 features","w"))
print 'tree saved\n'
#print 'EXCLUDING OTHERS!'


print 'counting the empirical distributions'
tree.count_occurrences()
print 'finish counting'
print tree.edges.keys()
Ot=tree.remove_other()
print tree.edges.keys()
lamb=numpy.linspace(0,0,n)       
algo_tree=AlgorithmTreeNorm(0)

print 'creating AlgorithmTreeNorm: OK!'
algo_tree.write_tree(tree,n, Sel)
print 'writing AlgorithmTreeNorm: OK!'
algo_tree.write_weights(lamb)
print 'weighting AlgorithmTreeNorm: OK!'

print 'getting weights:'
algo_tree.weight_selection(tree)
