import json
import influxdb
import tools

# open output file
out_file = open('../data/hr_neighbors.csv','w')

# configure influxDB
influxClient = influxdb.client.InfluxDBClient(
    host        = 'localhost',
    port        = '8086',
    database    = 'realms'
)

# query influxDB
query       =   "SELECT * FROM SOL_TYPE_DUST_NOTIF_HRNEIGHBORS"
query       +=  " WHERE site='ARG_junin' GROUP BY mac"
json_list   = tools.influxdb_to_json(influxClient.query(query).raw)

# write json to file
for obj in json_list:
    time    = tools.iso_to_epoch(obj["timestamp"])
    mote_id = tools.mac_to_id(obj["mac"],time)

    if mote_id is None:
        pass

    for key, value in obj["value"]["neighbors"].iteritems():
            out_file.write(
                time+','+\
                str(mote_id)+','+\
                str(value["neighborId"])+','+\
                str(value["rssi"])+\
                '\n'
            )
