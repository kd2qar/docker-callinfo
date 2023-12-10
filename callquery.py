#!/usr/bin/python3

#import importlib
#moduleName='qrz.qrz_query'
#importlib.import_module(moduleName) 
import sys
import qrz_query
from qrz_query import QRZ
print("/*") 

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

def get_sql(result):
    call = get_key('call',result).lower()
    fname = get_key('fname',result)
    name = get_key('name', result)
    addr2 = get_key('addr2',result)
    grid = get_key('grid',result)
    state = get_key('state',result)
    country = get_key('country',result)
    email = get_key('email',result)
    sql =""
    sql += "DELIMITER $$ \n"
    sql += "IF (SELECT callsign FroM rcforb.rawny_details WHERE callsign = '"+call+"') = '"+call+"' THEN \n"
    sql += "     UPDATE rcforb.rawny_details SET `fullname`='"+fname+" "+name+"',`addr2`='"+addr2+"',"
    sql += "`grid`='"+grid+"',`state`='"+state+"',`country`='"+country+"',"
    sql += "`email`='"+email+"' WHERE `callsign`='"+call+"';\n"
    sql += "ELSE \n"
    sql += "     INSERT INTO rcforb.rawny_details (`callsign`, `fullname`,`addr2`,`grid`,`state`,`country`,`email`) VALUES('"+call+"','"+fname+" "+name+"','"+addr2+"','"+grid+"','"+state+"','"+country+"','"+email+"') ; \n"
    sql += "END IF $$ \n"
    sql += "DELIMITER ; "
    return sql


qrz = QRZ('./settings.cfg')

cal = 'kd2qar'
print(sys.argv)
print ("*/")

for cal in sys.argv:
    try:
        print("/*")
        result = qrz.callsign(cal)
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

