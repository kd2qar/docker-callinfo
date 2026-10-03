#!/usr/bin/python3
# coding:utf-8

import json

from pathlib import Path
from callbooks.call_query import CallQuery
from callbooks.qrz_query import QRZ

cq = CallQuery(cfg="./settings.cfg")
cq.useHamqth=False
cq.forceRefresh=True

qrz = cq.qrz #.callsign(callsign)
#KC2HZR
cal = qrz.callsign('kc2hzr')
scal = json.dumps(cal,indent=2)
print(scal)
cal = qrz.callsign('w2aka')
scal = json.dumps(cal,indent=2)

print(scal)

cal = qrz.callsign('n')
scal = json.dumps(cal,indent=2)

