#!/usr/bin/python3

#import importlib
#moduleName='qrz.qrz_query'
#importlib.import_module(moduleName) 
import sys
import qrz_query
import certifi
import urllib3
from qrz_query import QRZ
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
        return value
    return '';

def get_sql(result):
    call = get_key('call',result).lower()
    fname = get_key('fname',result)
    name = get_key('name', result)
    addr1 = get_key('addr1',result)
    addr2 = get_key('addr2',result)
    zipcode = get_key('zip',result)
    county  = get_key('county',result)
    grid = get_key('grid',result)
    state = get_key('state',result)
    country = get_key('country',result)
    email = get_key('email',result)
    nickname = get_key('nickname',result)
    licclass = get_key('class',result)
    land = get_key('land',result)
    lat  = get_key('lat',result)
    lon  = get_key('lon',result)
    dxcc = get_key('dxcc',result)
    born = get_key('born',result)

    print("/*");
    #print(result);
    print("call    = "+call);
    print("fname   = "+fname);
    print("name    = "+name);
    print("nickname= "+nickname);
    print("addr1   = "+addr1);
    print("addr2   = "+addr2);
    print("zip     = "+zipcode);
    print("state   = "+state);
    print("country = "+country);
    print("county  = "+county);
    print("dxcc    = "+dxcc);
    print("class   = "+licclass);
    print("land    = "+land);
    print("email   = "+email);
    print("grid    = "+grid);
    print("lat     = "+lat);
    print("lon     = "+lon);
    print("born    = "+born);
    #print("*/");
    sql =""
    sql += "DELIMITER $$ \n"
    sql += "IF (SELECT callsign FROM rcforb.rawny_details WHERE callsign = '"+call+"') = '"+call+"' THEN \n"
    sql += "     UPDATE rcforb.rawny_details "
    sql += "SET "

    FIELDS = "`callsign`"
    VALUES = "'"+call+"'"

    #if fname != '' and name != '':
    #    sql += "`fullname`='"+fname+" "+name+"'"
    #    FIELDS += ", `fullname`"
    #    VALUES +=  ",'"+fname+" "+name+"'"
    if addr2 != '':
        sql += "`addr2`='"+addr2+"'"
        FIELDS += ",`addr2`"
        VALUES +=  ",'"+addr2+"'"
    if grid != '':
        sql += ",`grid`='"+grid+"'"
        FIELDS +=  ",`grid`"
        VALUES += ",'"+grid+"'"
    if state != '':
        sql += ",`state`='"+state+"'"
        FIELDS += ",`state`"
        VALUES += ",'"+state+"'"
    if country != '':
        sql += ",`country`='"+country+"'"
        FIELDS += ",`country`"
        VALUES += ",'"+country+"'"
    if fname != '':
        sql += ",`firstname`='"+fname+"'"
        FIELDS += ",`firstname`"
        VALUES += ",'"+fname+"'"
    if name != '':
        sql += ",`lastname`='"+name+"'"
        FIELDS += ",`lastname`"
        VALUES += ",'"+name+"'"
    if email != '':
        sql += ",`qrz_email`='"+email+"'"
        FIELDS += ",`email`"
        VALUES += ",'"+email+"'"
        FIELDS += ",`qrz_email`"
        VALUES += ",'"+email+"'"
    if licclass != '':
        sql += ", `class`='"+licclass+"'"
        FIELDS += ",`class`"
        VALUES += ",'"+licclass+"'"
    if nickname != '':
        sql += ", `nickname`='"+nickname+"'"
        FIELDS += ",`nickname`"
        VALUES += ",'"+nickname+"'"
 
    
    sql += "     WHERE `callsign`='"+call+"';\n"
    sql += " ELSE \n"
    sql += "     INSERT INTO rcforb.rawny_details ("+FIELDS+") VALUES("+VALUES+") ; \n"
    sql += "END IF $$ \n"
    sql += "DELIMITER ; "
    return sql


qrz = QRZ('./settings.cfg')

cal = 'kd2qar'
print(sys.argv[1:])
print ("*/")

for cal in sys.argv[1:]:
    try:
        print("/*")
        result = qrz.callsign(cal)
        print(result)
    except:
        print('oops')
        print("*/")
    else:
        #print_keys(['fname', 'name'], result)
        #print_keys(['addr2', 'state'], result)
        #print_keys(['country'], result)
        #print_keys(['grid','email'], result)

        sql = get_sql(result)
        print("*/")
        print(sql)
    
    print('')

