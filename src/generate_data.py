# encoding=utf-8
import os

import global_params
import json
import util
from util import WordAndIDTranslater
from util import StopWords
from log_util import LogUtil
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

STOPWORD_FILE_NAME = 'stopwords.p'
NLP_LOG_NAME = 'NLP_info.log'
WORD_FLAG_DICT_NAME = 'word_flag_dict.p'
ALL_NEWS_CTG_TITLE_CONTENT_FILE_NAME = 'all_news_ctg_title_data.p'


def load_file(file_name):
    data_file = open(file_name, 'r')
    data = []
    for line in data_file.readlines():
        data.append(line.split('\n')[0].encode('utf-8'))
    data_file.close()
    return data


def generate_stopwords(file_name):
    data = load_file(global_params.STOPWORDS_FILE_DIR)
    print data
    util.save_data_by_cPickle(data, file_name)


def generate_news_data_by_jieba(origin_news_file_dir):
    """
        word_flag_dict:{word:flag, ...}
        news_ctg_title_data:[[ctg,[title words],[content words]], ...]
    """
    stopWords = StopWords(STOPWORD_FILE_NAME)
    log = LogUtil(NLP_LOG_NAME)

    all_news_ctg_title_data = []
    word_flag_dict = {}

    for file_name in os.listdir(origin_news_file_dir):
        if file_name[-4:] != 'json':
            continue

        log.log_info('now process origin news file is : %s' % file_name)
        origin_news_data = load_file(origin_news_file_dir + file_name)
        count = 0

        for news in origin_news_data:
            if count % 100 == 0:
                log.log_info('now process origin news file is : %s, now processed news number is %s'
                             % (file_name, count))
            count += 1

            news_ctg_title_data = []
            news_json = json.loads(news, 'utf-8')
            ctg = news_json['category'].split('_')[2]
            title = news_json['title']
            content = news_json.get('content', '')

            title_words = util.split_sentence_to_word(title)
            title_words_filter_stopwords = []
            title_word_list = []
            for item in title_words:
                if not stopWords.is_stopword(item[0]):
                    title_words_filter_stopwords.append(item)
                    word_flag_dict[item[0]] = item[1]
                    title_word_list.append(item[0])

            content_words = util.split_sentence_to_word(content)
            content_words_filter_stopwords = []
            content_word_list = []
            for item in content_words:
                if not stopWords.is_stopword(item[0]):
                    content_words_filter_stopwords.append(item)
                    word_flag_dict[item[0]] = item[1]
                    content_word_list.append(item[0])

            news_ctg_title_data.append(ctg)
            news_ctg_title_data.append(title_word_list)
            news_ctg_title_data.append(content_word_list)
            all_news_ctg_title_data.append(news_ctg_title_data)

    log.log_info('start to save word_flag_dict')
    util.save_data_by_cPickle(word_flag_dict, WORD_FLAG_DICT_NAME)
    log.log_info('save word_flag_dict success')

    log.log_info('start to save all_news_ctg_title_data')
    util.save_data_by_cPickle(word_flag_dict, ALL_NEWS_CTG_TITLE_CONTENT_FILE_NAME)
    log.log_info('save all_news_ctg_title_data success')


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
    count = 0
    statitics_word = {}
    for news_keywords in data:
        if count % 100 == 0:
            print count
        count += 1
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
    util.save_data_by_cPickle(lda_input, 'data_for_lda.p')





if __name__ == "__main__":
    generate_news_data_by_jieba(global_params.ORIGIN_NEWS_DATA_DIR)
