# -*- coding: utf-8 -*-
from app.account import accounts
from app.tidepool import TidePool

from flask import current_app, jsonify, session


# ------------------------------------------------------------------------------
def get():
    current_app.logger.info('ReST API - read')
    d = {}
    if 'username' in session:
        user = session['username']
        if user in accounts:
            current_app.logger.info('ReST API - user approved for backend data')
            # OYD get hook, unencrypted data from backend, please insert logic here, e.g.
            # usage policies, ...., either directly or via API calls to another micro service
            print(accounts[user])
            if current_app.config['ON_HEROKU']:
                current_app.logger.info('ReST API - on heroku')
                if (accounts[user]['fake_response']):
                    data = {'dd-data': str(accounts[user]['fake_response'])}
                    backenddata = jsonify(data)
                    current_app.logger.info('ReST API - fake response on heroku')
                else:
                    backenddata = None
            else:
                for _ in accounts:
                    if (accounts[_]['shared_users']) == user:
                        # FIXME
                        print('FIMXE - add from users sharing data with current user')
                tp = TidePool(accounts[user])
                backenddata = tp.get()
            if backenddata is not None:
                current_app.logger.warning('Returning upstream data')
                return backenddata
            else:
                current_app.logger.warning('ReST no backend data')
                return jsonify(d)
        else:
            current_app.logger.warning('ReST no translation between external and internal user')
            return jsonify(d)
    else:
        current_app.logger.warning('ReST missing username')
        return jsonify(d)


def post():
    current_app.logger.info('ReST API - post')
    d = {}
    if 'username' in session:
        user = session['username']
        if user in accounts:
            current_app.logger.info('ReST API - user approved for backend data')
            # OYD post hook, insert logic here, e.g. watermarking of data
            if current_app.config['ON_HEROKU']:
                if (accounts[user]['fake_post']):
                    d = {'dd-data': str(accounts[user]['fake_post'])}
                    backenddata = jsonify(d)
                else:
                    backenddata = None
            if backenddata is not None:
                current_app.logger.warning('Returning upstream data')
                return backenddata
            else:
                current_app.logger.warning('ReST no backend data')
                return jsonify(d)
        else:
            current_app.logger.warning('ReST no translation between external and internal user')
            return jsonify(d)
    else:
        current_app.logger.warning('ReST missing username')
        return jsonify(d)
#    if 1:
#        return make_response('upload successfully created', 201)
# ------------------------------------------------------------------------------
