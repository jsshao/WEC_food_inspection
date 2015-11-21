import pandas as pd
from geopy.geocoders import Nominatim


def load_data():
    inspections = pd.read_csv('assets/Inspections_OpenData.csv')
    infractions = pd.read_csv('assets/Infractions_OpenData.csv')
    facilities = pd.read_csv('assets/Facilities_OpenData.csv')

    inspections = inspections[['INSPECTION_ID', 'FACILITYID']]
    infractions = infractions[['INSPECTION_ID', 'INFRACTION_TYPE', 'category_code', 'InspectionDate']]
    infractions = infractions[infractions.INFRACTION_TYPE != 'FSP']

    facility_inspections = pd.merge(facilities, inspections, on=['FACILITYID'])
    facility_infractions = pd.merge(facility_inspections, infractions, on=['INSPECTION_ID'])

    facility_infractions.groupby(['FACILITYID', 'BUSINESS_NAME', 'TELEPHONE', 'ADDR', 'CITY',
       'OPEN_DATE', 'DESCRIPTION']).size()

    output = {}
    geolocator = Nominatim()
    for i, j in facility_infractions.iteritems():
        id = i[0]
        output[id] = list(i)[1:]
        location = geolocator.geocode(i[3] + " " + i[4])
        output[id].append(location.latitude)
        output[id].append(lcation.longitude)

    print output


if __name__ == '__main__':
    load_data()
