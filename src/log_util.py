# coding=utf-8

import global_params
import os


class LogUtil(object):
    def __init__(self, log_name):
        if not os.path.exists(global_params.LOG_FILE_DIR):
            os.mkdir(global_params.LOG_FILE_DIR)
        self.log = open(global_params.LOG_FILE_DIR + log_name, 'a')

    def log_info(self, info):
        self.log.write('INFO: => ' + info + '\n')
