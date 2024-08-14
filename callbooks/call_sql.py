#!/usr/bin/env python
# coding:utf-8

import os
from pathlib import Path
import pymysql
from pymysql.cursors import DictCursor
from .cb_query import cb_query

class Callerror(Exception):
    pass

class CallsignNotFound(Exception):
    pass

class CallsessionNotFound(Exception):
    pass

class CallMissingCredentials(Exception):
    pass

class CallSQL(cb_query):
    def __init__(self,cfg=None):
        super().__init__(cfg)
        self._dbcursor = None
        self._sqltable = 'callinfo'
        self._sqldatabase = 'callbook'
        self._dxcctable = 'dxcc'
        self._sqlhost = 'localhost'
        self._sqlusername = 'callbookuser'
        self._sqlpassword = None
        self._db = None ## database connection
        self._columnnames = None  ## names of the columns in the callbook.callinfo table
        self._dxcccolumnnames = None ## names of the columns in the callbook.dxcc table

    def connectdb(self):
        if (self._cfg):
            if self._cfg.has_section('mariadb'):
                sqlusername = self._cfg.get('mariadb','username')
                sqlpassword = self._cfg.get('mariadb','password')
                sqldatabase = self._cfg.get('mariadb','database')
                sqlhost     = self._cfg.get('mariadb','host')
                sqltable    = self._cfg.get('mariadb','table')
                sqlport     = int(self._cfg.get('mariadb','port'))
            elif self.cfg.has_section('sql'):
                sqlusername = self._cfg.get('sql','username')
                sqlpassword = self._cfg.get('sql','password')
                sqldatabase = self._cfg.get('sql','database')
                sqlhost     = self._cfg.get('sql','host')
                sqltable    = self._cfg.get('sql','table')
                sqlport     = int(self._cfg.get('mariadb','port'))
            elif self.cfg.has_section('mysql'):
                sqlusername = self._cfg.get('mysql','username')
                sqlpassword = self._cfg.get('mysql','password')
                sqldatabase = self._cfg.get('mysql','database')
                sqlhost     = self._cfg.get('mysql','host')
                sqltable    = self._cfg.get('mysql','table')
                sqlport     = int(self._cfg.get('mariadb','port'))
        if self._db is None or not self._db.open:
            self._db = pymysql.connect( host=sqlhost, user=sqlusername, passwd=sqlpassword, database=sqldatabase, port=sqlport)
        cur = self._db.cursor(cursor=DictCursor)
        self._dbcursor = cur
        return cur

    def callsign(self, callsign, retry=True):
        result = None
        if self._dbcursor is None:
            self.connectdb()
        where = " WHERE `callsign` ='"+callsign+"' "
        n = self._dbcursor.execute("SELECT * FROM "+self._sqltable+where)
        if n <=0:
            return None
        row = self._dbcursor.fetchone()
        if row is None:
            return None
        if self._columnnames is None:
            self.getcolumns(row)
        return row
    
    def dxcc(self,dxcc,retry=True):
        result = None
        if self._dbcursor is None:
            self.connectdb()
        where = """WHERE `dxcc` ='{}'""".format(dxcc)
        n = self._dbcursor.execute("""SELECT * FROM {0} {1}""".format(self._dxcctable,where))
        if n <= 0: return None
        row = self._dbcursor.fetchone()
        if row is None: return None
        for x in row:
            if row[x] is None:
                row[x] = ''
        return row
    
    def getdxcccolumns(self,rowsample:dict = None):
        if self._dxcccolumnnames is None:
            self._dxcccolumnnames = self.getcols(self._sqldatabase,self._dxcctable)
        return self._dxcccolumnnames

    def getcols(self,database:str,tablename:str):
        n = self.connectdb().execute("SELECT column_name FROM information_schema.columns WHERE table_schema = '{0}' AND table_name = '{1}'".format(database,tablename))
        if n <= 0: return None
        cols = self._dbcursor.fetchall()
        columns = []
        for x in cols:
            columns.append(x['column_name'])
        return columns

    def getcolumns(self,rowsample:dict = None):
        if self._columnnames is None:
            self._columnnames = self.getcols(self._sqldatabase,self._sqltable)
        return self._columnnames

    def insertdxcc(self,dxcc:str,data:dict):
        sql = """INSERT INTO `{}` """.format(self._dxcctable)
        insertcols = "\n( `dxcc`"
        insertvals = "'"+data['dxcc']+"'"
        updatecols = " "
        addcomma=False
        assert(not data is None)
        assert(not dxcc is None)
        colnames = self._dxcccolumnnames
        if colnames is None:
            colnames = self.getdxcccolumns()
        assert(not colnames is None)
        assert(colnames[0] == 'dxcc')
        for x in colnames:
            if x == 'dxcc':
                continue
            if x in data:
                val = data[x]
            else:
                continue
            if val is None or val == '':
                continue
            insertcols += ",`"+x+"`"
            insertvals += ",'"+str(val)+"'"
            if not addcomma:
                addcomma = True
            else:
                updatecols+=","
            updatecols += " `"+x+"` = '"+str(val).replace("'","''")+"'"

        sql += insertcols
        sql += ")\nVALUES("+insertvals+") "
        sql += "\nON DUPLICATE KEY UPDATE  "
        sql += updatecols
        n = self._dbcursor.execute(sql)
        self._db.commit()
             
    def insertcall(self,callsign:str,data:dict):
        # soso
        sql = "INSERT INTO `"+self._sqltable+"` "
        insertcols = "\n( `callsign`"
        insertvals = "'"+callsign+"'"
        updatecols = " "
        addcomma=False

        if self._columnnames is None:
            self.getcolumns()
        for x in self._columnnames:
            if x == "callsign":
                continue
            if x in data:
                val = data[x]
            else:
                continue
            if val is None or val == '' or val == 'None':
                continue
            insertcols += ",`"+x+"`"
            insertvals += ",'"+str(val).replace("'","''")+"'"
            if not addcomma:
                addcomma=True
            else:
                updatecols += ", "
            updatecols += " `"+x+"` = '"+str(val).replace("'","''")+"'"

        sql += insertcols
        sql += ")\nVALUES("+insertvals+") "
        sql += "\nON DUPLICATE KEY UPDATE  "
        sql += updatecols
        n = self._dbcursor.execute(sql)
        self._db.commit()
