import numpy as np
import pandas as pd


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
       'OPEN_DATE', 'DESCRIPTION']).agg({'count': [np.size]})


if __name__ == '__main__':
    load_data()