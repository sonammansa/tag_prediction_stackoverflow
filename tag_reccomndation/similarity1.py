import MySQLdb
from gensim import corpora, models, similarities
import redis, redisbayes
from decimal import *

#def most_common(lst):
#    if(len(lst)==len(set(lst))):
#         return lst[0]
#    else:
#         return max(set(lst), key=lst.count)

# Open database connection
db = MySQLdb.connect("localhost","root","","major" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT title,body from posts limit 999")
results = cursor.fetchall()
text = ""
class MyCorpus(object):
     def __iter__(self):
        for line in results:
             text=line[0]+' '+line[1]
             # assume there's one document per line, tokens separated by whitespace
             yield dictionary.doc2bow(text.lower().split())
             
#for line in results:
     #text=line[0]+line[1]
     #dictionary = corpora.Dictionary(line[0].lower().split())

dictionary = corpora.Dictionary((line[0]+' '+line[1]).lower().split() for line in results)

# remove stop words and words that appear only once
stoplist = set('for a of the and to in i my there with without can cant cannot'.split())
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
            if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
dictionary.compactify() # remove gaps in id sequence after words that were removed

#print sorted(dictionary.values())

corpus_memory_friendly = MyCorpus() # doesn't load the corpus into memory!
ln=len(dictionary.keys())
#print corpus_memory_friendly
tfidf = models.TfidfModel(corpus_memory_friendly)
#for vector in corpus_memory_friendly: # load one vector into memory at a time
     #print tfidf[vector]
index = similarities.Similarity('',tfidf[corpus_memory_friendly],num_features=ln,num_best=10)
#-----------------------------------------------------------------
redis=redis.Redis()
#-----------------------------------------------------------------
cursor.execute("SELECT title,body,id,tags from posts_test")
results1 = cursor.fetchall()
doc=""
for line1 in results1:
    doc=line1[0]+' '+line1[1]
    vec_bow = dictionary.doc2bow(doc.lower().split())
    #print vec_bow
    vec_tfidf = tfidf[vec_bow]
    #print vec_tfidf
    sims = index[vec_tfidf]
    l=list(enumerate(sims))
    #print l
    i=0
    tl=list()
#------------------------------------------------------------------------------
    redis.flushall()
    rb = redisbayes.RedisBayes(redis)
#------------------------------------------------------------------------------
    #print doc
    did=line1[2]
    for entry in l:
         d=(str)(l[i][1][0])
         cursor.execute("SELECT id,tags,body,title from posts limit "+d+",1")
         results2 = cursor.fetchall()
         for line2 in results2:
                  #print (str)(line[0])+" "+line[1]
                  t=line2[1].lower().split(',')
                  t.pop()
                  tl.extend(t)
                  for tg in t:
                      rb.train(tg,line2[2]+line2[3])
         i=i+1
#tl=set(tl)
    tags=list()
    a_tags=list()
#print rb.classify(doc)
    tgss = rb.score(doc)
    tgss = sorted(tgss.items(), key=lambda x: x[1], reverse=True)
    if len(tgss)>=10:
         for i in range(0,10):
             t=tgss[i][0]
             tags.append(t)
    else:
         for i in range(0,len(tgss)):
            t=tgss[i][0]
            tags.append(t) 
          
    a_tags=line1[3].lower().split(',')
    t = [x for x in tags if x in a_tags]
    tp=len(t)
    fp=len(tags)-tp
    fn=len(a_tags)-1-tp
    #cursor.execute("SELECT count(tag) from tags")
    #(total,)=cursor.fetchone()
    total = 981     #for 1000 posts only
    tn=total-len(tags)-fn
    #print tp
    #print fp
    #print fn
    #print tn
    accuracy=Decimal(Decimal(tp+tn)/Decimal(tp+fp+fn+tn))
    #print accuracy
    tags = ", ".join(tags)
      
    #print did
    #print tags
    qry='INSERT INTO recommended VALUES (%s,%s,%s)'
    cursor.execute(qry,(did, tags,accuracy))
    db.commit()

 
#tags=list()
#for j in range (0,5):
     #com=most_common(tl)
     #tags.append(com)
     #tl = [x for x in tl if x != com]
     #print tl

#print tags
#corpora.MmCorpus.serialize('corpus_memory_friendly.mm', corpus)
# disconnect from server
db.close()
