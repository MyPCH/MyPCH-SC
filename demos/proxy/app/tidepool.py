# -*- coding: utf-8 -*-
import json

from flask import current_app

import requests
from requests.auth import HTTPBasicAuth


class TidePool():
    """A handle to the TP backend"""

    def __init__(self, account: dict):
        """Init object from env settings"""
        current_app.logger.info('Called TP init: ' + account['username'])
        self.username = account['username']
        self.password = account['password']
        self.url = account['url']
        # FIXME sanity check
        urlauth = '/auth/login'
        self.login(urlauth)

    def login(self, urlauth):
        """Attempt to login the TP backend """
        url = str(self.url)+str(urlauth)
        current_app.logger.info(url + ' ' + str(self.username) + ' ' + str(self.password))
        try:
            response = requests.post(url, auth=HTTPBasicAuth(self.username, self.password))
        except requests.exceptions.InvalidSchema:
            self.auth = None
            return
        current_app.logger.info('Status code returned from login attempt: ' +
                                str(response.status_code))
        json_data = json.loads(response.text)
        token = response.headers['x-tidepool-session-token']
        userid = json_data['userid']
        result = {}
        result['headers'] = {'x-tidepool-session-token': str(token),
                             'Content-Type': 'application/json'}
        result['userid'] = str(userid)
        self.auth = result

    def get(self):
        current_app.logger.info('Called TP proxy get')
        if self.auth is not None:
            # FIXME try catch
            r = requests.get(self.url + '/data/'+self.auth['userid'],
                             headers=self.auth['headers'])
            current_app.logger.info('Status code returned from GET: '+str(r.status_code))
            if len(r.json()) <= 0:
                current_app.logger.warning('No upstream data, check account details')
            else:
                return(json.dumps(r.json()))
        return None

    def post(self, pumpdata):
        current_app.logger.info('Called TP proxy post')
        pumpdata = json.dumps(pumpdata)
        if self.auth is not None:
            # FIXME try catch
            r = requests.post(url=self.url + '/data/'+self.auth['userid'],
                              data=pumpdata)
            current_app.logger.info('Status code returned from POST: '+str(r.status_code))
