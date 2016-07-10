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
out_file.write("time,mac,neighborMac,neighborFlag,rssi,numTxPackets,numTxFailures,numRxPackets\n")
for obj in json_list:
    time    = tools.iso_to_epoch(obj["timestamp"])

    for key, value in obj["value"]["neighbors"].iteritems():
        nbr_mac = tools.id_to_mac(value["neighborId"],time)
        if nbr_mac is not None:
            out_file.write(
                str(time)+','+\
                str(obj["mac"])+','+\
                str(nbr_mac)+','+\
                str(value["neighborFlag"])+','+\
                str(value["rssi"])+','+\
                str(value["numTxPackets"])+','+\
                str(value["numTxFailures"])+','+\
                str(value["numRxPackets"])+\
                '\n'
            )
