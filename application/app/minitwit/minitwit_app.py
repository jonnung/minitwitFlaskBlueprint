# -*- coding: utf-8 -*-

import os

from flask import Flask, render_template
from application.view.minitwit import bp_minitwit, timeline


class MinitwitApp(Flask):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.__init_config__()
        self.__register_blueprints()

    def __init_config__(self):
        self.config.from_object('application.config.settings.Config')
        self.config.from_envvar('MINITWIT_SETTINGS', silent=True)

    def __register_blueprints(self):
        self.register_blueprint(bp_minitwit, url_prefix='/timeline')
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