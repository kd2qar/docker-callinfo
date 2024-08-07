#!/usr/bin/env python
# coding:utf-8

import os
import configparser
from configparser import SafeConfigParser
import qrz_query
import hamqth_query
from pathlib import Path
from qrz_query import QRZ
from hamqth_query import HamQTH

class Callerror(Exception):
    pass

class CallsignNotFound(Exception):
    pass

class CallsessionNotFound(Exception):
    pass

class CallMissingCredentials(Exception):
    pass

class CallQuery(object):
    def __init__(self,cfg=None):
        if cfg:
            self._cfg = SafeConfigParser()
            self._cfg.read(cfg)
        else:
            self.cfg = None
        self._session = None
        self.useQrz = True
        self.useHamqth = True
        self.qrz = QRZ(cfg)
        self.hamQTH = HamQTH(cfg)

    def get_key(self,keyname,query_results):
        value = ""
        if keyname in query_results:
            value = query_results[keyname]
            if value is None:
                value = ''
            return value
        return '';    

    def callsign(self, callsign, retry=True):
        result = None
        if self.useQrz:
            try:
                result=self.qrz.callsign(callsign)
            except Exception as ex:
                print('/*')
                print('oops QRZ')
                print(ex)
                print('*/')
            else:
                self.useHamqth=False

        if self.useHamqth:
            try:
                result = self.hamQTH.callsign(callsign)
            except Exception as ex1:
                print('/*')
                print('oops HamQTH')
                print(ex1)
                print('*/')
            else:
                print('/* using hamqth */')
                print("/*");print(result);print("*/")
        if result == None:
            myresult = dict()
            return myresult
        myresult = self.getresult(callsign,result)
        return myresult

    def getresult(self,query_call,result):
        myresult = dict()

        call = self.get_key('call',result).lower()
        if call == '':
            call = self.get_key('callsign',result).lower()
        myresult['callsign'] = call

        myresult['querycall'] = query_call.lower()

        fname = self.get_key('fname',result)
        if fname == '':
            fname = self.get_key('nick',result)
        myresult['firstname'] = fname.title()

        name = self.get_key('name', result)
        if name == '':
            name = self.get_key('adr_name',result)
        myresult['lastname'] = name.title()

        nickname = self.get_key('nickname',result)
        if nickname == '':
            nickname = self.get_key('nick',result)
        myresult['nickname']=nickname.title()

        addr1 = self.get_key('addr1',result)
        if addr1 == '':
            addr1 = self.get_key('adr_street1',result)
        myresult['street1']=addr1

        city = self.get_key('addr2',result)
        if city == '':
            city = self.get_key('adr_city',result)
        myresult['city']=city

        zipcode = self.get_key('zip',result)
        if zipcode == '':
            zipcode = self.get_key('adr_zip',result)
        myresult['postalcode']=zipcode

        county  =self.get_key('county',result)
        if county == '':
            county = self.get_key('us_county',result)
        myresult['county']= county

        grid = self.get_key('grid',result)
        myresult['grid'] = grid
        
        state = self.get_key('state',result)
        if state == '':
            state = self.get_key('us_state',result)
        myresult['state']=state

        country = self.get_key('country',result)
        if country == '' or self.get_key('adr_country',result) != '':
            country = self.get_key('adr_country',result)
        myresult['country'] = country

        email = self.get_key('email',result)
        myresult['email']=email

        licclass = self.get_key('class',result)
        myresult['licclass']=licclass

        land = self.get_key('land',result)
        if land == '':
            land = self.get_key('country',result)
        myresult['land']=land

        lat  = self.get_key('lat',result)
        if lat == '':
            lat = self.get_key('latitude',result)
        myresult['lattitude']=lat

        lon  = self.get_key('lon',result)
        if lon == '':
            lon = self.get_key('longitude',result)
        myresult['longitude']=lon

        dxcc = self.get_key('dxcc',result)
        if dxcc == '':
            dxcc = self.get_key('adif',result)
        myresult['dxcc']=dxcc

        born = self.get_key('born',result)
        if born == '':
            born = self.get_key('birth_year',result)
        myresult['birthyear']=born

        aliases = self.get_key('aliases',result)
        myresult['aliases']=aliases

        areacode= self.get_key('AreaCode',result)
        myresult['areacode']=areacode

        timezone= self.get_key('TimeZone',result)
        myresult['timezone']=timezone

        utcoffset= self.get_key('GMTOffset',result)
        if utcoffset == '':
            utcoffset = self.get_key('utc_offset',result)
        myresult['utcoffset']=utcoffset

        continent = self.get_key('continent',result)
        myresult['continent']=continent

        qsldirect = self.get_key('mqsl',result)
        if qsldirect == '':
            qsldirect = self.get_key('qsldirect',result)
        myresult['qsldirect']=qsldirect

        buro = self.get_key('qsl',result)
        myresult['buro']=buro

        lotw = self.get_key('lotw',result)
        myresult['lotw']=lotw

        eqsl = self.get_key('eqsl',result)
        myresult['eqsl']=eqsl

        cqzone = self.get_key('cqzone',result) 
        if cqzone == '':
            cqzone = self.get_key('cq',result)
        myresult['cqzone']=cqzone

        ituzone = self.get_key('ituzone',result)
        if ituzone == '':
            ituzone = self.get_key('itu',result)
        myresult['ituzone']=ituzone

        qsl_via = self.get_key('qslmgr',result)
        if qsl_via == '':
            qsl_via = self.get_key('qsl_via',result)
        myresult['qsl_via']=qsl_via
        
        trustee = self.get_key('trustee',result)
        myresult['trustee']=trustee

        efdate  = self.get_key('efdate',result)
        myresult['efdate']=efdate

        expdate = self.get_key('expdate',result)
        myresult['expdate']=expdate

        biodate = self.get_key('biodate',result)
        myresult['biodate']=biodate

        moddate = self.get_key('moddate',result)
        myresult['moddate']=moddate

        fips    = self.get_key('fips',result)
        myresult['fips']=fips

        ccode   = self.get_key('ccode',result)
        myresult['ccode']=ccode
        return myresult
    
    def printResult(self,result:dict):
        """
        print formatted results
        """        
        for x in result:
            print(x.ljust(10)+"= "+result[x])
