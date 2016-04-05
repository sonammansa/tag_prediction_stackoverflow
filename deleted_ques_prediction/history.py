print("done")
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
    if a<2000:
     #uid=""
       if name == "row":
        #uid=(int)(attrs.getValue("Id"))
        phid=(int)(attrs.getValue("PostHistoryTypeId"))
        # if uid>0 &
        if phid==12 :
          dt = attrs.getValue("CreationDate")
          dt = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S.%f')
          insert_str = "insert into `post_history` values("+(attrs.getValue("Id"))+","+(attrs.getValue("PostHistoryTypeId"))+",'"+dt+"',"+(attrs.getValue("PostId"))+")"
          print 'hi'
          insert_cursor.execute(insert_str)
          a=a+1
          db1.commit()
          print "commit"
 
db1= MySQLdb.connect(host="localhost", user="root", passwd="",db="major",port=3306)
insert_cursor = db1.cursor()

d=datetime.now()
d=d.strftime('%Y-%m-%d %H:%M:%S')
insert_str = "insert into `post_history` values(%s,%s,%s, %s)"
insert_cursor.execute(insert_str,(-1,0,d,-1))
 
def main(sourceFileName):
  source = open(sourceFileName)
  xml.sax.parse(source, ABContentHandler())
 
if __name__ == "__main__":
  main("D:\\major\\dataset\\stackoverflow.com\\PostHistory.xml")
