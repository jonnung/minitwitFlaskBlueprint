# -*- coding: utf-8 -*-
from flask import Flask
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing


class MinitwitModel(Flask):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        with closing(self.connect_db()) as db:
            with self.open_resource('schema.sql') as f:
                db.cursor().executescript(f.read())
            db.commit()

        self.config.from_object('application.config.settings.Config')

    def connect_db(self):
        return sqlite3.connect(self.config['DATABASE'])

    def query_db(self, query, args=(), one=False):
        pass

    @before_request
    def before_request(self):
        g.db = self.connect_db()
        g.user = None
        if 'user_id' in session:
            g.user = self.query_db('select * from user where user_id = ?', [session['user_id']], one=True)
