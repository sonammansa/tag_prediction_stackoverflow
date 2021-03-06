from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import AdaBoostClassifier
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
cursor.execute("SELECT score,title,body,closed,userid from d_train limit 1000")
results = cursor.fetchall()

corpus=[]
for line in results:
    corpus.append((line[1]+' '+line[2]).lower())

#for ll in corpus:
vectorizer = TfidfVectorizer(min_df=1,stop_words=['for', 'a', 'of', 'the', 'and', 'to', 'in', 'i', 'my', 'there', 'with', 'without', 'can', 'cant', 'cannot', 's'])
v=vectorizer.fit_transform(corpus)
v = scipy.sparse.coo_matrix(v)

#print results

a=0
train=[]
for x in results:
    scr=0
    t=[]
    t.append(x[0])  #score of post
    cursor.execute("SELECT reputation,create_date from user where id="+(str)(x[4]))
    res = cursor.fetchall()
    for r in res:
        t.append(r[0])  #reputation
        today = datetime.now()
        dt = r[1]
        age = (today-dt)
        t.append(age.days)  #age of user account
    cursor.execute("SELECT score from d_train where userid="+(str)(x[4]))
    res1 = cursor.fetchall()
    for r1 in res1:
        scr=scr+r1[0]
    t.append(scr)  #score of other d_train of the user
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

target = [x[3] for x in results]

rf = AdaBoostClassifier(n_estimators=100)
rf = rf.fit(train, target)

cursor.execute("update d_test set a_closed1=0")
db.commit()

cursor.execute("SELECT id,score,title,body,closed,userid from d_test limit 1000")
results1 = cursor.fetchall()
#test = [x[0:1] for x in results1]

for line1 in results1:
    t=[]
    m=0
    scr=0
    t.append(line1[1])   #score of post
    cursor.execute("SELECT reputation,create_date from user where id="+(str)(line1[5]))
    res = cursor.fetchall()
    for r in res:
        m=m+1
        t.append(r[0])  #reputation
        today = datetime.now()
        dt = r[1]
        age = (today-dt)
        t.append(age.days)  #age of user account
    if m==0:
        t.append(m)
        t.append(m)
    cursor.execute("SELECT score from d_train where userid="+(str)(line1[5]))
    res1 = cursor.fetchall()
    for r1 in res1:
        scr=scr+r1[0]
    t.append(scr)  #score of other d_train of the user
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
        cursor.execute("update d_test set a_closed1=1 where id="+(str)(line1[0]))
        db.commit()

cursor.execute("SELECT count(*) from d_test where closed=a_closed1")
(result,) = cursor.fetchone()
ac=Decimal(Decimal(result)/Decimal(1000))
print ("accuracy: %f" % ac)
cursor.execute("update d_accuracy set a_accuracy="+(str)(ac)+" where sno=1")
db.commit()

#importance of features---
importances = rf.feature_importances_
std = np.std([tree.feature_importances_ for tree in rf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(5):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

import pylab as pl
pl.figure()
pl.title("Feature importances in AdaBoost")
pl.bar(range(5), importances[indices],
       color="y", yerr=std[indices], align="center")
pl.xticks(range(5), indices)
pl.xlim([-1, 10])
pl.show()

#-------------------------------------

#X = [[1,1,1], [2,2,2],[3,3,3]]
#Y = [4,5,6]
#clf = AdaBoostClassifier(n_estimators=100)
#clf = clf.fit(X, Y)
#a=[[2,3,1],[3,4,5]]
#print clf.predict(a)
