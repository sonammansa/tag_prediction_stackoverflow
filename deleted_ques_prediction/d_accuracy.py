import MySQLdb
import pylab as pl
from pylab import *

# Open database connection
db = MySQLdb.connect("localhost","root","","major" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT accuracy,description from c_accuracy limit 3")
result = cursor.fetchall()

y=list()
d=list()
for line in result:
    y.append(line[0])
    d.append(line[1])


pl.figure()
pl.plot(range(len(y)),y)
pl.xticks(range(len(y)),d)
pl.show()

cursor.execute("SELECT accuracy from c_accuracy where sno>3")
result1 = cursor.fetchall()
x=(10,15,20,25,30)
z=list()
for line1 in result1:
    z.append(line1[0])
plot(x,z)
ylabel('accuracy')
xlabel('estimators')
title('accuracy comparison with 3 features and different no of estimators')
show()
