#!/usr/bin/env python
# Query callsigns using available callbooks
import sys
import qrz_query
import hamqth_query
import certifi
import urllib3
from pathlib import Path
from qrz_query import QRZ
from hamqth_query import HamQTH

urllib3.disable_warnings()
useHamqth=True
useQrz=True
nosql=False

table = "rcforb.rawny_details"
gettable = False
temptable = '`test`.`temptable_calldata_temptable`'



# run through the arguments
for cal in sys.argv[1:]:
    if cal == '-h' or cal == '--help' or cal == '-?':
        print("callinfo [--help] [-n|--nosql] [(-t|--table) <database>.<table> ]  <callsign1 callsign2 ...>")
        print("\t --help:  Print this help and exit")
        print("\t --nosql: Do not output the sql statements")
        print("\t --table: Specify the database table to be used for the sql output")
        print("\t --qrz:   Only query data from QRZ.com")
        print("\t --hamqth: Only query data from hamqth.com")
        exit(0)
    if cal == '-t' or cal == '--table':
        gettable = True
        print("/* get table on next round */")
        continue
    if cal == '-n' or cal == '--nosql':
        nosql=True
        print("/* NO SQL OUTPUT WILL BE GENERATED */")
        continue
    if cal == '--noqrz':
        useQrz = False
        continue
    if cal == '--nohamqth':
        useHamqth = False
        continue
    if gettable == True:
        print("/* new table changed from "+table+" to "+cal+" */")
        table = cal
        gettable = False
        continue
    try:
        print("/*")
        #raise Exception("FAKE IT")
        if not useQrz:
            raise  Exception("Skip QRZ")
        result = qrz.callsign(cal)
        print(result)
        print("*/")
    except Exception as ex:
        try:
            print('oops QRZ')
            print(ex)
            result = hamqth.callsign(cal)
            print(result)
            print("*/")
        except Exception as ex1:
            #print(ex)
            print('oops HamQTH')
            print(ex1)
            print("*/")
        else:
            sql = get_sql(result,cal, table)
            print("*/")
            print(sql)
    else:
        #print_keys(['fname', 'name'], result)
        #print_keys(['addr2', 'state'], result)
        #print_keys(['country'], result)
        #print_keys(['grid','email'], result)
        sql = ""
        #sql = get_sql2(result, cal, table, temptable)
        sql += get_sql(result,cal,table)
        print("*/")
        print(sql)
    
    print('')