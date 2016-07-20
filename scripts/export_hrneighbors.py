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
out_file.write("time,mac,neighborMac,neighborFlag,rssi,numTxPackets,numTxFailures,numRxPackets,mote_board,ngbr_board,distance\n")
for obj in json_list:
    time                = tools.iso_to_epoch(obj["timestamp"])
    mote_lat, mote_long = tools.mac_to_position(obj["mac"],time)
    mote_board          = tools.mac_to_board(obj["mac"],time)

    if mote_board is None:
        mote_board = ""

    for key, nghbr in obj["value"]["neighbors"].iteritems():

        distance                = -1
        nghbr_mac, nghbr_board  = tools.id_to_mac(nghbr["neighborId"],time)
        nghbr_lat, nghbr_long   = tools.mac_to_position(nghbr_mac,time)
        if nghbr_lat is not None and mote_lat is not None:
            distance = tools.distance_on_unit_sphere(
                        mote_lat,
                        mote_long,
                        nghbr_lat,
                        nghbr_long
                    )

        if nghbr_board is None:
            nghbr_board = ""

        if nghbr_mac is not None:
            out_file.write(
                str(time)+','+\
                str(obj["mac"])+','+\
                str(nghbr_mac)+','+\
                str(nghbr["neighborFlag"])+','+\
                str(nghbr["rssi"])+','+\
                str(nghbr["numTxPackets"])+','+\
                str(nghbr["numTxFailures"])+','+\
                str(nghbr["numRxPackets"])+','+\
                mote_board+','+\
                nghbr_board+','+\
                str(distance)+\
                '\n'
            )
