# Influx data importation
This file describes how to make a local copy of the InfluxDB database and create a JSON dump of the SOL Objects.
We assume that you are working in a GNU/Linux environment.

If influxDB is not installed on your machine, follow the official website guide:
https://influxdata.com/


### Dump the production database (on the REALMS server)

`influxd backup -database realms /my/dump/name`

Note that dumps are currently made every our and can be found at "/home/realms/influx_backup/*"

### Import the database (on your machine)

After transferring the dump into your local machine, stop your local InfluxDB server

`sudo service influxdb stop`

Now you can import the dump file into your local database:

```
sudo influxd restore -metadir /var/lib/influxdb/meta/ /path/to/dump/folder/
sudo influxd restore -database realms -datadir /var/lib/influxdb/data /path/to/dump/folder/
```

Restart the local InfluxDB server:

`sudo service influxdb start`


### Extracting the data

Query the local database (example):

`curl -G 'http://localhost:8086/query?pretty=true' "db=realms" --data-urlencode "q=SELECT * FROM SOL_TYPE_DUST_EVENTMOTECREATE GROUP BY mac limit 1000" > influx_dump`

TODO: add script to export data into json
