# tag_prediction_stackoverflow
Introduction :
Stack Overflow is one of the very popular online media for the programmers to share their knowledge and experience. Developers seek for help from Stack Overflow type online communities. The objective of our research work is to ease the tagging process of questions on StackOverflow. This work proposes TagStack system a machine learning and feedback based framework for predicting tags on StackOverflow. We perform experiment on real world and publically available dataset, and results shows that TagStack system is effective in predicting tags on StackOverflow.
___________________________________________________________________________________________

installations:
-------------------------------------
install enthought canopy(for gensim, numpy, scipy)
install mysqldb in it ( 'easy_install mysql-python')
install redis client using 'easy_install redis' and redisbayes library using 'easy_install redisbayes' in canopy command prompt

install redis server using setup

run redis-server from program files/redis (wherever redis server is installed) - for naive bayes to work

install scikit by writing 'easy_install -U scikit-learn' in canopy command prompt - used for closed question recommendations

install numpy 
c:/go/to/path/numpy/python setup.py install

install gensim 
c:/go/to/path/gensim/python setup.py install

____________________________________________________________________________________________________________________________________

data extraction
--------------------------------
major1.py - extraction of training data - posts table (2000 rows)
major2.py - extraction of testing data - posts_test table (1000 rows)
user.py - extraction of user data for closed question prediction - user table
tagss.php - extract unique tags from posts table and insert them into tags table - used to count total tags in accuracy calculation
 
____________________________________________________________________________________________________________________________________
tag recommendation
-------------------------------------------------
similarity.py- calculate 10 best similar docs based on tfidf and recommend tags using naive bayes on those 10 docs and also store the accuracy of each doc- stores in recommended

copy data from posts to f_posts and tags to f_tags before running f_similarity.py
(insert into f_posts(select * from posts limit 999)) and run tagss.php again by changing posts to f_posts and tags to f_tags

f_similarity.py- same as above with feedback after every 50 recommendations(i.e. training data set is updated - f_posts and f_tags) - stores in f_recommended

compare.py - compares the accuracy with and without feedback and plots a graph


______________________________________________________________________________________________________________________________
closed question recommendation
--------------------------------------------------
rand1.py - predicts that question will be closed or not using random forest classifier using 10 estimators and 5 features : score of question, reputation of user, age of user account, total score of other questions posted by same user, question title+body((word_number*its tfidf)/no of unique words in that question). It also tells the importance of each of these 5 features and plots a graph(i.e which feature is contributing more towards the prediction) - stores prediction in r_closed1 column of posts_test. It finally checks how many questions are correctly predicted as closed or not closed and inserts into c_accuracy table

rand2.py - takes 3 best features only (score of question, reputation of user, question title+body((word_number*its tfidf)/no of unique words in that question)) - stores in r_closed2 column

rand3.py - takes 2 best features only (reputation of user, question title+body((word_number*its tfidf)/no of unique words in that question)) - stores in r_closed3 column

run rand2.py by changing no of estimators to 10, 15, 20, 25, 30 and sno for table insertion accordingly where comment is written - den compare accuracy using c_accuracy.py

c_accuracy.py - plots the graph for accuracy comparison of diff predictions from c_accuracy table

rand4.py - executes rand2.py (since it was best) for different ratios of training and testing dataset and store accuracy in c_accuracy1 table
		(change limit at 2 places according to ratio ,and id and sno at place where comment is there, and divide by where accuracy is written)

c_accuracy1.py - plots the graph for accuracy comparison of predictions with diff ratios of training and testing data from c_accuracy1 table

similar for dec1.py, dec2.py, dec3.py, dec4.py & ada1.py,ada2.py,ada3.py,ada4.py

____________________________________________________________________________________________________________________________

deleted question recommendation
--------------------------------------------------
rand1.py - predicts that question will be deleted or not using random forest classifier using 10 estimators and 5 features : score of question, reputation of user, age of user account, total score of other questions posted by same user, question title+body((word_number*its tfidf)/no of unique words in that question). It also tells the importance of each of these 5 features and plots a graph(i.e which feature is contributing more towards the prediction) - stores prediction in r_deleted1 column of posts_test. It finally checks how many questions are correctly predicted as deleted or not deleted and inserts into c_accuracy table

rand2.py - takes 3 best features only (score of question, reputation of user, question title+body((word_number*its tfidf)/no of unique words in that question)) - stores in r_deleted2 column

rand3.py - takes 2 best features only (reputation of user, question title+body((word_number*its tfidf)/no of unique words in that question)) - stores in r_deleted3 column

run rand2.py by changing no of estimators to 10, 15, 20, 25, 30 and sno for table insertion accordingly where comment is written - den compare accuracy using c_accuracy.py

c_accuracy.py - plots the graph for accuracy comparison of diff predictions from c_accuracy table

rand4.py - executes rand2.py (since it was best) for different ratios of training and testing dataset and store accuracy in c_accuracy1 table
		(change limit at 2 places according to ratio ,and id and sno at place where comment is there, and divide by where accuracy is written)

c_accuracy1.py - plots the graph for accuracy comparison of predictions with diff ratios of training and testing data from c_accuracy1 table

similar for dec1.py, dec2.py, dec3.py, dec4.py & ada1.py,ada2.py,ada3.py,ada4.py

____________________________________________________________________________________________________________________________

Databases:
c_accuracy- Accuracies for closed questions corresponding all three classifiers(w.r.t features and estimators count)
c_accuracy1- Accuracies for closed questions corresponding all three classifiers(w.r.t testing and training set count)
del_posts- all deleted posts are extracted
d_accuracy- Accuracies for deleted questions corresponding all three classifiers(w.r.t features and estimators count)
d_accuracy1- Accuracies for deleted questions corresponding all three classifiers(w.r.t testing and training set count)
d_test- testing set for deleted questions
d_train- traning set for deleted questions
f_posts- posts after getting feedback
f_reccomendation- reccomendation table after getting updates
f_tags- collecting tags after 50 reccomendations
posts- traning set for closed and tags reccomendation
posts_test- testing set for closed and tags reccomendation
posts_history- all the posts are extracted having postid=12 for deleted question collection
reccomended- reccomended tags collection
tags- tags corresponding to their ids
tag_dictionary- bag of words for finding best tag for reccomending user
user- corresponding to each user id there is reputation score(for considering one more feature)
x1,x2,x3,x4,x5- Tags extracted with different number of count corresponding to each post.