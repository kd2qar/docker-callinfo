# Query callbook sources
Query callbook sources given one or more callsigns and generate SQL code to insert or update a local database table.

The docker container wraps a python scripts and the necessary python libraries. You could run the scripts directly if you have a compatable version of python and libraries used by them.

Copy the file settings-example.cfg to settings.cfg
modify the file to add your own 
credentials for your local database and/or qrz and hamqth.

use the file sql/callinfo.sql to create the database schema used by the scripts.


Build the docker container using the command:

make

Run the file 'callinfo' giving a callsign as an argument.

It will attempt to lookup the data in your local database or on qrz.com or hamqth.
The results of those queries will be cached in you local database.
You can also augment the information in you local copy to fill in missing or updated values of phone numbers, email addresses or nicknames.

If you don't have a local database it can just do the online callbook lookups.


