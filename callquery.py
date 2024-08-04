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
print("/*") 
urllib3.disable_warnings();
useHamqth=True
useQrz=True
nosql=False

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

def get_key(keyname,query_results):
    value = ""
    if keyname in query_results:
        value = query_results[keyname]
        if value is None:
            value = ''
        return value
    return '';

def get_sql(result,query_call, table):
    call = get_key('call',result).lower()
    if call == '':
        call = get_key('callsign',result).lower()
    fname = get_key('fname',result)
    if fname == '':
        fname = get_key('nick',result)
    name = get_key('name', result)
    if name == '':
        name = get_key('adr_name',result)
    addr1 = get_key('addr1',result)
    if addr1 == '':
        addr1 = get_key('adr_street1',result)
    city = get_key('addr2',result)
    if city == '':
        city = get_key('adr_city',result)
    zipcode = get_key('zip',result)
    if zipcode == '':
        zipcode = get_key('adr_zip',result)
    county  = get_key('county',result)
    if county == '':
        county = get_key('us_county',result)
    grid = get_key('grid',result)
    state = get_key('state',result)
    if state == '':
        state = get_key('us_state',result)
    country = get_key('country',result)
    if country == '' or get_key('adr_country',result) != '':
        country = get_key('adr_country',result)
    email = get_key('email',result)
    nickname = get_key('nickname',result)
    if nickname == '':
        nickname = get_key('nick',result)
    licclass = get_key('class',result)
    land = get_key('land',result)
    if land == '':
        land = get_key('country',result)
    lat  = get_key('lat',result)
    if lat == '':
        lat = get_key('latitude',result)
    lon  = get_key('lon',result)
    if lon == '':
        lon = get_key('longitude',result)
    dxcc = get_key('dxcc',result)
    if dxcc == '':
        dxcc = get_key('adif',result)
    born = get_key('born',result)
    if born == '':
        born = get_key('birth_year',result)

    aliases = get_key('aliases',result)
    areacode= get_key('AreaCode',result)
    timezone= get_key('TimeZone',result)
    utcoffset= get_key('GMTOffset',result)
    if utcoffset == '':
         utcoffset = get_key('utc_offset',result)
    continent = get_key('continent',result)

    qsldirect = get_key('mqsl',result)
    if qsldirect == '':
        qsldirect = get_key('qsldirect',result)
    buro = get_key('qsl',result)
    lotw = get_key('lotw',result)
    eqsl = get_key('eqsl',result)
    cqzone = get_key('cqzone',result) 
    if cqzone == '':
        cqzone = get_key('cq',result)
    ituzone = get_key('ituzone',result)
    if ituzone == '':
        ituzone = get_key('itu',result)
    qsl_via = get_key('qslmgr',result)
    if qsl_via == '':
        qsl_via = get_key('qsl_via',result)
    qsldirect = get_key('mqsl',result)
    if qsldirect == '':
        qsldirect = get_key('qsldirect',result)
    trustee = get_key('trustee',result)

    print("/*")
    #print(result)
    print("call      = "+call)
    print("trustee   = "+trustee)
    print("aliases   = "+aliases)
    print("fname     = "+fname)
    print("name      = "+name)
    print("nickname  = "+nickname)
    print("addr1     = "+addr1)
    print("city      = "+city)
    print("zip       = "+zipcode)
    print("state     = "+state)
    print("country   = "+country)
    print("county    = "+county)
    print("areacode  = "+areacode)
    print("timezone  = "+timezone)
    print("utcoffset = "+utcoffset)
    print("continent = "+continent)
    print("dxcc      = "+dxcc)
    print("class     = "+licclass)
    print("land      = "+land)
    print("email     = "+email)
    print("grid      = "+grid)
    print("lat       = "+lat)
    print("lon       = "+lon)
    print("born      = "+born)
    print("direct    = "+qsldirect)
    print("buro      = "+buro)
    print("lotw      = "+lotw)
    print("eqsl      = "+eqsl)
    print("ituzone   = "+ituzone)
    print("cqzone    = "+cqzone)
    print("qsl_via   = "+qsl_via)
    #print("*/");
    if nosql:
        return ""
    sql =""
    if table == 'test.temptable_calldata_temptable' or table == '`test`.`temptable_calldata_temptable`' :
        mtempTableCreate = Path('/root/temptable.sql').read_text()
        sql = tempTableCreate
    sql += "DELIMITER $$ \n"
    if table == 'fieldday.qrzdata':
        sql += "IF (SELECT fdcall FROM "+table+" WHERE fdcall = '"+query_call+"') = '"+query_call+"' THEN \n"
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
        nAmE = name.replace("'","''")
        sql += "`lastname`='"+nAmE+"'"
        FIELDS += ",`lastname`"
        VALUES += ",'"+nAmE+"'"
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
    if addr1 != '':
        Addr1 = addr1.replace("'","''")
        if comma:
            sql += ","
        sql += "`addr1`='"+Addr1+"'"
        FIELDS += ", `addr1`"
        VALUES += ",'"+Addr1+"'"
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

