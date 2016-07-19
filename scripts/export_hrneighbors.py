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
out_file.write("time,mac,neighborMac,neighborFlag,rssi,numTxPackets,numTxFailures,numRxPackets,distance\n")
for obj in json_list:
    time    = tools.iso_to_epoch(obj["timestamp"])
    mote_lat, mote_long = tools.mac_to_position(obj["mac"],time)

    for key, nghbr in obj["value"]["neighbors"].iteritems():

        distance                = None
        nghbr_mac               = tools.id_to_mac(nghbr["neighborId"],time)
        nghbr_lat, nghbr_long   = tools.mac_to_position(nghbr_mac,time)
        if nghbr_lat is not None and mote_lat is not None:
            distance = tools.distance_on_unit_sphere(
                        mote_lat,
                        mote_long,
                        nghbr_lat,
                        nghbr_long
                    )
        else: distance = None

        nbr_mac = tools.id_to_mac(nghbr["neighborId"],time)
        if nbr_mac is not None:
            out_file.write(
                str(time)+','+\
                str(obj["mac"])+','+\
                str(nbr_mac)+','+\
                str(nghbr["neighborFlag"])+','+\
                str(nghbr["rssi"])+','+\
                str(nghbr["numTxPackets"])+','+\
                str(nghbr["numTxFailures"])+','+\
                str(nghbr["numRxPackets"])+','+\
                str(distance)+\
                '\n'
            )
