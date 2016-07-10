import flatdict
import time
import calendar
import csv

#-CONSTANTS-------------------------------------------------------------------#

MOTECREATE_PATH = "../data/motecreate.csv"

#-----------------------------------------------------------------------------#

def influxdb_to_json(sol_influxdb):
    """
    Converts an Influxdb query reply into a list of dicts.

    :param sol_influxdb dict: the result of a database query (sush as SELECT * FROM)
    :return: a list of JSON SOL objects
    :rtype: list

    """

    # verify influxdb data
    if not ("series" in sol_influxdb):
        raise ValueError("Influxdb data not recognized")

    # init
    json_list = []

    # remove unused headers
    for serie in sol_influxdb["series"]:
        for val in serie['values']:
            # convert to dict
            d_influxdb = dict(zip(serie['columns'], val))

            # remove null values
            #for key in obj.keys():
            #    if obj[key] is None:
            #        del(obj[key])

            # unflat dict
            obj_value = flatdict.FlatDict(d_influxdb).as_dict()

            # parse specific objects
            if serie['name'] == "SOL_TYPE_DUST_NOTIF_HRNEIGHBORS" :
                for i in range(0,len(obj_value["neighbors"])+1):
                    ngbr_id = str(i)

                    # new HR_NGBR parsing
                    if ngbr_id in obj_value["neighbors"]:
                        if obj_value["neighbors"][ngbr_id]["neighborFlag"] is None:
                            del obj_value["neighbors"][ngbr_id]

                    # old HR_NGBR parsing
                    if ngbr_id in obj_value:
                        if obj_value[ngbr_id]["neighborFlag"] is not None:
                            obj_value["neighbors"][ngbr_id] = obj_value[ngbr_id]
                        del obj_value[ngbr_id]

            # time is not passed in the "value" field
            del obj_value["time"]

            # create final dict
            jdic = {
                    'type'      : serie['name'],
                    'mac'       : serie['tags']['mac'],
                    'value'     : obj_value,
                    'timestamp' : d_influxdb['time'],
                    }
            json_list.append(jdic)
    return json_list

def iso_to_epoch(iso_time):
    return str(calendar.timegm(time.strptime(iso_time, '%Y-%m-%dT%H:%M:%SZ')))

def mac_to_id(mac, time):
    line = 1
    moteid = None
    with open(MOTECREATE_PATH) as csvfile:
        createmote_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        event_list = list(createmote_reader)

        while line < len(event_list):
            event = event_list[line]
            if int(event[0]) > time or line == len(event_list)-1:
                break
            if event[1] == mac:
                moteid = int(event[2])
            line += 1
    return moteid




