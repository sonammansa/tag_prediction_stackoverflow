import xml.sax
import MySQLdb
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

i=1
 
class ABContentHandler(xml.sax.ContentHandler):
  def __init__(self):
    xml.sax.ContentHandler.__init__(self)
 
  def startElement(self, name, attrs):
   # print("startElement '" + name + "'")
   global i
   if i<2000:
    Body = ""
    Title = ""
    tags = ""
    cl = ""
    uid=""
    if name == "row":
      pid=(int)(attrs.getValue("PostTypeId"))
      if pid==1:
      #dd=(int)(attrs.getValue("Id"));                     #####
      #if dd>2046:                                         #####
        #print dd;                                         #####
        try:
          Body=(str)(attrs.getValue("Body"))
          Body = Body.replace("\n"," ")
          Body = Body.replace("'"," ")
          Body = Body.replace("\""," ")
          Body = Body.replace(",", " ")
          Body = Body.replace("(", " ")
          Body = Body.replace(")", " ")
          Body = Body.replace("\\", " ")
          Body = strip_tags(Body)
        except Exception, e:
          Body=""
        try:
          Title=(str)(attrs.getValue("Title"))
          Title = Title.replace("\r"," ")
          Title = Title.replace("\n"," ")
          Title = Title.replace("'"," ")
          Title = Title.replace("\""," ")
          Title = Title.replace(",", " ")
          Title = Title.replace("("," ")
          Title = Title.replace(")", " ")
          Title = Title.replace("\\", " ")
          Title = Title.replace("?", " ")
          Title = strip_tags(Title)
        except Exception, e:
          Title=""
        try:
          tags=(str)(attrs.getValue("Tags"))
          tags = tags.replace("<","")
          tags = tags.replace(">",",")
        except Exception, e:
          tags=""
        try:
          cl=attrs.getValue("ClosedDate")
          cl="1"
        except Exception, e:
          cl="0"
        try:
          uid=attrs.getValue("OwnerUserId")
        except Exception, e:
          uid="-1"
        insert_str = "insert into `posts` values("+(attrs.getValue("Id"))+","+(attrs.getValue("PostTypeId"))+","+\
             (attrs.getValue("Score"))+",'"+Body+"','"+Title+"','"+tags+"',"+cl+","+uid+")"
        insert_cursor.execute(insert_str)
        #db1.commit()
        i=i+1
      #print( attrs.getValue("Id") + "," + attrs.getValue("PostTypeId") + "," + attrs.getValue("Score") + "," + attrs.getValue("Body") + "," +\
      #       attrs.getValue("Title") + "," + attrs.getValue("Tags"))
    db1.commit() 
  
 
db1= MySQLdb.connect(host="localhost", user="root", passwd="",db="major",port=3306)
insert_cursor = db1.cursor()   
 
def main(sourceFileName):
  source = open(sourceFileName)
  xml.sax.parse(source, ABContentHandler())
 
if __name__ == "__main__":
  main("D:\\major\\dataset\\stackoverflow.com\\posts.xml")
