# -*- coding: utf-8 -*-


class Config(object):  # object를 전달하는 이유?
    DATABASE = '/tmp/minitwit.db'
    PER_PAGE = 30
    DEBUG = True
    SERCRET_KEY = 'development'
