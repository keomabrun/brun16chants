import Sol
import json
import influxdb
import flatdict

###############################################################################
# Convert a InfluxDB dump of DUST measurments to a list of JSON objects.
###############################################################################


sol = Sol.Sol()

# open output file
out_file    = open('../data/objects.json','w')

# configure influxDB
influxClient    = influxdb.client.InfluxDBClient(
        host        = 'localhost',
        port        = '8086',
        database    = 'realms'
)

# query influxDB
query       =   "SELECT * FROM SOL_TYPE_DUST_SNAPSHOT"
query       +=  " WHERE time > '2016-04-20T00:00:00Z' AND site='ARG_junin'"
query       +=  " GROUP BY mac"
json_list   = influxClient.query(query).get_points()

# write json to file
for obj in json_list:
    # remove null values
    for key in obj.keys():
        if obj[key] is None:
            del(obj[key])

    # unflat dict
    obj_value = flatdict.FlatDict(obj).as_dict()

    # write to file
    out_file.write(json.dumps(obj_value)+'\n')
