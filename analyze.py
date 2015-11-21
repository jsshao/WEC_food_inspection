import copy

import pandas as pd
from geopy.geocoders import GoogleV3
from multiprocessing.pool import ThreadPool as Pool
import pickle
import os.path

cache = {}


def process(inp):
    i, j = inp
    id = i[0]

    output = {}
    global cache

    try:
        output["id"] = i[0]
        output["name"] = i[1]
        output["phone"] = i[2]
        output["addr"] = i[3]
        output["city"] = i[4]
        output["open_date"] = i[5]
        output["type"] = i[6]

        address = i[3] + " " + i[4] + " Canada"
        if address in cache:
            output["latitude"] = cache[address][0]
            output["longitude"] = cache[address][1]
        else:
            geolocator = GoogleV3()
            location = geolocator.geocode(address)
            output["latitude"] = (location.latitude)
            output["longitude"] = (location.longitude)
            cache[address] = (location.latitude, location.longitude)
    except Exception as e:
        print e

    output["infractions"] = j
    return output


def load_data_as_df():
    inspections = pd.read_csv('assets/Inspections_OpenData.csv')
    infractions = pd.read_csv('assets/Infractions_OpenData.csv')
    facilities = pd.read_csv('assets/Facilities_OpenData.csv')

    inspections = inspections[['INSPECTION_ID', 'FACILITYID']]
    infractions = infractions[['INSPECTION_ID', 'INFRACTION_TYPE', 'category_code', 'InspectionDate']]
    infractions = infractions[infractions.INFRACTION_TYPE != 'FSP']

    facility_inspections = pd.merge(facilities, inspections, on=['FACILITYID'])
    facility_infractions = pd.merge(facility_inspections, infractions, on=['INSPECTION_ID'])
    return facility_infractions


def filter_by_year(df, start=None, end=None):
    new_df = copy.deepcopy(df)
    if start:
        new_df = df[df['InspectionDate' >= str(start)]]

    if end:
        new_df = df[df['InspectionDate' >= str(end)]]

    return new_df


def group_by_restaurants(df, top=None):
    groups = df.groupby("FACILITYID")
    restaurants = [g for g in groups]
    restaurants = sorted(restaurants, key=lambda g: len(g[1]), reverse=True)

    return restaurants


def get_infractions_for_restaurant(df, rid):
    restaurant = df[df['FACILITYID'] == rid]
    infractions = restaurant.T.to_dict().values()
    return infractions


def load_data():
    global cache
    print "begin loading data!"
    if os.path.isfile('cache.txt'):
        with open ('cache.txt', 'rb') as f:
            cache = pickle.load(f)
        print "loaded cache, size %d" % len(cache)

    facility_infractions = load_data_as_df()
    facility_infractions = facility_infractions.groupby(['FACILITYID', 'BUSINESS_NAME', 'TELEPHONE', 'ADDR', 'CITY',
       'OPEN_DATE', 'DESCRIPTION']).size()

    output = []
    l = []
    for i, j in facility_infractions.iteritems():
        l.append((i, j))


    p = Pool(2)
    data = p.map(process, l)

    with open ('cache.txt', 'wb') as f:
        pickle.dump(cache, f)

    return data

if __name__ == '__main__':
    load_data()
