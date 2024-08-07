#!/usr/bin/python3

#import importlib
#moduleName='qrz.qrz_query'
#importlib.import_module(moduleName) 
import sys
import qrz_query
import hamqth_query
import certifi
import urllib3
from pathlib import Path
from qrz_query import QRZ
from hamqth_query import HamQTH
from call_query import CallQuery

print("/*") 
urllib3.disable_warnings()
useHamqth=True
useQrz=True
nosql=False
callquery = CallQuery('./settings.cfg')


def print_keys(key_names, query_result):
    """
    Prints results and does not throw exception on queries
    like W1AW where fname key does not exist
    """
    info = ""
    for key_name in key_names:
        if key_name in query_result:
            info += query_result[key_name] + " "
    print(info)

def get_key(keyname,query_result):
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

def get_sql(result, table):
    querycall = get_key('querycall',result)
    call = get_key('callsign',result)
    fname = get_key('firstname',result)
    name = get_key('lastname', result)
    street1 = get_key('street1',result)
    city = get_key('city',result)
    zipcode = get_key('postalcode',result)
    county  = get_key('county',result)
    grid = get_key('grid',result)
    state = get_key('state',result)
    country = get_key('country',result)
    email = get_key('email',result)
    nickname = get_key('nickname',result)
    licclass = get_key('licclass',result)
    land = get_key('land',result)
    lat = get_key('lattitude',result)
    lon = get_key('longitude',result)
    dxcc = get_key('dxcc',result)
    born = get_key('birthyear',result)
    aliases = get_key('aliases',result)
    areacode = get_key('areacode',result)
    timezone = get_key('timezone',result)
    utcoffset = get_key('utcoffset',result)
    continent = get_key('continent',result)
    qsldirect = get_key('qsldirect',result)
    buro = get_key('buro',result)
    lotw = get_key('lotw',result)
    eqsl = get_key('eqsl',result)
    cqzone = get_key('cqzone',result) 
    ituzone = get_key('ituzone',result)
    qsl_via = get_key('qslmgr',result)
    trustee = get_key('trustee',result)
    efdate  = get_key('efdate',result)
    expdate = get_key('expdate',result)
    biodate = get_key('biodate',result)
    moddate = get_key('moddate',result)
    fips    = get_key('fips',result)
    ccode   = get_key('ccode',result)

    #print("/*")
    #callquery.printResult(result)
    #print("*/")
    if nosql:
        return ""
    sql =""
    if table == 'test.temptable_calldata_temptable' or table == '`test`.`temptable_calldata_temptable`' :
        tempTableCreate = Path('/root/temptable.sql').read_text()
        sql = tempTableCreate
    sql += "DELIMITER $$ \n"
    if table == 'fieldday.qrzdata':
        sql += "IF (SELECT fdcall FROM "+table+" WHERE fdcall = '"+querycall+"') = '"+querycall+"' THEN \n"
    else:
        sql += "IF (SELECT callsign FROM "+table+" WHERE callsign = '"+call+"') = '"+call+"' THEN \n"
    sql += "     UPDATE "+table+" "
    sql += "SET "

    FIELDS = "`callsign`"
    VALUES = "'"+call+"'"

    if table == 'fieldday.qrzdata':
        FIELDS = "`fdcall`, "+FIELDS
        VALUES = "'"+query_call+"', "+VALUES
        sql += "`callsign`='"+call+"',"

    #if fname != '' and name != '':
    #    sql += "`fullname`='"+fname+" "+name+"'"
    #    FIELDS += ", `fullname`"
    #    VALUES +=  ",'"+fname+" "+name+"'"
    comma = False
    if city != '':
        sql += "`city`='"+city+"'"
        FIELDS += ",`city`"
        VALUES +=  ",'"+city+"'"
        comma = True
    if grid != '':
        if comma:
            sql+= ","
        sql += "`grid`='"+grid+"'"
        FIELDS +=  ",`grid`"
        VALUES += ",'"+grid+"'"
        comma = True
    if state != '':
        if comma:
            sql += ","
        sql += "`state`='"+state+"'"
        FIELDS += ",`state`"
        VALUES += ",'"+state+"'"
        comma = True
    if country != '':
        if comma:
            sql+= ","
        sql += "`country`='"+country+"'"
        FIELDS += ",`country`"
        VALUES += ",'"+country+"'"
        comma = True
    if fname != '':
        if comma:
            sql += ","
        sql += "`firstname`='"+fname+"'"
        FIELDS += ",`firstname`"
        VALUES += ",'"+fname+"'"
        comma = True
    if name != '':
        if comma:
            sql += ","
        lastname = name.replace("'","''")
        sql += "`lastname`='"+lastname+"'"
        FIELDS += ",`lastname`"
        VALUES += ",'"+lastname+"'"
        comma = True
    if email != '':
        if comma:
            sql += ","
        sql += "`qrz_email`='"+email+"'"
        FIELDS += ",`email`"
        VALUES += ",'"+email+"'"
        FIELDS += ",`qrz_email`"
        VALUES += ",'"+email+"'"
        comma = True
    if licclass != '':
        if comma:
            sql += ","
        sql += "`class`='"+licclass+"'"
        FIELDS += ",`class`"
        VALUES += ",'"+licclass+"'"
        comma = True
    if nickname != '':
        nn = nickname.replace("'","''")
        if comma:
            sql += ","
        sql += "`nickname`='"+nn+"'"
        FIELDS += ",`nickname`"
        VALUES += ",'"+nn+"'"
        comma = True
    if lat != '':
        if comma:
            sql +=","
        sql += "`lattitude`='"+lat+"'"
        FIELDS += ",`lattitude`"
        VALUES += ",'"+lat+"'"
        comma = True
    if lon != '':
        if comma:
            sql +=","
        sql += "`longitude`='"+lon+"'"
        FIELDS += ", `longitude`"
        VALUES += ",'"+lon+"'"
        comma = True
    if aliases != '':
        Aliases = aliases.replace("'","''")
        if comma:
            sql+=","
        sql += "`aliases`='"+Aliases+"'"
        FIELDS += ", `aliases`"
        VALUES += ",'"+Aliases+"'"
        comma = True
    if street1 != '':
        street1 = street1.replace("'","''")
        if comma:
            sql += ","
        sql += "`addr1`='"+street1+"'"
        FIELDS += ", `addr1`"
        VALUES += ",'"+street1+"'"
        comma = True
    if continent != '':
        if comma:
            sql += ","
        sql += "`continent`='"+continent+"'"
        FIELDS += ", `continent`"
        VALUES += ",'"+continent+"'"
        comma = True
    if zipcode != '':
        if comma:
            sql += ","
        sql += "`postalcode`='"+zipcode+"'"
        FIELDS += ",`postalcode`"
        VALUES += ",'"+zipcode+"'"
        comma = True
    if ituzone != '':
        if comma:
            sql += ","
        sql += "`ituzone`="+ituzone
        FIELDS += ",`ituzone`"
        VALUES += ","+ituzone
        comma = True
    if cqzone != '':
        if comma:
            sql += ","
        sql += "`cqzone`="+cqzone
        FIELDS += ",`cqzone`"
        VALUES += ","+cqzone
        comma = True
    if dxcc != '':
        if comma:
            sql += ","
        sql += "`dxcc`="+dxcc
        FIELDS += ",`dxcc`"
        VALUES += ","+dxcc
        comma=True
    if trustee != '':
        if comma:
            sql += ","
        sql += "`trustee`='"+trustee+"'"
        FIELDS += ",`trustee`"
        VALUES +=",'"+trustee+"'"
        comma = True
 
    if table == 'fieldday.qrzdata':
        sql += "     WHERE `fdcall`='"+query_call+"';\n"
    else:
        sql += "     WHERE `callsign`='"+call+"';\n"

    sql += " ELSE \n"
    sql += "     INSERT INTO "+table+" ("+FIELDS+") VALUES("+VALUES+") ; \n"
    sql += "END IF $$ \n"
    sql += "DELIMITER ; "
    return sql

def get_sql2(result,query_call, table, temptable):
    sql =""
    tempTableCreate = Path('/root/temptable.sql').read_text()
    sql += tempTableCreate
    sql += get_sql(result,query_call,temptable)
    #print("*/");
    if nosql:
        return ""
    return sql

# ****************************************************************************


qrz = QRZ('./settings.cfg')
hamqth = HamQTH('./settings.cfg')

cal = 'kd2qar'
print(sys.argv[1:])
print ("*/")

nosql=False
useQrz = True
useHamqth = True


table = "rcforb.rawny_details"
gettable = False
temptable = '`test`.`temptable_calldata_temptable`'

callsigns = []

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
    callsigns.append(cal)
    continue
    

for cal in callsigns:
    print("-- "+cal+" --")
    if True:
        #callquery = CallQuery('./settings.cfg')
        result = callquery.callsign(cal)
        if not nosql: print("/*")
        #print(result)
        callquery.printResult(result)
        if not nosql: print("*/")
        if not nosql:
            sql = ""
            #sql = get_sql2(result, cal, table, temptable)
            sql += get_sql(result,table)
            print(sql)

        print('')

