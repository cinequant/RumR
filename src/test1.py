'''
beginning: 04/04/12
'''


import urllib2
from BeautifulSoup import BeautifulSoup
import time
import MySQLdb
import string


##################                                                                                                                                                      
# debut du script ###                                                                                                                                                   
####################                                                                                                                                                    

def insertMovieReview(id_, url, stars, comment, cursor):
    insertQuery="""INSERT INTO `rafael`.`cinefrance_moviereviews` (`movie_id`,`allocine_url`,`rating`,`review`) VALUES ("%s", "%s", "%s", "%s");"""%(id_, url, stars ,comment);
    #{"a":id_,"b":url,"c":stars,"d":comment}%
    cursor.execute(insertQuery)
    print "insertion reussite!"
    


def getMovieReviews(id, allocine_url):
    #recuperer l'url du film cercher 
    url="http://www.allocine.fr/film/fichefilm-"+allocine_url+"/critiques/spectateurs/recentes/"
    db2=MySQLdb.connect("cinequant.com","rafael","nqq2612", "rafael", use_unicode=True,charset="utf8")
    cursor2=db2.cursor()
    while True:
        print "start searching reviews at " + url
        file=urllib2.urlopen(url)
        print "access to allocine webpage successful"
        source=file.read()
        soup=BeautifulSoup (source,fromEncoding='utf-8')
        #recuperer etoiles
        StarsArray=soup.findAll ('div', attrs={'class':"stareval stars_medium "}) 
        CommentsArray=soup.findAll ('p', attrs={'class':"margin_10b"})
        i=0 
        for comment in CommentsArray[0:]:
            data1=StarsArray[i].findAll('span')[1].contents[0]
            note=data1[6:].split(' ')[0]
            print note
            text=comment.contents[0].encode('utf-8')
            text=string.replace(text,'"', '/')
            print text
            i=i+1
            if text!=None:
                insertMovieReview(id, allocine_url, note, text, cursor2)
                
                #va chercher la prochaine page 
        nextSoupTemp=soup.findAll('div',attrs={'class':"pager "})[0].find('a')
        print nextSoupTemp
        if nextSoupTemp==None:
            break
        else:
            nextSoup=nextSoupTemp['href']
            urlStart="http://www.allocine.fr"
            url=urlStart+nextSoup
            time.sleep(1) 

    
def getAllocineReviews():
    db=MySQLdb.connect("cinequant.com","rafael","nqq2612", "cqdata", use_unicode=True,charset="utf8")
    cursor=db.cursor()
    query="""SELECT `movie_id`,`allocine_url` FROM `cqdata`.`cinefrance_basicdata`"""
    cursor.execute(query)
    #print cursor.fetchall()
    for movie in cursor.fetchall():
        print movie
        getMovieReviews(movie[0],movie[1])
    
        
getAllocineReviews()        