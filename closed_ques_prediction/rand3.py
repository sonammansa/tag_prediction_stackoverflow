from sklearn.ensemble import RandomForestClassifier
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

# execute SQL query using execute() method.
cursor.execute("SELECT score,title,body,closed,userid from posts limit 1000")
results = cursor.fetchall()

corpus=[]
for line in results:
    corpus.append((line[1]+' '+line[2]).lower())

#for ll in corpus:
#    print ll
vectorizer = TfidfVectorizer(min_df=1,stop_words=['for', 'a', 'of', 'the', 'and', 'to', 'in', 'i', 'my', 'there', 'with', 'without', 'can', 'cant', 'cannot', 's'])
v=vectorizer.fit_transform(corpus)
v = scipy.sparse.coo_matrix(v)
#print vectorizer.transform(['computer'])

#print results

a=0
train=[]
for x in results:
    t=[]
    cursor.execute("SELECT reputation,create_date from user where id="+(str)(x[4]))
    res = cursor.fetchall()
    for r in res:
        t.append(r[0])  #reputation
    t1=0
    d=0
    for i,j,k in zip(v.row, v.col, v.data):
        if i==a:
            t1=t1+(j*k)
            d=d+1
    if d>0:
        t1=t1/d
    t.append(t1)  #post content
    a=a+1
    train.append(t)
    #print train
#train = [x[0:1] for x in results]
#print train

target = [x[3] for x in results]

rf = RandomForestClassifier(n_estimators=10)
rf = rf.fit(train, target)

cursor.execute("update posts_test set r_closed3=0")
db.commit()

cursor.execute("SELECT id,score,title,body,closed,userid from posts_test limit 1000")
results1 = cursor.fetchall()
#test = [x[0:1] for x in results1]

for line1 in results1:
    #l= rf.predict(line1[1:2])
    m=0
    t=[]
    cursor.execute("SELECT reputation,create_date from user where id="+(str)(line1[5]))
    res = cursor.fetchall()
    for r in res:
        m=m+1
        t.append(r[0])  #reputation
    if m==0:
        t.append(m)
    v1=vectorizer.transform((line1[2]+' '+line1[3]).lower())
    v1 = scipy.sparse.coo_matrix(v1)
    t1=0
    d=0
    for i,j,k in zip(v1.row, v1.col, v1.data):
        t1=t1+(j*k)
        d=d+1
    if d>0:
        t1=t1/d
    t.append(t1)          #post content
    l= rf.predict(t)
    if l[0]==1:
        cursor.execute("update posts_test set r_closed3=1 where id="+(str)(line1[0]))
        db.commit()


#importance of features---
importances = rf.feature_importances_
std = np.std([tree.feature_importances_ for tree in rf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

cursor.execute("SELECT count(*) from posts_test where closed=r_closed3")
(result,) = cursor.fetchone()
ac=Decimal(Decimal(result)/Decimal(1000))
print ("accuracy: %f" % ac)
cursor.execute("update c_accuracy set accuracy="+(str)(ac)+" where sno=3")
db.commit()

# Print the feature ranking
print("Feature ranking:")

for f in range(2):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

import pylab as pl
pl.figure()
pl.title("Feature importances in RandomForest")
pl.bar(range(2), importances[indices],
       color="r", yerr=std[indices], align="center")
pl.xticks(range(2), indices)
pl.xlim([-1, 10])
pl.show()

#-------------------------------------

#X = [[1,1,1], [2,2,2],[3,3,3]]
#Y = [4,5,6]
#clf = RandomForestClassifier(n_estimators=10)
#clf = clf.fit(X, Y)
#a=[[2,3,1],[3,4,5]]
#print clf.predict(a)
