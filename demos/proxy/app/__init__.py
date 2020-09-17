# -*- coding: utf-8 -*-
import logging
from os import environ

from app.account import accounts
from app.config import Config

import connexion

from flask import current_app, redirect, render_template, request, session, url_for

from flask_dance.contrib.google import google, make_google_blueprint

from flask_session import Session

from flask_talisman import Talisman


# ------------------------------------------------------------------------------
app = connexion.App(__name__, specification_dir='./',
                    options={'swagger_ui': True})
sess = Session(app.app)
feature_policy = {'geolocation': 'none'}
ENVIRONMENT = environ.get('MYPCH_CONFIG') or 'dev'
if ENVIRONMENT == 'test':
    CONFIG = Config('test')
elif ENVIRONMENT == 'prod':
    CONFIG = Config('prod')
else:
    CONFIG = Config('dev')
if 'DYNO' in environ:
    on_heroku = True
else:
    on_heroku = False
if on_heroku or ENVIRONMENT == 'prod':
    # force security
    print('INFO running with talisman')
    csp = {'default-src': ['\'self\'', 'mypch.herokuapp.com'],
           'font-src': ['\'self\'',
                        'https://fonts.gstatic.com',
                        'https://fonts.googleapis.com'],
           'style-src': ['\'self\'', 'https://cdnjs.cloudflare.com']}
    talisman = Talisman(app.app, feature_policy=feature_policy,
                        content_security_policy=csp,
                        force_https_permanent=True)
else:
    print('WARNING running without talisman')
    print('INFO heroku: ', on_heroku)
app.add_api('./swagger.yaml', strict_validation=True)  # ??not app.app
app.app.secret_key = environ.get('FLASK_SECRET_KEY')
app.app.config['SESSION_TYPE'] = 'filesystem'
app.app.config['ON_HEROKU'] = on_heroku
sess.init_app(app.app)
app.app.config['GOOGLE_OAUTH_CLIENT_ID'] = environ.get('GOOGLE_OAUTH_CLIENT_ID')
app.app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
app.app.config.update(vars(CONFIG))
# TODO - add minimal test of env vars to provide better logging in cases where env is missing
log_level_int = getattr(logging, CONFIG.log_level.upper(), None)
if isinstance(log_level_int, int):
    app.app.logger.setLevel(log_level_int)
if hasattr(app.app.config, 'OAUTHLIB_INSECURE_TRANSPORT'):
    if app.app.config['OAUTHLIB_INSECURE_TRANSPORT']:
        print('WARNING insecure oauth')
if not on_heroku:
    print('INFO heroku: ', on_heroku)
    print(app.app.config)
google_blueprint = make_google_blueprint(scope=['email'], offline=True)
app.app.register_blueprint(google_blueprint, url_prefix='/login')


# ------------------------------------------------------------------------------
def retrieve_user():
    if google.authorized:
        resp = google.get('/oauth2/v1/userinfo')
        # oauthlib.oauth2.rfc6749.errors.TokenExpiredError: FIXME
        assert resp.ok, resp.text  # FIXME
        session['username'] = resp.json()['email']
        if session['username'] in accounts:
            session['approved'] = True
            api = 'Yes'
        else:
            session['approved'] = False
            api = 'No'
        session['template'] = session['username'] + '(API approval: ' + api + ')'
        print('retrieve_user - Defining user to ',
              session['username'], session['approved'])

# ------------------------------------------------------------------------------
# FIXME exception InsecureTransportError()


@app.app.before_request
def before_request_func():
    print('before_request is running')
    # FIXME : (userid is either unknown, RO, RW), account.module for session
    print('path request', request.path)
    if request.path.startswith('/api/ui/') or\
       request.path.startswith('/api/swagger.json'):
        print('path contains rest-api', request.path)
        if not google.authorized:
            return redirect(url_for('google.login'))
        if not session['approved']:
            print('user is not approved for the rest API')
            return redirect(url_for('google.login'))
        # disable strict talisman on the swagger page, FIXME
        print('disable strict CSP on swagger to render correct - FIXME!')
        if 'talisman' in globals():
            talisman.content_security_policy = {}


@app.app.route('/')
def index():
    retrieve_user()
    if 'username' in session:
        return render_template('index.html', name=session['template'])
    else:
        return render_template('index.html')


@app.app.route('/login')
def login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    # FIXME exception InsecureTransportError()
    retrieve_user()
    if 'username' in session:
        return render_template('index.html', name=session['template'])
    else:
        return render_template('index.html')


@app.app.route('/logout', methods=['GET'])
def logout():
    retrieve_user()
    if not google.authorized:
        return render_template('index.html')
    if 'username' in session:
        del session['username']
    if 'template' in session:
        del session['template']
    if hasattr(current_app.blueprints, 'google'):
        token = current_app.blueprints['google'].token['access_token']
        resp = google.post(
            'https://accounts.google.com/o/oauth2/revoke',
            params={'token': token},
            headers={'Content-Type": "application/x-www-form-urlencoded'},
        )
        assert resp.ok, resp.text  # FIXME
        del current_app.blueprints['google'].token['access_token']
    else:
        print('Missing attribute google')
    session.clear()
    # oauthlib.oauth2.rfc6749.errors.InvalidClientIdError: (invalid_request)
    # Missing required parameter: refresh_token
    # FIXME what if token empty
    if 'username' in session:
        return render_template('index.html', name=session['template'])
    else:
        return render_template('index.html')
