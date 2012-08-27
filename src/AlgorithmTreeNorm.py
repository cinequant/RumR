from __future__ import division
import Joker
import FeaturesTree
import Features
import IteratorWords
import math
import pickle
import cPickle
import numpy
import time
import ProbabilityTree
import MySQLdb

def test():
    return cPickle.load(open("Allez la"))

def norm_log(x_1,x_2):
    if ((x_1>0) & (x_2>0)):
        return math.log(x_1)- math.log(x_2)
    else:
        raise ValueError('(x_1,x_2) = '+str(x_1)+' , '+str(x_2))

class AlgorithmTreeNorm:

    def __init__(self,occurrences):
        self.empirical_probability=occurrences #won't change after its creation
        self.weight=0 #will change at each step of the Algorithm
        self.edges={}


    def __str__(self):
        '''searching the tree in DFS and printing the key to every leaf'''
        print 'printing AlgorithmTreeNorm'
        stt=''
        zeros=''
        for key_1 in self.edges.keys():
            stt=stt+'\n'+str(key_1)
            value_1=self.edges[key_1]
            for key_2 in value_1.edges.keys():
                value_2=value_1.edges[key_2]
                if len(value_2.edges)==0:
                    zeros=zeros+'\n'+str((key_1, key_2))
                    #branches from iteratorwords.stars=others
                for key_3 in value_2.edges.keys():
                    stt=stt+'\n'+str((key_1, key_2, key_3, value_2.edges[key_3].empirical_probability, value_2.edges[key_3].weight)) #
            #if not boo:
                #zeros=zeros+'\n'+str(key_1)        
        return stt

    '''
    first generation: features vertex. edges -> keys: feature_index values: feature_index vertex
    second generation: features_index vertex. edges -> keys:(branch1_key, branch2_key, branch3_key). values: historic vertex
    third generation: historic vertex. edges -> keys: values: 
    '''    

    def write_tree(self,features_tree,N,features_indexes_set):
        #creating tree's first generation
        for i in range(N):
            self.edges[i]=AlgorithmTreeNorm(0)  
        #creating tree's second generation
        second_generation={}
        for feature_index in features_indexes_set:
            #here, feature_index is a tuple
            new_branch=AlgorithmTreeNorm(None)
            new_branch.weight=1
            second_generation[feature_index]=new_branch
            for i in feature_index:
                try:
                    self.edges[i].edges[feature_index]=second_generation[feature_index]
                except:
                    print feature_index
                    raise KeyError('i='+str(i)+', N = '+str(N))
        #creating tree's third generation
        for branch1_key in features_tree.edges.keys():
            if True:
                branch1=features_tree.edges[branch1_key]
                for branch2_key in branch1.edges.keys():
                    branch2=branch1.edges[branch2_key]
                    new_branch=AlgorithmTreeNorm(branch2.occurrences) #new_branch represents the context x=(s,w_1). It will be used several times as second generation
                    new_branch.weight=len(branch2.edges.keys())
                    for branch3_key in branch2.edges.keys():
                        branch3=branch2.edges[branch3_key]
                        if (branch3!=None):
                            feat_index=branch3.feature_index
                            #updating empirical_probability of the features
                            if (type(feat_index)==int):
                                raise ValueError('feature_index : '+str(features_indexes_set))
                            for i in feat_index:
                                if (i!=0):
                                    self.edges[i].empirical_probability+=branch3.occurrences/3
                                else:
                                    self.edges[i].empirical_probability+=branch3.occurrences*(4-len(feat_index))/3
                            second_generation[feat_index].edges[(branch1_key, branch2_key, branch3_key)]=new_branch #self.edges[i].edges
                        else:
                            raise ValueError('breakpoint!!')
        '''for i in self.edges.keys():
            if self.edges[i].empirical_probability==0:
                self.edges.pop(i)'''
        '''for tuple in second_generation.keys():
            if len(second_generation[tuple].edges)==0:
                raise ValueError('eita porra '+str(tuple))'''

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

    def test_write_weights(self):
        Sel=cPickle.load(open('3 selected features file'))
        tree=FeaturesTree.FeaturesTree()
        tree.write_tree(Sel)

    def p_lambda(self,i):  
        '''Probability of the feature i calculated to the vector lambda'''
        branch_i=self.edges[i]
        p_lambda_i=0
        normalizer=1/3
        for feature_index in branch_i.edges.keys():
            if (i==0):
                normalizer=(4-len(feature_index))/3
            feature_index_tree=branch_i.edges[feature_index]
            proba=feature_index_tree.weight*normalizer
            for historic_tree in feature_index_tree.edges.values():
                p_lambda_i+=proba*historic_tree.empirical_probability/historic_tree.weight
        #if p_lambda<=0:
            
        return p_lambda_i        

    def test_p_lambda(self):
        print 'test_p_lambda ='+str(sum(self.p_lambda(i) for i in range(len(self.edges))))

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

    def test_update_weight(self):
        lamb={i:self.edges[i].weight for i in range(len(self.edges))}
        print lamb
        print self
        delta_lamb=1
        self.update_weight(0, delta_lamb)
        lamb={i:self.edges[i].weight for i in range(len(self.edges))}
        print lamb
        print self
        

    def empirical_probability_test(self,sel): #OK!
        '''test for i!=0 '''
        boo=True
        iterator=IteratorWords.IteratorWords()
        normalizer=1/3    
        empirical_counter=numpy.linspace(0, 0, len(sel))
        for iter in iterator:
            for i in range(len(sel)):
                feature_tested=sel[i] #feature i+1
                if iter.word==feature_tested[2]:
                    if ((type(feature_tested[1])==object) | (iter.words[1]==feature_tested[1])):
                        if ((type(feature_tested[0])==object) | (iter.stars==feature_tested[0])):
                            empirical_counter[i]+=1
        for i in range(len(sel)):
            empirical_counter[i]*=normalizer
            if abs(empirical_counter[i]-self.edges[i+1].empirical_probability)<1e-10:
                print 'ok'
            else:
                print 'False for i = '+str(i)
                print (empirical_counter[i], self.edges[i+1].empirical_probability)
                boo=False
        if not boo:
            print 'problem'

    def weight_selection_3(self, tree):
        n=len(self.edges)
        P={j:self.p_lambda(j) for j in range(n)}
        P_tilde={j:self.edges[j].empirical_probability for j in range(n)}
        
        L={i:self.edges[i].weight for i in range(n)}
        proba_tree=ProbabilityTree.ProbabilityTree()
        proba_tree.write_tree(tree, L)
        proba_tree.write_weights()
                #booleans for saving data
        e01=True
        print n
        norm=max(numpy.abs(P[j]- P_tilde[j]) for j in range(n))
        while (norm>0.1):
            for j in range(n):
                P[j]=self.p_lambda(j)
                if True:
                    #if (numpy.abs(norm_log(P[i],P_tilde[i]))>norm/2):
                        #print (P[i],P_tilde[i])
                    if (P[j]<0):
                        raise ValueError('uepa!'+str(j)+str(self.edges[j].edges.keys())+str(self.edges[j].weight))
                    #if (P[i]==0):
                        #delta_lamb=0
                    if (P_tilde[j]==0):
                        #print 'we have a zero!'
                        #print (P[i],P_tilde[i])
                        delta_lamb=-1 #TEST!!!
                    else:
                        delta_lamb=norm_log(P_tilde[j],P[j])
                    self.update_weight(j, delta_lamb)
            
            P={j:self.p_lambda(j) for j in range(n)}
            #P[0]=self.p_lambda(0)
            somme=0
            for value in P.values():
                somme+=value
            print 'P = '+str(somme)
            norm=max(numpy.abs(P[j]-P_tilde[j]) for j in range(n))
            print 'new norm ='+str(norm)
            L={i:self.edges[i].weight for i in range(n)}
            proba_tree.refresh_weights(L)
            print 'Log vraissemblance = '+str(proba_tree.loglikehood())
            #saving time
            if (e01 & (norm<0.1)):
                #official
                L={i:self.edges[i].weight for i in range(n)}
                
                #TEST !!!
                ##L={i:0 for i in range(n)}
                cPickle.dump(L, open("Final Weights threshold 0.01 version 3 features","w")) #"Final Weights threshold 0.01 version 1000 features"
                '''
                proba_tree=ProbabilityTree.ProbabilityTree()
                proba_tree.write_tree(tree, L)
                proba_tree.write_weights()
                '''
                proba_tree.refresh_weights(L)
                print proba_tree
                proba_tree.test_max_loglikehood(0.5, L)
                #time.sleep(60)                 #cPickle.dump(proba_tree, open("Probability Tree threshold 0.1 version 10000 features","w"))
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

            '''
            if (e02 & (norm<0.01)):
                L={i:self.edges[i].weight for i in range(n)}
                cPickle.dump(L, open("Final Weights threshold 0.01 version 1000 features","w"))
                e02=False
            if (e03 & (norm<0.001)):
                L={i:self.edges[i].weight for i in range(n)}
                cPickle.dump(L, open("Final Weights threshold 0.001 version 1000 features","w"))
                e03=False    
           '''
                #print 'test: difference ='+str(P_tilde-P)
        print 'get it!'
        print 
        '''L={i:self.edges[i].weight for i in range(n)}
        cPickle.dump(L, open("Final Weights threshold 0.1 version 3 features","w"))
        '''
    
    
      
    def new_weight_selection(self, tree):
        n=len(self.edges)-1
        
        L={i:self.edges[i].weight for i in range(n+1)}
        proba_tree=ProbabilityTree.ProbabilityTree()
        proba_tree.write_tree(tree, L)
        proba_tree.write_weights()
        
        norm=numpy.abs(self.p_lambda(n)-self.edges[n].empirical_probability)
        print (self.p_lambda(n),self.edges[n].empirical_probability)
        while norm>1:
            delta_lamb=norm_log(self.edges[n].empirical_probability, self.p_lambda(n))
            self.update_weight(n, delta_lamb)
            print delta_lamb
            L={i:self.edges[i].weight for i in range(n+1)}
            #print L
            P={i:self.p_lambda(i) for i in range(n+1)}
            somme= sum(P.values())
            print somme
            norm=numpy.abs(self.p_lambda(n)-self.edges[n].empirical_probability)
            #proba_tree.refresh_weights(L)
            #proba_tree.write_weights()
            #print (self.p_lambda(n),self.edges[n].empirical_probability)
            #print 'Log vraissemblance = '+str(proba_tree.loglikehood())
        print 'new weight = '+str(self.edges[n].weight)
        return (self.edges[n].weight, proba_tree.loglikehood())

    def weight_selection(self, tree):
        n=len(self.edges)
        P={j:self.p_lambda(j) for j in range(n)}
        P_tilde={j:self.edges[j].empirical_probability for j in range(n)}
        
        L={i:self.edges[i].weight for i in range(n)}
        proba_tree=ProbabilityTree.ProbabilityTree()
        proba_tree.write_tree(tree, L)
        proba_tree.write_weights()
        #booleans for saving data
        #e00=True
        e01=True
        #e02=True
        #e03=True
        print n
        norm=max(numpy.abs(P[j]- P_tilde[j]) for j in range(n))
        somme=0
        for value in P_tilde.values():
            somme+=value
        print "p_tilde ="+str(somme)
        while (norm>0.5):
            for j in range(n):
                P[j]=self.p_lambda(j)
                if True:
                    #if (numpy.abs(norm_log(P[i],P_tilde[i]))>norm/2):
                        #print (P[i],P_tilde[i])
                    if (P[j]<0):
                        raise ValueError('uepa!'+str(j)+str(self.edges[j].edges.keys())+str(self.edges[j].weight))
                    #if (P[i]==0):
                        #delta_lamb=0
                    if (P_tilde[j]==0):
                        #print 'we have a zero!'
                        #raise ValueError('uepa !'+str(j)+str(self.edges[j].edges.keys())+str(self.edges[j].weight))
                        #print (P[i],P_tilde[i])
                        delta_lamb=-0.1 #TEST!!!
                    else:
                        delta_lamb=norm_log(P_tilde[j],P[j])
                    self.update_weight(j, delta_lamb)
            
            P={j:self.p_lambda(j) for j in range(n)}
            #P[0]=self.p_lambda(0)
            somme=0
            for value in P.values():
                somme+=value
            print 'P = '+str(somme)
            norm=max(numpy.abs(P[j]- P_tilde[j]) for j in range(n))
            print 'new norm ='+str(norm)
            #L={i:self.edges[i].weight for i in range(n)}
            #proba_tree.refresh_weights(L)
            #print 'Log vraissemblance = '+str(proba_tree.loglikehood())
            #saving time
            '''if (e00 & (norm<1)):
                L={i:self.edges[i].weight for i in range(n)}
                #cPickle.dump(L, open("Final Weights threshold 1 version 1000 features","w"))
                proba_tree=ProbabilityTree.ProbabilityTree()
                proba_tree.write_tree(self, L)
                proba_tree.write_weights()
                cPickle.dump(proba_tree, open("Probability Tree threshold 1 version 10000 features","w"))
                e00=False'''
            if (e01 & (norm<0.5)):
                #official
                L={i:self.edges[i].weight for i in range(n)}
                
                #TEST !!!
                ##L={i:0 for i in range(n)}
                cPickle.dump(L, open("Initial weights of initial features","w")) #"Final Weights threshold 0.01 version 1000 features"
                '''
                proba_tree=ProbabilityTree.ProbabilityTree()
                proba_tree.write_tree(tree, L)
                proba_tree.write_weights()
                '''
                proba_tree.refresh_weights(L)
                print L
                
                #proba_tree.test_max_loglikehood(0.5, L)
                #cPickle.dump(proba_tree, open("Probability Tree threshold 0.1 version 10000 features","w"))
                #tree in the mysql db
                db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
                cursor=db.cursor()
                index_sql=10.0
                for branch1_key in proba_tree.edges.keys():
                    branch1=proba_tree.edges[branch1_key]
                    for branch2_key in branch1.edges.keys():
                        index_sql+=1
                        cursor.execute("""INSERT INTO `rafael`.`Probability Tree Super Normalized Features` (`edge_id`, `key`, `son_id`, `proba`) VALUES  ("%s", "%s", "%s", NULL)"""%(2*branch1_key, branch2_key, index_sql))
                        branch2=branch1.edges[branch2_key]
                        for branch3_key in branch2.edges.keys():
                            branch3=branch2.edges[branch3_key]
                            cursor.execute("""INSERT INTO `rafael`.`Probability Tree Super Normalized Features` (`edge_id`, `key`, `son_id`, `proba`) VALUES ("%s","%s",NULL,"%s")"""%(index_sql, branch3_key, branch3.probability))
                e01=False
            '''
            if (e02 & (norm<0.01)):
                L={i:self.edges[i].weight for i in range(n)}
                cPickle.dump(L, open("Final Weights threshold 0.01 version 1000 features","w"))
                e02=False
            if (e03 & (norm<0.001)):
                L={i:self.edges[i].weight for i in range(n)}
                cPickle.dump(L, open("Final Weights threshold 0.001 version 1000 features","w"))
                e03=False    
           '''
                #print 'test: difference ='+str(P_tilde-P)
        print 'get it!'
        print 
        '''L={i:self.edges[i].weight for i in range(n)}
        cPickle.dump(L, open("Final Weights threshold 0.1 version 3 features","w"))
        '''

    '''def insertion_SQL(self):
        
        L=cPickle.load(open("Final Weights threshold 0.01 version 1000 features"))'''

    def test_algo(self):
        n=len(self.edges)
        P={j:self.p_lambda(j) for j in range(n)}
        P_tilde={j:self.edges[j].empirical_probability for j in range(n)}
        entropy=0
        for i in range(n):
            print (P[i], P_tilde[i])


    def main(self):
        Sel=pickle.load(open("Features of Wednesday 2"))
        Sel=list(Sel)
        print 'Sel ok!'
        print
        print 'creating our features tree: representation of all possible triple (x,y) '
        tree=FeaturesTree.FeaturesTree()
        tree.write_tree(Sel)
        print 'tree: OK!\n'
        print 'counting the empirical distributions'
        tree.count_occurrences()
        #time.sleep(10)
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
        algo_tree=AlgorithmTreeNorm(0)

        print 'creating AlgorithmTreeNorm: OK!'
        algo_tree.write_tree(tree, n, tuples.values())
        print 'writing AlgorithmTreeNorm: OK!'

        #cPickle.dump(algo_tree, open("Allez la","w"))
        #print algo_tree
        print 'getting weights:'
        algo_tree.weight_selection(tree)
        algo_tree.test_algo()
        
algo_tree=AlgorithmTreeNorm(0)
algo_tree.main()