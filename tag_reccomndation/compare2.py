from pylab import *
import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","","major" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute("select accuracy from x1")
results=cursor.fetchall()

cursor.execute("select accuracy from x2")
results1=cursor.fetchall()

cursor.execute("select accuracy from x3")
results2=cursor.fetchall()

cursor.execute("select accuracy from x4")
results3=cursor.fetchall()

cursor.execute("select accuracy from x5")
results4=cursor.fetchall()

x=arange(0,509,1)
y=list()
z=list()
p=list()
q=list()
r=list()

for line in results:
    y.append(line[0])

for line1 in results1:
    z.append(line1[0])

for line2 in results2:
    p.append(line2[0])

for line3 in results3:
    q.append(line3[0])

for line4 in results4:
    r.append(line4[0])

plot(x,y, 'g^') #top 1 tag
plot(x,z, 'ro') #top 2 tags
plot(x,p, 'bs') #top 3 tags
plot(x,q, 'yo') #top 4 tags
plot(x,r,'c*') #top 5 tags
legend(['top 1 tag','top 2 tags','top 3 tags','top 4 tags','top 5 tags'],loc='upper right')
ylabel('accuracy')
xlabel('question')
title('Accuracies for different number of tags for each post')
show()
