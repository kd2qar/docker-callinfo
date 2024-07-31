#!/usr/bin/python3

#import importlib
#moduleName='qrz.qrz_query'
#importlib.import_module(moduleName) 
import sys
import qrz_query
import hamqth_query
import certifi
import urllib3
from qrz_query import QRZ
from hamqth_query import HamQTH
print("/*") 
urllib3.disable_warnings();

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
    addr2 = get_key('addr2',result)
    if addr2 == '':
        addr2 = get_key('adr_city',result)
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

    print("/*")
    #print(result)
    print("call      = "+call)
    print("aliases   = "+aliases)
    print("fname     = "+fname)
    print("name      = "+name)
    print("nickname  = "+nickname)
    print("addr1     = "+addr1);
    print("addr2     = "+addr2)
    print("zip       = "+zipcode)
    print("state     = "+state)
    print("country   = "+country)
    print("county    = "+county)
    print("areacode  = "+areacode)
    print("timezone  = "+timezone)
    print("utcoffset = "+utcoffset)
    print("continent = "+continent)
    print("dxcc      = "+dxcc);
    print("class     = "+licclass);
    print("land      = "+land);
    print("email     = "+email);
    print("grid      = "+grid);
    print("lat       = "+lat);
    print("lon       = "+lon);
    print("born      = "+born);
    print("lotw      = "+lotw);
    print("eqsl      = "+eqsl);
    print("ituzone   = "+ituzone);
    print("cqzone    = "+cqzone);
    print("qsl_via   = "+qsl_via);
    print("qsldirect = "+qsldirect);
    #print("*/");
    sql =""
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
    if addr2 != '':
        sql += "`addr2`='"+addr2+"'"
        FIELDS += ",`addr2`"
        VALUES +=  ",'"+addr2+"'"
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
 
    if table == 'fieldday.qrzdata':
        sql += "     WHERE `fdcall`='"+query_call+"';\n"
    else:
        sql += "     WHERE `callsign`='"+call+"';\n"

    sql += " ELSE \n"
    sql += "     INSERT INTO "+table+" ("+FIELDS+") VALUES("+VALUES+") ; \n"
    sql += "END IF $$ \n"
    sql += "DELIMITER ; "
    return sql


qrz = QRZ('./settings.cfg')
hamqth = HamQTH('./settings.cfg')

cal = 'kd2qar'
print(sys.argv[1:])
print ("*/")

table = "rcforb.rawny_details"
gettable = False
for cal in sys.argv[1:]:
    if cal == '-t' or cal == '--table':
        gettable = True
        print("/* get table on next round */")
        continue
    if gettable == True:
        print("/* new table changed from "+table+" to "+cal+" */")
        table = cal
        gettable = False
        continue
    try:
        print("/*")
        #raise Exception("FAKE IT")
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

        sql = get_sql(result,cal, table)
        print("*/")
        print(sql)
    
    print('')

