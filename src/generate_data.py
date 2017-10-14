# encoding=utf-8

import util
from util import WordAndIDTranslater
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

pre_dir = "/home/zhang/Documents/data_file_2017/"


def load_file(file_name):
    data_file = open(pre_dir + file_name, 'r')
    data = []
    for line in data_file.readlines():
        data.append(line)
    data_file.close()
    return data


def get_all_news_keywords():
    ctg_title_keywords = "all_news_title_and_ctg_with_keywords.txt"
    ctg_title = "news_title_data_and_category.txt"

    data_ctg_title_keywords = load_file(ctg_title_keywords)
    data_ctg_title = load_file(ctg_title)

    is_illegal = True
    if len(data_ctg_title) == len(data_ctg_title_keywords):
        is_illegal = False
    all_news_keywords = []
    if not is_illegal:
        for index in range(len(data_ctg_title)):
            ctg_tltle = data_ctg_title[index]
            ctg_title_keywords = data_ctg_title_keywords[index]

            ctg_tltle_words = ctg_tltle.split(" ")
            ctg_title_keywords_words = ctg_title_keywords.split(" ")

            # if len(ctg_tltle_words) == 0:
            #     print "news_id %s : ctg_tltle_words'num is 0 " % index
            if len(ctg_title_keywords_words) != len(ctg_tltle_words):
                # print "news_id %s : news has no keywords " % index
                news_keywords = ctg_title_keywords_words[len(ctg_tltle_words):]
                all_news_keywords.append(news_keywords)
            else:
                all_news_keywords.append([])
    util.save_data_by_cPickle(all_news_keywords, "all_news_keywords.p")
    # cPickle.dump(all_news_keywords, open(pre_dir + "all_news_keywords.p", "wb"), True)
    return True


def statistics_word_appears(data):
    word_and_id_getter = WordAndIDTranslater('wordtoix_and_ixtoword_true.p')

    statitics_word = {}
    for news_keywords in data:
        print news_keywords
        for word in news_keywords:
            wordID = word_and_id_getter.get_wordID(word)
            if wordID not in statitics_word.keys():
                statitics_word[wordID] = 1
            else:
                statitics_word[wordID] += 1
    print statitics_word
    util.save_data_by_cPickle(statitics_word, 'statitics_word.p')


def generate_stastics_word_appears_data():
    all_news_keywords = util.load_cPickle('all_news_keywords.p')
    statistics_word_appears(all_news_keywords)


def generate_data_for_lda():
    word_and_id_getter = WordAndIDTranslater('wordtoix_and_ixtoword_true.p')
    statitics_word = util.load_cPickle('statitics_word.p')
    all_news_keywords = util.load_cPickle('all_news_keywords.p')
    lda_input = []

    for news_keywords in all_news_keywords:
        news = []
        for word in news_keywords:
            wordID = word_and_id_getter.get_wordID(word)
            news.append((wordID, statitics_word[wordID]))
        lda_input.append(news)
    util.save_data_by_cPickle(lda_input, 'data_for_lda.p')



if __name__ == "__main__":
    generate_data_for_lda()
