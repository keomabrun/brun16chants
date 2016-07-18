import flatdict
import time
import calendar
import csv
import math

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
    return calendar.timegm(time.strptime(iso_time, '%Y-%m-%dT%H:%M:%SZ'))

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

def id_to_mac(mote_id, time):
    line = 1
    mote_mac = None
    with open(MOTECREATE_PATH) as csvfile:
        createmote_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        event_list = list(createmote_reader)[1:]

        for event in reversed(event_list):
            if int(event[2]) == mote_id:
                if int(event[0]) < time:
                    mote_mac = event[1]
                    break
    return mote_mac

def distance_on_unit_sphere(lat1, long1, lat2, long2):
    """
    Code from John Cook.
    http://www.johndcook.com/blog/python_longitude_latitude/
    """

    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
        math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc*6371*1000 # in meters



