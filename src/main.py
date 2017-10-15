# encoding=utf-8

from util import WordAndIDTranslater

import util
import global_params
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == '__main__':
    # word_and_id_getter = WordAndIDTranslater('wordtoix_and_ixtoword_true.p')
    # statitics_word = util.load_cPickle('statitics_word.p')
    # data_for_lda = util.load_cPickle('data_for_lda.p')
    # print statitics_word
    # # print len(data_for_lda)
    # # print data_for_lda
    # for key in statitics_word.keys():
    #     if not isinstance(key, int):
    #         print 'key: %s, value: %s' % (key, statitics_word[key])
    # # print statitics_word[0.0]
    # # print word_and_id_getter.get_word(0.0)

    for file_name in os.listdir(global_params.ORIGIN_NEWS_DATA_DIR):
        print file_name[-4:] == 'json'
