import json
import influxdb
import time
import calendar
import tools

# open output file
out_file = open('../data/motecreate.csv','w')

# configure influxDB
influxClient = influxdb.client.InfluxDBClient(
    host        = 'localhost',
    port        = '8086',
    database    = 'realms'
)

# query influxDB
query       =   "SELECT * FROM SOL_TYPE_DUST_EVENTMOTECREATE"
query       +=  " WHERE site='ARG_junin' GROUP BY mac"
json_list   = tools.influxdb_to_json(influxClient.query(query).raw)

# write json to file
out_file.write('time,mac,id,lat,long\n')
for obj in json_list:
    out_file.write(
        str(tools.iso_to_epoch(obj["timestamp"]))+','+\
        obj["value"]["macAddress"]+','+\
        str(obj["value"]["moteId"])+','+\
        obj["value"]["latitude"]+','+\
        obj["value"]["longitude"]+\
        '\n'
    )
