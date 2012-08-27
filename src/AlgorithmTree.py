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

class AlgorithmTree:
    
    def __init__(self,occurrences):
        self.empirical_probability=occurrences #won't change after its creation
        self.weight=0 #will change at each step of the Algorithm
        self.edges={}
        
    def __str__(self):
        print 'printing AlgorithmTree'
        stt=''
        zeros=''
        for key_1 in self.edges.keys():
            stt=stt+'\n'+str(key_1)
            boo=False
            value_1=self.edges[key_1]
            for key_2 in value_1.edges.keys():
                value_2=value_1.edges[key_2]
                boo=True
                stt=stt+'\n'+str((key_1, key_2, value_2.empirical_probability, value_1.weight)) #
            #if not boo:
                #zeros=zeros+'\n'+str(key_1)        
        return stt    
        
        
        
    def write_tree(self,features_tree,lenght):
        for i in range(lenght):
            self.edges[i]=AlgorithmTree(0)
        for branch1_key in features_tree.edges.keys():
            if True:
                branch1=features_tree.edges[branch1_key]
                for branch2_key in branch1.edges.keys():
                    branch2=branch1.edges[branch2_key]
                    new_branch=AlgorithmTree(branch2.occurrences) #new_branch represents the context x=(s,w_1). It will be used several times as second generation
                    for branch3_key in branch2.edges.keys():
                        branch3=branch2.edges[branch3_key]
                        if (branch3!=None):
                            feature_index=branch3.feature_index
                            self.edges[feature_index].empirical_probability+=branch3.occurrences
                            self.edges[feature_index].edges[(branch1_key,branch2_key,branch3_key)]=new_branch
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
            for context_tree in self.edges[i].edges.values():
                context_tree.weight+=math.exp(lamb[i])
                            
    def p_lambda(self,i): #New Features
        '''Probability (no empirical) of the feature i'''
        branch_i=self.edges[i]
        p_lambda_i=0
        for historic in branch_i.edges.values():
            p_lambda_i+=historic.empirical_probability/historic.weight
        return math.exp(branch_i.weight)*p_lambda_i
    
    def p_lambda_norm(self,i): #Normilized Features
        '''Probability (no empirical) of the feature i'''
        branch_i=self.edges[i]
        p_lambda_i=0
        for historic in branch_i.edges.values():
            p_lambda_i+=historic.empirical_probability/historic.weight
    
    def update_weight(self,i,delta_lamb):
        old_lamb=self.edges[i].weight
        new_lamb=old_lamb+delta_lamb
        self.edges[i].weight=new_lamb
        for branch_key in self.edges[i].edges.keys():
            self.edges[i].edges[branch_key].weight=self.edges[i].edges[branch_key].weight - math.exp(old_lamb) + math.exp(new_lamb)
            
            
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
        
        L={i:self.edges[i].weight for i in range(n)}
        proba_tree=ProbabilityTree.ProbabilityTree()
        proba_tree.write_tree(tree, L)
        proba_tree.write_weights()
        print proba_tree
        raise ValueError('rrr')
        for j in range(n):
            norm=numpy.maximum(norm,numpy.abs(P[j]-P_tilde[j]))
        while (norm>1e-04):
            for i in range(n):
                P[i]=self.p_lambda(i)
                if ((P[i]-P_tilde[i]>1e-04) | (P_tilde[i]-P[i]>1e-04)):
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
            L={i:self.edges[i].weight for i in range(n)}
            print 'L = '+str(L)
            proba_tree.refresh_weights(L)
            print 'Log vraissemblance = '+str(proba_tree.loglikehood())
            #print proba_tree
            #saving time
            '''if (e00 & (norm<1)):
                L={i:self.edges[i].weight for i in range(n)}
                #cPickle.dump(L, open("Final Weights threshold 1 version 1000 features","w"))
                proba_tree=ProbabilityTree.ProbabilityTree()
                proba_tree.write_tree(self, L)
                proba_tree.write_weights()
                cPickle.dump(proba_tree, open("Probability Tree threshold 1 version 1000 features","w"))
                e00=False'''
            if (e01 & (norm<0.1)):
                raise ValueError('parou')
                #L={i:self.edges[i].weight for i in range(n)}
                #cPickle.dump(L, open("Final Weights threshold 0.1 version 1000 features","w"))
                #proba_tree=ProbabilityTree.ProbabilityTree()
                #proba_tree.write_tree(tree, L)
                #proba_tree.write_weights()
                #cPickle.dump(proba_tree, open("Probability Tree threshold 0.1 version 1000 features","w"))
                #tree in the mysql db
                db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
                cursor=db.cursor()
                index_sql=10.0
                for branch1_key in proba_tree.edges.keys():
                    branch1=proba_tree.edges[branch1_key]
                    for branch2_key in branch1.edges.keys():
                        index_sql+=1
                        cursor.execute("""INSERT INTO `rafael`.`Probability Tree 1000 Features` (`edge_id`, `key`, `son_id`, `proba`) VALUES  ("%s", "%s", "%s", NULL)"""%(2*branch1_key, branch2_key, index_sql))
                        branch2=branch1.edges[branch2_key]
                        for branch3_key in branch2.edges.keys():
                            branch3=branch2.edges[branch3_key]
                            cursor.execute("""INSERT INTO `rafael`.`Probability Tree 1000 Features` (`edge_id`, `key`, `son_id`, `proba`) VALUES ("%s","%s",NULL,"%s")"""%(index_sql, branch3_key, branch3.probability))
                            
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
print 'tree: OK!'
print

t0=time.time()
print 'start new_features'
new_feats=tree.new_features()
#tree.edges[Joker.other]=Ot
print 'end of new_features'
t1=time.time()
t=t1-t0
print 'temps d execution de new_features avec un dict :'+str(t)
n=len(new_feats)
print str(n)+' new features'
print 'removing sets'
#tree.remove_features()
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
algo_tree=AlgorithmTree(0)
print 'creating AlgorithmTree: OK!'
algo_tree.write_tree(tree,n)
print 'writing AlgorithmTree: OK!'
algo_tree.write_weights(lamb)
print 'weighting AlgorithmTree: OK!'
print 'getting weights:'
algo_tree.weight_selection(tree)
