#!/usr/bin/python3
# coding:utf-8

import sys
import certifi
import urllib3
from pathlib import Path
from callbooks.call_query import CallQuery

print("/*") 
urllib3.disable_warnings()
useHamqth=True
useQrz=True
nosql=False
callquery = CallQuery('./settings.cfg')

def print_keys(key_names:list, query_result:dict):
    """
    Prints results and does not throw exception on queries
    like W1AW where fname key does not exist
    """
    info = ""
    for key_name in key_names:
        if key_name in query_result:
            info += query_result[key_name] + " "
    print(info)

def get_key(keyname:str,query_result:dict):
    """
    Returns empty string for missing result
    """
    value = ""
    if keyname in query_result:
        value = query_result[keyname]
        if value is None:
            value = ''
        return value
    return ''

def get_sql(callsign:str,table:str,data:dict):
    # soso
    map = getFieldMap(table)
    columnnames = map.keys()
    columnnames = list(map)
    sql = "INSERT INTO "+table+" "
    addcomma=False

    for x in columnnames:
        if x == columnnames[0]:
            insertcols = "\n(`"+x+"` "
            insertvals = "'"+data[map[x]] +"'"
            updatecols = " "
            continue
        if map[x] in data:
            val = data[map[x]]
        else:
            continue
        if val is None or val == '':
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
    sql += ";"
    return sql

def getFieldMap(table):
    ## NEED TO CREATE A MORE FLEXIBLE FIELD MATCHING SYSTEM
    ## PROBABLY A MAPPING FILE
    if table == 'fieldday.qrzdata':
        return {'fdcall':'callsign','callsign':'callsign','aliases':'aliases',
         'trustee':'trustee','nickname':'nickname','firstname':'firstname',
         'lastname':'lastname','grid':'grid','lattitude':'lattitude',
         'longitude':'longitude','ituzone':'ituzone','cqzone':'cqzone',
         'dxcc':'dxcc','county':'county','continent':'continent','street1':'street1',
         'city':'city','state':'state','postalcode':'postalcode','country':'country',
         'licclass':'licclass','qrz_email':'qrz_mail','email':'email','phone':'phone'}
    if table == 'rcforb.rawny_details':
        return {'callsign':'callsign','aliases':'aliases',
         'trustee':'trustee','nickname':'nickname','firstname':'firstname',
         'lastname':'lastname','grid':'grid','lattitude':'lattitude',
         'longitude':'longitude','ituzone':'ituzone','cqzone':'cqzone',
         'dxcc':'dxcc','county':'county','continent':'continent','street1':'street1',
         'city':'city','state':'state','postalcode':'postalcode','country':'country',
         'licclass':'licclass','qrz_email':'qrz_mail','email':'email','phone':'phone'}
    if table == 'test.temptable_calldata_temptable':
        return{'callsign':'callsign','aliases':'aliases',
         'trustee':'trustee','nickname':'nickname','firstname':'firstname',
         'lastname':'lastname','grid':'grid','lattitude':'lattitude',
         'longitude':'longitude','ituzone':'ituzone','cqzone':'cqzone',
         'dxcc':'dxcc','county':'county','continent':'continent','street1':'street1',
         'city':'city','state':'state','postalcode':'postalcode','country':'country',
         'licclass':'licclass','qrz_email':'qrz_mail','email':'email','phone':'phone'
        }


# ****************************************************************************

cal = 'w1aw'
print(sys.argv[1:])
print ("*/")

nosql=False
useQrz = True
useHamqth = True
noResults = False
forceRefresh=False

table = "rcforb.rawny_details"
gettable = False
temptable = '`test`.`temptable_calldata_temptable`'

callsigns = []

for cal in sys.argv[1:]:
    if cal == '-h' or cal == '--help' or cal == '-?':
        print("callinfo [--help] [-n|--nosql] [(-t|--table) <database>.<table> ]  <callsign1 callsign2 ...>")
        print("\t --help:     Print this help and exit")
        print("\t --nosql:    Do not output the sql statements")
        print("\t --noresult: Do not output the results list")
        print("\t --table:    Specify the database table to be used for the sql output")
        print("\t --qrz:      Only query data from QRZ.com")
        print("\t --hamqth:   Only query data from hamqth.com")
        exit(0)
    if cal == '-t' or cal == '--table':
        gettable = True
        print("-- get table on next round")
        continue
    if cal == '-n' or cal == '--nosql':
        nosql=True
        print("-- NO SQL OUTPUT WILL BE GENERATED")
        continue
    if cal == '--noqrz' or cal == '--hamqth':
        useQrz = False
        continue
    if cal == '--nohamqth' or cal == '--qrz':
        useHamqth = False
        continue
    if cal == '--noresults':
        noResults = True
        continue
    if cal == '--refresh' or cal == '--force':
        forceRefresh = True
        continue        
    if gettable == True:
        print("-- new table changed from "+table+" to "+cal+"")
        table = cal
        gettable = False
        continue
    callsigns.append(cal)
    continue

callquery.useHamqth = useHamqth
callquery.useQrz = useQrz
callquery.forceRefresh = forceRefresh

for cal in callsigns:
    print("-- "+cal+" --")
    result = callquery.callsign(cal)
    if not result is None and 'callsign' in result and result['callsign'] != '':
        if not noResults:
            if not nosql: print("/*")
            callquery.printResult(result)
            if not nosql: print("*/")
        if not nosql:
            sql = ""
            sql += get_sql(cal,table,result)
            print(sql)
    print('')
