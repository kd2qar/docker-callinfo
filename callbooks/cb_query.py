#!/usr/bin/env python
# coding:utf-8
import os
import requests
import xmltodict
import configparser
from configparser import SafeConfigParser


class cb_query(object):
    def __init__(self, cfg=None):
        if cfg:
            self._cfg = SafeConfigParser()
            self._cfg.read(cfg)
        else:
            self._cfg = None
        self._session = None
        self._session_key = None
        self._program_name = 'MH1.1'

    def get_key(self,keyname,query_results):
        value = ""
        if keyname in query_results:
            value = query_results[keyname]
            if value is None:
                value = ''
            return value
        return '';    

    def printResult(self,result:dict):
        """
        print formatted results
        """        
        for x in result:
            print(x.ljust(10)+"= "+result[x])

    def _get_session(self):
        """
        Override in child class
        """
        raise NotImplemented()

    def callsign(self, callsign, retry=True):
        """
        Override in child class
        """
        raise NotImplemented()
