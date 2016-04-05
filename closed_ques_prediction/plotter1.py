import matplotlib.pyplot as plotter
import MySQLdb
import numpy as np
import scipy.sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
from decimal import *

# Open database connection
db = MySQLdb.connect("localhost","root","","major" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

def plotData(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6):
        x_max = max(max(x1),max(x2))+1
        y_max = max(max(y1),max(y2),max(y3),max(y4),max(y5),max(y6))+1
        x_min = min(min(x1),min(x2))-1
        y_min = min(min(y1),min(y2))-1
        f, (ax1, ax2,ax3) = plotter.subplots(1,3, sharey=True)
        ax1.plot(x1,y1,'ro')
        ax1.plot(x2,y2,'bo')
        ax1.axis([x_min,x_max,y_min,y_max])
        x_max = max(max(x3),max(x4))+1
        x_min = min(min(x3),min(x4))-1
        ax2.plot(x3,y3,'ro')
        ax2.plot(x4,y4,'bo')
        ax2.axis([x_min,x_max,y_min,y_max])
        x_max = max(max(x5),max(x6))+1
        x_min = min(min(x5),min(x6))-1
        ax3.plot(x5,y5,'ro')
        ax3.plot(x6,y6,'bo')
        ax3.axis([x_min,x_max,y_min,y_max])
        legend(location="lower right")
        xlabel("question number")
        ylabel("random")
        save
        plotter.show()




def plotData1(y1,y2,y3,r_count,a_count,d_count):
        f, (ax1, ax2,ax3) = plotter.subplots(3,1, sharey=True)
        x = range(0,999)
        ax1.plot(x,y1,'bo')
        ax1.axis([0,1000,-1,2])
        ax2.plot(x,y2,'bo',label=str(a_count))
        ax2.axis([0,1000,-1,2])
        ax3.plot(x,y3,'bo',label=str(d_count))
        ax3.axis([0,1000,-1,2])
        ax1.text(450,1.4,'count:' + str(r_count))
        ax2.text(450,1.4,'count:' + str(a_count))
        ax3.text(450,1.4,'count:' + str(d_count))
        ax1.set_title('random_forest')
        ax2.set_title('ada_boost')
        ax3.set_title('extra_trees')
        ax3.set_xlabel('count')
        ax2.set_ylabel('post number')
        plotter.show()


def plotData2(y1,y2,y3):
        x = [1000,1250,1500,1750,2000]
        plotter.plot(x,y1,'b',label='Random Forest')
        plotter.axis([950,2050,83,90])
        plotter.plot(x,y2,'y',label='Ada Boost')
        plotter.plot(x,y3,'r',label='Extra Trees')
        plotter.title('accuracy')
        plotter.legend(title='',loc='lower right')
        plotter.xlabel('Training Set')
        plotter.ylabel('Accuracy')
        plotter.show()


def plotData3(y1,y2,y3):
        x = [10,15,20,25,30]
        print len(y1)
        plotter.plot(x,y1,'b',label='Random Forest')
        plotter.axis([10,35,88.5,90.0])
        plotter.plot(x,y2,'y',label='Ada Boost')
        plotter.plot(x,y3,'r',label='Extra Trees')
        plotter.title('accuracy')
        plotter.legend(title='',loc='lower right')
        plotter.xlabel('Estimators')
        plotter.ylabel('Accuracy')
        plotter.show()



def test():
        x1=[1,2,3,4,5]
        y1=[1,2,3,4,5]
        x2=[4,5]
        y2=[6,7]
        x3 = [10,12,14,16,18]
        y3 = [12,14,15,16,17]
        x4=[4,5]
        y4=[6,7]
        x5=[1,2,3,4,5]
        y5=[1,2,3,4,5]
        x6=[4,5]
        y6=[6,7]
        plotData(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6)



def test1():
        cursor.execute("SELECT r_closed1,a_closed1,d_closed1 from posts_test limit 1000")
        results = cursor.fetchall()

        random_forest = []
        ada_boost = []
        d_algo = []
        r_count = 0
        a_count = 0
        d_count = 0
        for line in results:
            random_forest.append(line[0])
            r_count = r_count + line[0]
            ada_boost.append(line[1])
            a_count = a_count + line[1]
            d_algo.append(line[2])
            d_count = d_count + line[2]
        plotData1(random_forest,ada_boost,d_algo,r_count,a_count,d_count)




def test2():
        cursor.execute("SELECT accuracy,a_accuracy,d_accuracy from c_accuracy1 order by sno asc limit 5")
        results = cursor.fetchall()
        random_forest = []
        ada_boost = []
        d_algo = []     
        for line in results:
                random_forest.append(float(line[0])*100)
                ada_boost.append(float(line[1])*100)
                d_algo.append(float(line[2])*100)
        plotData2(random_forest,ada_boost,d_algo)



def test3():
        cursor.execute("SELECT accuracy,a_accuracy,d_accuracy from c_accuracy where sno>3")
        results = cursor.fetchall()
        random_forest = []
        ada_boost = []
        d_algo = []
        for line in results:
                random_forest.append(float(line[0])*100)
                #print int(line[0])*100
                ada_boost.append(float(line[1])*100)
                d_algo.append(float(line[2])*100)
        plotData3(random_forest,ada_boost,d_algo)



def train(x):
        return x,y
test1()
