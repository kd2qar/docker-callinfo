#!/usr/bin/env python
# coding:utf-8

import os
import requests
import xmltodict
from .cb_query import cb_query

class HamQTHerror(Exception):
    """HamQTH Error"""
    pass

class CallsignNotFound(Exception):
    """Callsign Not Found Exception"""
    pass

class HamQTHsessionNotFound(Exception):
    """HamQTH Session Not Found"""
    pass

class HamQTHMissingCredentials(Exception):
    """HamQTH Missing Credentials"""
    pass

class HamQTH(cb_query):
    def _get_session(self):
        ## HamQTH session lasts 1 Hour
        if self._cfg and self._cfg.has_section('hamqth'):
            username = self._cfg.get('hamqth', 'username')
            password = self._cfg.get('hamqth', 'password')
        else:
            username = os.environ.get('HAMQTH_USER')
            password = os.environ.get('HAMQTH_PASSWORD')
        if not username or not password:
            raise HamQTHMissingCredentials("No Username/Password found")
        version='1.31'
        url = '''https://www.hamqth.com/xml.php?u={0}&p={1}'''.format(username,password)
        self._session = requests.Session()
        self._session.verify = bool(os.getenv('SSL_VERIFY', False))
        r = self._session.get(url)
        if r.status_code == 200:
            raw_session = xmltodict.parse(r.content).get('HamQTH')
            if raw_session['session'].get('error'):
                errormsg = raw_session['session'].get('error')
                if 'Wrong user name or password' in errormsg:
                    raise HamQTHerror(raw_session['session'].get('error'))
                raise  HamQTHerror(raw_session['session'].get('error'))
            else:
                self._session_key = raw_session['session'].get('session_id')
                if self._session_key:
                    return True
        raise HamQTHsessionNotFound("Could not get HamQTH session")

    def callsign(self, callsign, retry=True):
        if self._session_key is None:
            self._get_session()
        url = """https://www.hamqth.com/xml.php?id={0}&callsign={1}&prg={2}""".format(self._session_key, callsign, self._program_name)
        r = self._session.get(url)
        if r.status_code != 200:
            raise Exception("Error Querying: Response code {}".format(r.status_code))
        raw = xmltodict.parse(r.content).get('HamQTH')
        #print(raw)
        if not raw:
            raise HamQTHerror('Unexpected API Result')
        if raw.get('session'):
            if raw.get('session').get('error'):
                errormsg = raw['session'].get('error')
                if 'Session does not exist' in errormsg or 'expired' in errormsg:
                    if retry:
                        self._session_key = None
                        self._session = None
                        return self.callsign(callsign, retry=False)
                elif "not found" in errormsg.lower():
                    raise CallsignNotFound(errormsg)
                raise HamQTHerror(raw.get('session').get('error'))
        else:
            ham = raw.get('search')
            if ham:
                if 'email' in ham:
                    ham['hamqth_email'] = ham['email']
                    ham = self.removekey(ham,'email')
                return ham
        raise Exception("Unhandled Error during Query")
