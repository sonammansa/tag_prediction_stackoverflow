import matplotlib.pyplot as plotter
import MySQLdb
import numpy as np
import scipy.sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
from decimal import *
from random import randrange
# Open database connection
db = MySQLdb.connect("localhost","root","","major" )

# prepare a cursor object using cursor() method
cursor = db.cursor()


def test1():
        counter=0
        
        cursor.execute("SELECT PostId from post_history")
        results = cursor.fetchall()
        for c in results:
                counter=0
                while(1):
                        c1=randrange(1,300000)                        
                        try:
                
                                #status=cursor.execute("update sonam_scared set id="+str(c[0])+" where id="+str(c1)+"")
                                print "update sonam_scared set id="+str(c[0])+" where id="+str(c1)+";"
                                counter=counter+1
                                if counter==10:
                                        break
                        except Exception,e:
                                counter2=counter2+1
                                if(counter2==10):
                                        counter2=0
test1()
