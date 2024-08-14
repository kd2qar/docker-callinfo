#!/usr/bin/env python
# coding:utf-8

import os
import requests
import xmltodict
import configparser
from .cb_query import cb_query
from configparser import SafeConfigParser

class QRZerror(Exception):
    pass

class CallsignNotFound(Exception):
    pass

class QRZsessionNotFound(Exception):
    pass

class QRZMissingCredentials(Exception):
    pass

class QRZ(cb_query):
    def _get_session(self):
        if self._cfg and self._cfg.has_section('qrz'):
            username    = self._cfg.get('qrz', 'username', fallback='')
            password    = self._cfg.get('qrz', 'password', fallback='')
            agent       = self._cfg.get('qrz','agent',fallback='MH1.1')
            apiVersion  = self._cfg.get('qrz','apiversion',fallback='1.34')
        else:
            username = os.environ.get('QRZ_USER')
            password = os.environ.get('QRZ_PASSWORD')
        if not username or not password:
            raise QRZMissingCredentials("No Username/Password found")
        version='1.31'

        url = '''https://xmldata.qrz.com/xml/{3}/?username={0}&password={1};;agent={2}'''.format(username, password,agent,apiVersion)
        self._session = requests.Session()
        self._session.verify = bool(os.getenv('SSL_VERIFY', False))
        r = self._session.get(url)
        if r.status_code == 200:
            raw_session = xmltodict.parse(r.content)
            self._session_key = raw_session.get('QRZDatabase').get('Session').get('Key')
            if self._session_key:
                return True
        raise QRZsessionNotFound("Could not get QRZ session")

    def callsign(self, callsign, retry=True):
        if self._session_key is None:
            self._get_session()
        url = """http://xmldata.qrz.com/xml/current/?s={0}&callsign={1}""".format(self._session_key, callsign)
        r = self._session.get(url)
        if r.status_code != 200:
            raise Exception("Error Querying: Response code {}".format(r.status_code))
        raw = xmltodict.parse(r.content).get('QRZDatabase')
        if not raw:
            raise QRZerror('Unexpected API Result')
        if raw['Session'].get('Error'):
            errormsg = raw['Session'].get('Error')
            if 'Session Timeout' in errormsg or 'Invalid session key' in errormsg:
                if retry:
                    self._session_key = None
                    self._session = None
                    return self.callsign(callsign, retry=False)
            elif "not found" in errormsg.lower():
                raise CallsignNotFound(errormsg)
            raise QRZerror(raw['Session'].get('Error'))
        else:
            ham = raw.get('Callsign')
            if ham:
                if 'email' in ham:
                    ham['qrz_email'] = ham['email']
                    ham['email']=''
                return ham
        raise Exception("Unhandled Error during Query")

    def dxcc(self,dxcc:str,retry=True):
        if self._session_key is None:
            self._get_session()

        # https://xmldata.qrz.com/xml/current/?s=d0cf9d7b3b937ed5f5de28ddf5a0122d;dxcc=291
        url = """https://xmldata.qrz.com/xml/current/?s={0};dxcc={1}""".format(self._session_key,dxcc)
        r = self._session.get(url)
        if r.status_code != 200:
            raise Exception("Error Querying: Response code P{".format(r.status_code))
        raw = xmltodict.parse(r.content).get('QRZDatabase')
        if not raw:
            raise QRZerror('Unexpected API Result')
        if raw['Session'].get('Error'):
            errormsg = raw['Session'].get('Error')
            if 'Session Timeout' in errormsg or 'Invalid session key' in errormsg:
                if retry:
                    self._session_key = None
                    self._session = None
                    return self.dxcc(dxcc, retry=False)
            elif "not found" in errormsg.lower():
                raise CallsignNotFound(errormsg)
            raise QRZerror(raw['Session'].get('Error'))
        else:
            dx = raw.get('DXCC')
            if dx:
                return dx
        raise Exception("Unhandled Error during Query")        
