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
table = "rcforb.rawny_details"

if callquery._cfg:
    try:
        table = callquery._cfg.get('callbook','outputTable')
    except:
        """ no op """

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
    if map is None: map = {'callsign': 'callsign', 'email': 'email', 'firstname': 'firstname'}
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
    return callquery.getFieldMap(table)

# ****************************************************************************

cal = 'w1aw'
print(sys.argv[1:])
print ("*/")

nosql=False
useQrz = True
useHamqth = True
noResults = False
forceRefresh=False
noBlanks=False
compact = False
listTables = False
gettable = False

callsigns = []

def help():
    print("callinfo [--help] [-n|--nosql] [(-t|--table) <database>.<table> ]  <callsign1 callsign2 ...>")
    print("\t --help:       Print this help and exit")
    print("\t --nosql:      Do not output the sql statements")
    print("\t --noresult:   Do not output the results list")
    print("\t --noblanks:   Do not output empty results")
    print("\t --brief:      Same as --nosql --noblanks")
    print("\t --table:      Specify the database table to be used for the sql output")
    print("\t --listtables: Get a list of table available in config file")
    print("\t --qrz:        Only query data from QRZ.com")
    print("\t --hamqth:     Only query data from hamqth.com")

for cal in sys.argv[1:]:
    if cal[:1] == '-':
        if cal == '-h' or cal == '--help' or cal == '-?':
            help()
            exit(0)
        if cal == '-t' or cal == '--table':
            gettable = True
            print("-- get table on next round")
            continue
        if cal == '-lt' or cal == '--listtables' or cal == '--listtable':
            listTables = True
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
        if cal == '--noblanks':
            noBlanks = True
            continue
        if cal == '--brief':
            noBlanks = True
            nosql = True
            continue
        if cal == '--compact':
            compact = True
            nosql = True
            continue
        if cal == '--refresh' or cal == '--force':
            forceRefresh = True
            continue        
        # UNKNOWN OPTION
        print("UNKNOWN OPTION: "+cal)
        help()
        exit(2)
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
callquery.noBlanks = noBlanks
#callquery.compact = compact
results = []

if listTables :
    tables = callquery.listTables()
    print(tables)
    exit(0)

for cal in callsigns:
    if not compact:
        print("-- "+cal+" --")
    result = callquery.callsign(cal)
    if not result is None and 'callsign' in result and result['callsign'] != '':
        if compact:
            results.append(result)
        else:
            if not noResults:
                if not nosql: print("/*")
                callquery.printResult(result)
                if not nosql: print("*/")
            if not nosql:
                sql = ""
                sql += get_sql(cal,table,result)
                print(sql)
            print('')
    else:
        print("/* ",result," */")

if compact:
    fields = {'callsign':len('callsign'),'fullname':len('name'),'grid':len('grid'),'county':len('county'),'city':len('city'),'SPC':len('SPC')}
    callquery.compact_header_emitted = False
    for r in results:
        if not 'fullname' in r:
            r['fullname'] = callquery.fullname(r)
        if not 'SPC' in r:
            r['SPC'] = callquery.spc(r)

        for f in fields:
            if r in results:
                fields[f]=max(fields[f],len(r[f]))
    for r in results:
        callquery.printCompact(r,fields)


