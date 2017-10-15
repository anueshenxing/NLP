# coding=utf-8

import sys
import cPickle
import time
from gensim import corpora, models

reload(sys)
sys.setdefaultencoding("utf-8")
predir = '/home/zhang/Documents/data_file_2017/'


def load_cPickle(file_name):
    data = cPickle.load(open(predir + file_name, "rb"))
    return data


def save_data_by_cPickle(data, file_name):
    cPickle.dump(data, open(predir + file_name, "wb"), True)


def encode_utf8(str):
    return str.encode('utf-8')


def generate_data_for_lda():
    word_and_id_getter = WordAndIDTranslater('wordtoix_and_ixtoword_true.p')
    statitics_word = load_cPickle('statitics_word.p')
    all_news_keywords = load_cPickle('all_news_keywords.p')
    lda_input = []
    count = 0
    for news_keywords in all_news_keywords:
        if count % 100 == 0:
            print count
        count += 1
        news = []
        for word in news_keywords:
            wordID = word_and_id_getter.get_wordID(word)
            if not isinstance(wordID, int):
                continue
            news.append((wordID, statitics_word[wordID]))
        lda_input.append(news)
    save_data_by_cPickle(lda_input, 'data_for_lda.p')


class WordAndIDTranslater(object):
    def __init__(self, file_name):
        wordtoix_and_ixtoword = load_cPickle(file_name)
        self.get_wordID_by_word = wordtoix_and_ixtoword[0]
        self.get_word_by_wordID = wordtoix_and_ixtoword[1]

    def get_wordID(self, word):
        return self.get_wordID_by_word[encode_utf8(word)]

    def get_word(self, wordID):
        return self.get_word_by_wordID[wordID]


if __name__ == "__main__":
    generate_data_for_lda()
    time.sleep(5)
    corpus = cPickle.load(open(predir + 'data_for_lda.p', "rb"))
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
