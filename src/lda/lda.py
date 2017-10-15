# coding=utf-8
import sys
import random
import cPickle
from gensim import corpora, models

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":
    corpus = cPickle.load(open('/home/zhang/Documents/data_file_2017/data_for_lda.p', "rb"))
    lda = models.ldamodel.LdaModel(corpus, num_topics=100, alpha='symmetric', eval_every=5, iterations=10,
                                   gamma_threshold=0.001, minimum_probability=0.01, random_state=1)

    lda.save('/home/zhang/Documents/data_file_2017/lda.model')

    # doc_topic = []
    # for index in range(len(corpus)):
    #     max_p = 0.
    #     topic = ''
    #     for ti in lda[corpus[index]]:
    #         if ti[1] > max_p:
    #             topic = ti[0]
    #             max_p = ti[1]
    #     doc_topic.append(topic)
    #
    # for i in range(30):
    #     print str(i + 1) + ":" + str(doc_topic[i]) + "->" + str(doc_topic[i + 30])
