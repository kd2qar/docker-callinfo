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
        self.noBlanks = False
        self.useQrz = True
        self.useHamqth = True
        self.forceRefresh = False
        #self.compact = False ## generate compact output.
        self.compact_header_emitted = False
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
        useQrz = self.useQrz
        useHamqth = self.useHamqth
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
                    useQrz=False
                    useHamqth=False 
        if useQrz:
            try:
                result=self.qrz.callsign(callsign)
            except Exception as ex:
                print('/*\noops QRZ')
                print(ex)
                print('*/')
            else:
                useHamqth=False
                refreshdb = True

        if useHamqth:
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
            ## Get final aggregate
            result=self.callSQL.callsign(callsign)
            myresult= self.getresult(callsign,result)
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
        myresult['prev_call'] = self.convertkeys(['prev_call','p_call'],result)
        myresult['querycall'] = query_call.lower()
        myresult['firstname'] = self.convertkeys(['firstname','fname','nick'],result).title()
        lastname = self.convertkeys(['lastname','name','adr_name'],result)
        if lastname.isupper(): lastname = lastname.title() # only title names that are only uppercase. Assume mixed case is as intended
        myresult['lastname'] = lastname
        myresult['nickname']=self.convertkeys(['nickname','nick'],result).title()
        myresult['street1']=self.convertkeys(['street1','addr1','adr_street1'],result)
        myresult['street2']=self.convertkeys(['street2'],result)
        myresult['city']=self.convertkeys(['city','addr2','adr_city'],result)
        myresult['postalcode']=self.convertkeys(['postalcode','zip','adr_zip','zipcode'],result)
        myresult['county']= self.convertkeys(['county','us_county'],result)
        myresult['grid'] = self.convertkeys(['grid','gridsquare'],result)
        myresult['state']=self.convertkeys(['state','us_state'],result)
        myresult['country'] = self.convertkeys(['country','adr_country'],result)
        myresult['phone'] = self.convertkeys(['phone'],result)
        myresult['email']=self.convertkeys(['email'],result)
        myresult['qrz_email']=self.convertkeys(['qrz_email'],result)
        myresult['hqth_email']=self.convertkeys(['hamqth_email','hqth_email'],result)
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
        myresult['qsl_manager']=self.convertkeys(['qsl_manager','qsl_via','qslmgr'],result)
        myresult['trustee']=self.convertkeys(['trustee'],result)
        myresult['efdate']=self.convertkeys(['efdate'],result)
        myresult['expdate']=self.convertkeys(['expdate'],result)
        myresult['biodate']=self.convertkeys(['biodate'],result)
        myresult['moddate']=self.convertkeys(['moddate'],result)
       # myresult['qrz_moddate']=self.convertkeys(['qrz_moddate'],result)
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
        for x in self.callSQL.getcolumns():
            if x == 'qrz_moddate' or x == 'location' or x == 'fullname' or x == 'last_updated' : continue
            assert x in myresult,"-- ------------- missing field:"+str(x)+" in myresult ------------------"
        return myresult
    
    def printResult(self,result:dict):
        """
        print formatted results
        """
        if result is None:
            return
        for x in result:
            if self.noBlanks and (result[x] is None or result[x] == ''):
                continue
            val = result[x]
            if val is None: val = ''
            print(x.ljust(12)+"= "+val)

    def spc(self,result:dict):
        if not result['state'] is None and not result['state'] == '':
            return result['state']
        return result['country']

    def fullname(self,result:dict):
        fullname =''
        if not result['nickname'] is None and not result['nickname'] == '':
            fullname = result['nickname'] + " " + result['lastname']
        else:
            if not result['firstname'] is None and not result['firstname'] == '':
                fullname = result['firstname'] + " " + result['lastname']
            else:
                fullname = result['lastname']
        return fullname

    def printCompact(self,result:dict,fields = None):
        if fields is None:
            if not self.compact_header_emitted:
                print('{:10s} {:20s} {:15s} {:15s} '.format('callsign', 'name','city','SPC'))
                self.compact_header_emitted = True

            print('{:10s} {:20s} {:15s} {:15s} '.format(result['callsign'], self.fullname(result), result['city'], self.spc(result)))
        else:
            row = ''
            if not self.compact_header_emitted:
                hdr = ''
                for f in fields:
                    hdr += f.ljust(fields[f]+1,' ')
                print(hdr)
                self.compact_header_emitted = True
            for f in fields:
                row += result[f].ljust(fields[f]+1,' ')
            print(row)

    def getFieldMap(self,table:str):
        cfg = self._cfg
        if cfg and cfg.has_section(table):
            cmap = {}
            for x in cfg.items(table):
                cmap[x[0]]=x[1]
            return cmap
        return None

    def listTables(self):
        cfg = self._cfg
        sects = cfg.sections()
        tables = []
        for a in sects:
            if (a == 'callbook' or a == 'qrz' or a == 'hamqth' or a == 'mariadb' or a == 'mysql' or a == 'clublog' ):
                continue
            tables.append(a)
        # print(tables)
        return tables


