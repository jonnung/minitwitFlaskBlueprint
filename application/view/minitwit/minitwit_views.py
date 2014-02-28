# -*- coding: utf-8 -*-

from flask import render_template, g, url_for, request, redirect, flash
from flask.blueprints import Blueprint


bp_minitwit = Blueprint('bp_minitwit', __name__)
bp_user = Blueprint('bp_user', __name__)


@bp_minitwit.route('/')
def timeline():
    return render_template('timeline.html')


@bp_user.route('/')
def user():
    return render_template('user.html')


@bp_user.route('/register', methods=['GET', 'POST'])
def register():
    """
    사용자 등록 뷰함수
    GET 메서드는 사용자 등록화면을 보여주기 위해
    POST 매서드는 사용자 정보가 전송되어 사용자를 등록을 처리하기 위해
    """
    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            g.db.execute('''insert into user (
                username, email, pw_hash) values (?, ?, ?)''',
                [request.form['username'], request.form['email'],
                 generate_password_hash(request.form['password'])])
            g.db.commit()
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)