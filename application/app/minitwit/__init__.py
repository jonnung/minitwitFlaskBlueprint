# -*- coding: utf-8 -*-

from application.app.minitwit.minitwit_app import MinitwitApp


def create_app():
    app = MinitwitApp(__name__)
    return app

app = create_app()