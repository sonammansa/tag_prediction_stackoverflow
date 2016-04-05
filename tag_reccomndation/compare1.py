from pylab import *
import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","","major" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute("select accuracy from recommended")
results=cursor.fetchall()

cursor.execute("select accuracy from f_recommended")
results1=cursor.fetchall()

x=arange(0,999,1)
y=list()
z=list()
for line in results:
    y.append(line[0])

for line1 in results1:
    z.append(line1[0])

plot(x,y)
plot(x,z)
legend(['without feedback','with feedback'],loc='upper left')
ylabel('accuracy')
xlabel('question')
title('accuracy comparison with and without feedback')
show()
