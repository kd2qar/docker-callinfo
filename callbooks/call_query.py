#!/usr/bin/env python
# coding:utf-8

import os
import datetime
from pathlib import Path
from .qrz_query import QRZ
from .hamqth_query import HamQTH
from .cb_query import cb_query
from .call_sql import CallSQL

class Callerror(Exception):
    pass

class CallsignNotFound(Exception):
    pass

class CallsessionNotFound(Exception):
    pass

class CallMissingCredentials(Exception):
    pass

class CallQuery(cb_query):
    def __init__(self,cfg=None):
        super().__init__(cfg)
        self.useQrz = True
        self.useHamqth = True
        self.forceRefresh = False
        self._refreshDays = 90
        if self._cfg and self._cfg.has_section('callbook') and self._cfg.has_option('callbook','refreshDays') :
            try:
                self._refreshDays = self._cfg.getint('callbook','refreshDays',fallback=90)
            except:
                """ no op """

        self.qrz = QRZ(cfg)
        self.hamQTH = HamQTH(cfg)
        self.callSQL = CallSQL(cfg)

    def callsign(self, callsign, retry=True):
        result = None
        refreshdb = True
        if not self.forceRefresh:
            try:
                result=self.callSQL.callsign(callsign)
                if result and 'last_updated' in result:
                    lu = result['last_updated']
                    nw = datetime.datetime.now()
                    delta = nw-lu
                    if (delta.days > self._refreshDays):
                        # force a refresh
                        result = None

            except Exception as ex:
                print('/*')
                print('oops SQL')
                print(ex)
                print('*/')
            else:
                if (result):
                    refreshdb = False
                    self.useQrz=False
                    self.useHamqth=False 
        if self.useQrz:
            try:
                result=self.qrz.callsign(callsign)
            except Exception as ex:
                print('/*\noops QRZ')
                print(ex)
                print('*/')
            else:
                self.useHamqth=False
                refreshdb = True

        if self.useHamqth:
            try:
                result = self.hamQTH.callsign(callsign)
            except Exception as ex1:
                print('/*\noops HamQTH')
                print(ex1)
                print('*/')
            else:
                print('-- using hamqth')
                print("/*");print(result);print("*/")
                refreshdb = True
        if result == None:
            myresult = dict()
            return myresult
        myresult = self.getresult(callsign,result)
        if refreshdb:
            self.callSQL.insertcall(callsign,myresult)
        return myresult
    
    def dxcc(self,dxcc:str,retry=True):
        refreshdb=True
        result = None
        try:
            result = self.callSQL.dxcc(dxcc)
            if result and 'last_updated' in result:
                lu = result['last_updated']
                nw = datetime.datetime.now()
                delta = nw-lu
                if (delta.days > self._refreshDays):
                    # force a refresh
                    result = None
        except Exception as ex:
            print('/* oops DXCC SQL')
            print(str(ex) + '*/')
        else:
            if (result):
                refreshdb = False
        if result == None:
            try:
                result = self.qrz.dxcc(dxcc)
                result['entity_number'] = result['dxcc']
                result['entity_name']=result['name']
                result['dxcc_name']=result['name']
                result['utcoffset']=result['timezone']
                result['lattitude']=result['lat']
                result['longitude']=result['lon']
                if result['cqzone'] is None or  result['cqzone'] == 0 or result['cqzone'] == '0' or result['cqzone'] == 'None' :
                    result['cqzone']=''
                if result['ituzone'] is None or result['ituzone'] ==0 or result['ituzone'] =='0' or result['ituzone'] == 'None' :
                    result['ituzone']=''
            except Exception as ex:
                print('/* oops DXCC QRZ')
                print('{0} */',ex)
            else:
                refreshdb = True
        if refreshdb:
            self.callSQL.insertdxcc(dxcc,result)
        return result


    def convertkeys(self,keys:list,result:dict):
        val = ''
        for x in keys:
            val = self.get_key(x,result)
            if val != '': break
        return val
    
    def getresult(self,query_call:str,result:dict):
        myresult = dict()

        myresult['callsign'] = self.convertkeys(['callsign','call'],result)
        myresult['prev_call']=self.convertkeys(['prev_call','p_call'],result)
        myresult['querycall'] = query_call.lower()
        myresult['firstname'] = self.convertkeys(['firstname','fname','nick'],result).title()
        lastname = self.convertkeys(['lastname','name','adr_name'],result)
        if lastname.isupper(): lastname = lastname.title() # only title names that are only uppercase. Assume mixed case is as intended
        myresult['lastname'] = lastname
        myresult['nickname']=self.convertkeys(['nickname','nick'],result).title()
        myresult['street1']=self.convertkeys(['street1','addr1','adr_street1'],result)
        myresult['city']=self.convertkeys(['city','addr2','adr_city'],result)
        myresult['postalcode']=self.convertkeys(['postalcode','zip','adr_zip','zipcode'],result)
        myresult['county']= self.convertkeys(['county','us_county'],result)
        myresult['grid'] = self.convertkeys(['grid','gridsquare'],result)
        myresult['state']=self.convertkeys(['state','us_state'],result)
        myresult['country'] = self.convertkeys(['country','adr_country'],result)
        myresult['email']=self.convertkeys(['email'],result)
        myresult['licclass']=self.convertkeys(['licclass','class'],result)
        myresult['lattitude']=self.convertkeys(['lattitude','latitude','lat'],result)
        myresult['longitude']=self.convertkeys(['longitude','lon'],result)
        # DXCC Number
        myresult['dxcc']=self.convertkeys(['dxcc','adif'],result)
        # DXXCC Name
        myresult['dxcc_name']=self.convertkeys(['dxcc_name','land','country'],result)
        myresult['birthyear']=self.convertkeys(['birthyear','born','birth_year'],result)
        myresult['aliases']=self.convertkeys(['aliases'],result)
        myresult['areacode']=self.convertkeys(['areacode','AreaCode'],result)
        myresult['timezone']=self.convertkeys(['timezone','TimeZone'],result)
        myresult['utcoffset']=self.convertkeys(['utcoffset','utc_offset','GMTOffset'],result)
        myresult['continent']=self.convertkeys(['continent'],result)
        myresult['qsldirect']=self.convertkeys(['qsldirect','msql'],result)
        myresult['buro']=self.convertkeys(['buro','qsl'],result)
        myresult['lotw']=self.convertkeys(['lotw'],result)
        myresult['eqsl']=self.convertkeys(['eqsl'],result)
        myresult['cqzone']=self.convertkeys(['cqzone','cq'],result)
        myresult['ituzone']=self.convertkeys(['ituzone','itu'],result)
        myresult['qsl_via']=self.convertkeys(['qsl_via','qslmgr'],result)
        myresult['trustee']=self.convertkeys(['trustee'],result)
        myresult['efdate']=self.convertkeys(['efdate'],result)
        myresult['expdate']=self.convertkeys(['expdate'],result)
        myresult['biodate']=self.convertkeys(['biodate'],result)
        myresult['moddate']=self.convertkeys(['moddate'],result)
        # FIPS county identifier (USA)
        myresult['fips']=self.convertkeys(['fips'],result)
        myresult['ccode']=self.convertkeys(['ccodem'],result)

        ## AUGMENT WITH DXCC INFORMATION
        if myresult['dxcc'] != '':
            dxccdata = self.dxcc(myresult['dxcc'])
            if not dxccdata is None:
                if self.get_key('continent',myresult) == '':
                    myresult['continent'] = dxccdata['continent']
                if self.get_key('dxcc_name',myresult) == '':
                    myresult['dxcc_name']=dxccdata['dxcc_name']
                if self.get_key('ituzone',myresult) == '':
                    myresult['ituzone']=str(dxccdata['ituzone'])
                if self.get_key('cqzone',myresult) == '':
                    myresult['cqzone']=str(dxccdata['cqzone'])
                if self.get_key('utcoffset',myresult) =='':
                    myresult['utcoffset']=str(dxccdata['utcoffset'])
                if self.get_key('longitude',myresult) =='':
                    myresult['longitude']=dxccdata['longitude']
                if self.get_key('lattitude',myresult) =='':
                    myresult['lattitude']=dxccdata['lattitude']
            else:
                assert(False)
        return myresult
    
    def printResult(self,result:dict):
        """
        print formatted results
        """        
        for x in result:
            print(x.ljust(10)+"= "+result[x])

    def getFieldMap(self,table:str):
        cfg = self._cfg
        if cfg and cfg.has_section(table):
            cmap = {}
            for x in cfg.items(table):
                cmap[x[0]]=x[1]
            return cmap
        return None
