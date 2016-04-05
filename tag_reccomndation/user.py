import xml.sax
import MySQLdb
from datetime import datetime

a=0
class ABContentHandler(xml.sax.ContentHandler):
  def __init__(self):
    xml.sax.ContentHandler.__init__(self)
 
  def startElement(self, name, attrs):
   # print("startElement '" + name + "'")
    global a 
    uid=""
    if name == "row":
        uid=(int)(attrs.getValue("Id"))
        if uid>0:
          dt = attrs.getValue("CreationDate")
          dt = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S.%f')
          insert_str = "insert into `user` values("+(attrs.getValue("Id"))+","+(attrs.getValue("Reputation"))+",'"+dt+"')"
          insert_cursor.execute(insert_str)
          a=a+1
          if a%100000==0:
            db1.commit()
            print "commit"
      #print( attrs.getValue("Id") + "," + attrs.getValue("PostTypeId") + "," + attrs.getValue("Score") + "," + attrs.getValue("Body") + "," +\
      #       attrs.getValue("Title") + "," + attrs.getValue("Tags"))
 
  
 
db1= MySQLdb.connect(host="localhost", user="root", passwd="",db="major",port=3306)
insert_cursor = db1.cursor()

d=datetime.now()
d=d.strftime('%Y-%m-%d %H:%M:%S')
insert_str = "insert into `user` values(%s,%s,%s)"
insert_cursor.execute(insert_str,(-1,0,d))
 
def main(sourceFileName):
  source = open(sourceFileName)
  xml.sax.parse(source, ABContentHandler())
 
if __name__ == "__main__":
  main("D:\\major\\dataset\\stackoverflow.com\\users.xml")
