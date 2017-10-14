# encoding=utf-8

from gensim import corpora
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
documents = ["Human machine interface for lab abc computer applications",
    "A survey of user opinion of computer system response time",
    "The EPS user interface management system",
    "System and human system engineering testing of EPS",
    "Relation of user perceived response time to error measurement",
    "The generation of random binary unordered trees",
    "The intersection graph of paths in trees",
    "Graph minors IV Widths of trees and well quasi ordering",
    "Graph minors A survey"]
"""
#use StemmedCountVectorizer to get stemmed without stop words corpus
Vectorizer = StemmedCountVectorizer
# Vectorizer = CountVectorizer
vectorizer = Vectorizer(stop_words='english')
vectorizer.fit_transform(documents)
texts = vectorizer.get_feature_names()
# print(texts)
"""
texts = [doc.lower().split() for doc in documents]
# print(texts)
dict = corpora.Dictionary(texts)
# print dict, dict.token2id
corpus = [dict.doc2bow(text) for text in texts]
print(corpus)

print u'自建词典'.encode('utf-8')

