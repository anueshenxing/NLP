# encoding=utf-8

import cPickle
import global_params
import jieba.posseg as pseg
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def load_cPickle(file_name):
    data = cPickle.load(open(global_params.GENERATE_DATA_DIR + file_name, "rb"))
    return data


def save_data_by_cPickle(data, file_name):
    cPickle.dump(data, open(global_params.GENERATE_DATA_DIR + file_name, "wb"), True)


def encode_utf8(str):
    return str.encode('utf-8')


def split_sentence_to_word(sentence):
    """
    :param sentence:
    :return: [(word,flag),...]
    """
    result = []
    if sentence is None or sentence == '':
        return result
    sent = ' '.join(sentence.split('\n'))
    word_flag_dict = pseg.cut(sent)
    for item in word_flag_dict:
        word = (item.word, item.flag)
        result.append(word)
    return result


def get_word2vec_dict(file_name):
    word_vec_dict = load_cPickle(file_name)
    return word_vec_dict


class WordVec(object):
    def __init__(self, word2vec_dict_filename):
        word_vec_dict = get_word2vec_dict(word2vec_dict_filename)
        self.word2vec_dict = np.array(word_vec_dict[0])

    def get_word_vec(self, word__i_d):
        return self.word2vec_dict[word__i_d]


class WordAndIDTranslater(object):
    def __init__(self, file_name):
        wordtoix_and_ixtoword = load_cPickle(file_name)
        self.get_wordID_by_word = wordtoix_and_ixtoword[0]
        self.get_word_by_wordID = wordtoix_and_ixtoword[1]

    def get_wordID(self, word):
        return self.get_wordID_by_word[encode_utf8(word)]

    def get_word(self, wordID):
        return self.get_word_by_wordID[wordID]


class StopWords(object):
    def __init__(self, filename):
        self.stopwords = load_cPickle(filename)

    def is_stopword(self, word):
        is_a_stopword = False
        if word in self.stopwords:
            is_a_stopword = True
        return is_a_stopword


if __name__ == "__main__":
    word_and_id_getter = WordAndIDTranslater('wordtoix_and_ixtoword_true.p')
    print word_and_id_getter.get_wordID('中国')
    print word_and_id_getter.get_word(12345)

    wordVec = WordVec('word_vec_dict_true.p')
    print wordVec.get_word_vec(word_and_id_getter.get_wordID('中国'))



