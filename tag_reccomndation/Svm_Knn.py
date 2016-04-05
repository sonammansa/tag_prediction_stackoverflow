import MySQLdb
from gensim import corpora, models, similarities
import redis, redisbayes
from decimal import *
from sklearn import svm
from sklearn import neighbors

# Open database connection
db = MySQLdb.connect("localhost","root","","major")
input_words = {}
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
input_words = {}
counter = 0
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
    words=list()
    a_words=list()
#print rb.classify(doc)
    wrdss = rb.score(doc)
    wrdss = sorted(wrdss.items(), key=lambda x: x[1], reverse=True)
    if len(wrdss)>=5:
         for i in range(0,5):
             t=wrdss[i][0]
             words.append(t)
             #print type(input_words)
             if t not in input_words:
                input_words[t] = counter
                counter = counter +1
    else:
         for i in range(0,len(wrdss)):
            t=wrdss[i][0]
            words.append(t)
            if t not in input_words:
                input_words[t] = counter
                counter = counter +1 
      
    print len(input_words)
    #print "output of classifiers"
#### Testing the input set with output set

input_set = []
output_set = []

sql = "select sno,tag from tags order by sno asc limit 200"
cursor.execute(sql)
word_map = {}
word_numbers = {}
result = cursor.fetchall()
for row in result:
    word_map[row[1]] = row[0]
    word_numbers[row[0]] = row[1]


for line1 in results1:
    temp = []
    for i in range(0,len(input_words)):
        temp.append(0);
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
    words=list()
    a_words=list()
#print rb.classify(doc)
    wrdss = rb.score(doc)
    wrdss = sorted(wrdss.items(), key=lambda x: x[1], reverse=True)
    if len(wrdss)>=5:
         for i in range(0,5):
             t=wrdss[i][0]
             words.append(t)
             temp[input_words[t]] += 1
    else:
         for i in range(0,len(wrdss)):
            t=wrdss[i][0]
            words.append(t)
            temp[input_words[t]] += 1
    
    a_words=line1[3].lower().split(',')
    for i in a_words:
        if i in word_map:
            input_set.append(temp)
            output_set.append(word_map[i])
            #break


#print len(input_set)
#print len(output_set)

clf = svm.SVC()
clf.fit(input_set,output_set)
out = clf.predict([input_set[0]])
print out
print word_numbers[out[0]]

knn = neighbors.KNeighborsClassifier()
knn.fit(input_set,output_set)
out = knn.predict([input_set[0]])
print out
print word_numbers[out[0]]
db.close()
