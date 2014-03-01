# -*- coding: utf-8 -*-
from flask import Flask, g
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing


class MinitwitModel(Flask):
    def __init__(self, *args, **kwargs):
        """
        데이터베이스 연결을 얻고 그 연결을 closing 클래스에 인자로 넘긴다.
        with 문과 함께 사용하여 with 블럭이 끝나면 closing 클래스로 넘어온 객체를 닫거나 제거한다.
        아래 with 문도 데이터베이스 스키마 파일(schema.sql)을 열고 해당 with 블럭에서
        데이터베이스 스키마 생성이 끝나면 열린 파일을 받으라는 것이다.
        """
        super(self.__class__, self).__init__(*args, **kwargs)
        self.config.from_object('application.config.settings.Config')
        with closing(self.connect_db()) as db:
            with self.open_resource('schema.sql') as f:
                db.cursor().executescript(f.read())
            db.commit()

    def connect_db(self):
        return sqlite3.connect(self.config['DATABASE'])

    def query_db(self, query, args=(), one=False):
        """
        데이터베이스 질의를 쉽게 처리할 수 있는 공통 함수
        """
        cur = g.db.execute(query, args)
        """
        dict() 구성자는 키-값 쌍이 투플로 저장된 리스트로부터 직접 사전을 만든다.
        """
        rv = [dict((cur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv  # 굉장히 깔끔하고 의미전달이 확실한 if문 같다