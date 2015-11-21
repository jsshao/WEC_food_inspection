import pandas as pd
from geopy.geocoders import Nominatim
from multiprocessing.pool import ThreadPool as Pool


def process(inp):
    i, j = inp
    id = i[0]

    output = list(i)[1:]
    if len(i) > 4:
        try :
            geolocator = Nominatim()
            location = geolocator.geocode(i[3] + " " + i[4] + " Canada")
            output.append(location.latitude)
            output.append(location.longitude)
            output.append(j)
        except:
            pass
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
    return facility_interactions


def group_by_restaurants(df):
    groups = df.groupby("FACILITYID")
    restaurants = [g for g in groups]
    restaurants = sorted(restaurants, key=lambda g: len(g[1]), reverse=True)
    return restaurants


def load_data():
   facility_infractions = load_data_as_df()
   facility_infractions = facility_infractions.groupby(['FACILITYID', 'BUSINESS_NAME', 'TELEPHONE', 'ADDR', 'CITY',
       'OPEN_DATE', 'DESCRIPTION']).size()

    output = []
    l = []
    for i, j in facility_infractions.iteritems():
        l.append((i, j))

    p = Pool(100)
    data = p.map(process, l)
    return data

if __name__ == '__main__':
    load_data()
