#-*- coding: utf-8 -*-
#from django.core.context_processors import csrf
from __future__ import division
from django.template import RequestContext, Context, loader
#from polls.models import Poll
from django.http import HttpResponse
from django.shortcuts import render_to_response,render
from pygooglechart import StackedVerticalBarChart
import sys
sys.path.append('/home/rafael/RumR/Projet/RumR/src')
import MySQLdb
import re
import string
import time
#import ProbabilityTree

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

def classifier_message_SQL_10000(message):
        db=MySQLdb.connect("217.160.235.17","rafael","rafael","rafael",use_unicode=True,charset="utf8")
	print 'connection ok!'
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
		    matches=cursor.execute("""SELECT `son_id` FROM `rafael`.`Probability Tree 10000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(2*star, words[i-1]))
		    try:
                        branch_id=cursor.fetchone()[0]
                        cursor.execute("""SELECT * FROM `rafael`.`Probability Tree 10000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,words[i]))
			if (matches.__float__()>1):
		            print 'EITA PORRA'
			    print [branch_id, words[i-1], None, None]
			    print matches.fetchone()
			    print 
			    fetched=matches.fetchone()
			    print fetched
			    print
			try: 
                            proba=fetched[3]
			    	
                        except:
                            cursor.execute("""SELECT * FROM `rafael`.`Probability Tree 10000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,'<object object at 0x21830a0>'))
			    if (matches.__float__()>1):
		                print 'EITA PORRA'
				print [branch_id, None, None]
				
                            proba=cursor.fetchone()[3]
                        
                    except:
			cursor.execute("""SELECT `son_id` FROM `rafael`.`Probability Tree 10000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(2*star,'<object object at 0x21830a0>'))
			branch_id=cursor.fetchone()[0]
			try:
                            cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree 10000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,word[i]))
                            proba=cursor.fetchone()[0]
			    
                        except:
                            cursor.execute("""SELECT `proba` FROM `rafael`.`Probability Tree 10000 Features` WHERE `edge_id`="%s" AND `key`="%s" """%(branch_id,'<object object at 0x21830a0>'))
                            proba=cursor.fetchone()[0]
		    print (star, words[i-1], words[i])
		    print proba    
		    result[star]=result[star]*proba
        somme=sum(result.values())
        for key in result.keys():
            result[key]=result[key]/somme
        return result

def index(request):
    #t = loader.get_template("index.html")
    #c = Context({})
    #output = ', '.join([p.question for p in latest_poll_list])
    return render (request,'index.html',{})

def detail(request,poll_id):
    S="First line \n Second Line \n"
    print S
    return HttpResponse("Look at \n this number : %s" %poll_id)

def notation(request):
    t0=time.time()
    #c = {}
    #c.update(csrf(request))
    try:
        message=request.POST["critique"]
        #message=string.replace(message,'’', '\'')
	#proba_tree=ProbabilityTree.ProbabilityTree()
	#output=proba_tree.main_3(message)
	output=classifier_message_SQL_super(message)
    except:
	return HttpResponse("erreur")
    chart = StackedVerticalBarChart(400, 400, y_range=(0, 70))
    chart.set_bar_width(30)
    chart.set_colours(['f87217'])
    print output
    labels=[]
    bars=[]
    for key in sorted(output.keys()):
        labels.append(key)
        bars.append(67*output[key])
    chart.set_axis_labels('x',labels)
    chart.add_data(bars)
    y_axis=['0 %', '10 %', '20 %', '30 %', '40 %', '50 %', '60 %', '70 %', '80 %', '90 %', '100 %']
    chart.set_axis_labels('y', y_axis)
    new_url=chart.get_url()
    t1=time.time()
    print t1-t0
    return HttpResponse(new_url)
