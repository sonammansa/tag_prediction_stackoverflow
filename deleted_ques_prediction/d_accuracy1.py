import MySQLdb
import pylab as pl
from pylab import *

# Open database connection
db = MySQLdb.connect("localhost","root","","major" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT accuracy,description from c_accuracy1")
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
#plot(x,y)
#ylabel('accuracy')
#xlabel('predictions')
#title('accuracy comparison with different no of features')
#show()
