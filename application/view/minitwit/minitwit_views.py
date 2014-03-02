# -*- coding: utf-8 -*-

import time
from datetime import datetime
from hashlib import md5
from flask import render_template, g, url_for, request, redirect, flash, session, abort
from flask.blueprints import Blueprint
from application.model import db
from application.config.settings import Config
from werkzeug import check_password_hash, generate_password_hash


bp_minitwit = Blueprint('bp_minitwit', __name__)
bp_user = Blueprint('bp_user', __name__)


def get_user_id(username):
    """
    기존 사용자 여부 체크
    """
    rv = db.execute('select user_id from user where username = ?', [username]).fetchone()
    return rv[0] if rv else None


def format_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=80):
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)


@bp_minitwit.route('/')
def timeline():
    if not g.user:
        return redirect(url_for('bp_minitwit.public_timeline'))
    return render_template('timeline.html', messages=db.query_db('''
        select message.*, user.* from message, user where message.author_id = user.user_id and (
          user.user_id ? or
          user.user_id in (select whom_id from follower where who_id = ?))
        order by message.pub_date desc limit ?
    ''', [session['user_id'], session['usr_id']], Config.PER_PAGE))


@bp_minitwit.route('/public')
def public_timeline():
    return render_template('timeline.html', messages=db.query_db('''
        select message.*, user.* from message, user
        where message.author_id = user.user_id
        order by message.pub_date desc limit ?
    ''', [Config.PER_PAGE]))


@bp_minitwit.route('/<username>')
def user_timeline(username):
    profile_user = db.query_db('select * from user where username = ?', [username], one=True)
    if profile_user is None:
        abort(404)
    followed = False
    if g.user:
        followed = db.query_db('''select 1 from follower
          where follower.who_id = ? and follower.whom_id = ?
        ''', [session['user_id'], profile_user['user_id']], one=True) is not None
    return render_template('timeline.html', messages=db.query_db('''
        select message.*, user.* from message, user
        where user.user_id = message.author_id and user.user_id = ?
        order by message.pub_date desc limit ?
        ''', [profile_user['user_id'], Config.PER_PAGE]), followed=followed, profile_user=profile_user)


@bp_minitwit.route('/add_message', methods=['POST'])
def add_message():
    if 'user_id' not in session:
        abort(404)
    if request.form['text']:
        db.execute('''insert into message (author_id, text, pub_date)
          values (?, ?, ?)''', [session['user_id'], request.form['text'], int(time.time())])
        db.commit()
        flash('Your message was recorded')
    return redirect(url_for('bp_minitwit.timeline'))


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
        return redirect(url_for('bp_minitwit.timeline'))
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
            db.execute('''insert into user (
                username, email, pw_hash) values (?, ?, ?)''',
                [request.form['username'], request.form['email'],
                 generate_password_hash(request.form['password'])])
            db.commit()
            flash('You were successfully registered and can login now')
            return redirect(url_for('bp_user.login'))
    return render_template('register.html', error=error)


@bp_user.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('bp_minitwit.timeline'))
    error = None
    if request.method == 'POST':
        user = db.query_db(''' select * from user where
            username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'], request.form['password']):
            error = 'Invalid passowrd'
        else:
            flash('You were logged in')
            session['user_id'] = user['user_id']
            return redirect(url_for('bp_minitwit.timeline'))
    return render_template('login.html', error=error)


@bp_user.route('/<username>/follow')
def follow_user(username):
    if not g.user:
        abort(404)
    whom_id = get_user_id(username)
    if whom_id is None:
        abort(404)
    db.execute('insert into follower (who_id, whom_id) values (?, ?)', [session['user_id'], whom_id])
    db.commit()
    flash('You are now following "%s"' % username)
    return redirect(url_for('bp_minitwit.user_timeline', username=username))


@bp_user.route('/<username>/unfollow')
def unfollow_user(username):
    if not g.user:
        abort(404)
    whom_id = get_user_id(username)
    if whom_id is None:
        abort(404)
    db.execute('delete from follower where who_id=? and whom_id=?', [session['user_id'], whom_id])
    db.commit()
    flash('You are no longer following "%s"' % username)
    return redirect(url_for('bp_minitwit.user_timeline', username=username))

