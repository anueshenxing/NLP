# coding=utf-8

from src.util import *

if __name__ == "__main__":
    all_news_ctg_title_data = load_cPickle('all_news_ctg_title_data.p')
    print all_news_ctg_title_data[0]
