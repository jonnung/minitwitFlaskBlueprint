# -*- coding: utf-8 -*-

import os

from flask import Flask, render_template, g, session
from application.view.minitwit import bp_minitwit, bp_user, timeline
from application.model import db


class MinitwitApp(Flask):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.__init_config__()
        self.__register_blueprints()

    def __init_config__(self):
        self.config.from_object('application.config.settings.Config')
        self.config.from_envvar('MINITWIT_SETTINGS', silent=True)

    def __register_blueprints(self):
        """
        블루프린트 지정
        """
        self.register_blueprint(bp_minitwit, url_prefix='/timeline')
        self.register_blueprint(bp_user, url_prefix='/user')
        self.add_url_rule('/', 'home', view_func=timeline)
        self.template_folder = os.path.join(os.path.dirname((os.path.dirname(os.path.dirname(__file__)))), 'templates')

        # Error handlers
        # Handle 404 errors
        @self.errorhandler(404)
        def page_not_fount(error):
            return render_template('404.html'), 404

        # Handle 500 errors
        @self.errorhandler(500)
        def server_error(error):
            return render_template('500.html'), 500

        @self.before_request
        def before_request():
            """
            Flask 에서 제공하는 요청에 앞서서 실행되는 함수
            """
            g.db = db.connect_db()
            # 전역객체 g: 한 번의 요청에 대해서만 같은 값을 유지하고 /
            #             스레드에 대해 안전하는 전제 조건
            g.user = None
            if 'user_id' in session:
                g.user = db.query_db('select * from user where user_id = ?', [session['user_id']], one=True)

        @self.teardown_request
        def teardown_request(exception):
            """
            Flask 에서 제공하는 응답이 생성된 후 실행되는 함수
            """
            if hasattr(g, 'db'):
                g.db.close()