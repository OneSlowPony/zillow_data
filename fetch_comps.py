import requests
import pandas as pd
from xml.etree import ElementTree
import xmltodict
from bs4 import BeautifulSoup
import numpy as np
import urllib
import utils
import datetime
import csv
import os.path
os.path.isfile(fname)

##User specific ID used for IDing requests
zws_id = ''
##Address of property##
address = ''
##This one is intuitive
citystatezip = 'Washington-DC'
##Zillow ID for property. Get from URL in browswer
zpid = '491287'
##How any results
count = '25'

##Identifying info to base search on##
search_params = {'zws_id': zws_id, 'address': address,
                'citystatezip': citystatezip,
                'zpid': zpid, 'count': count}

##Tags to extract from respons##
search_tags = (('address'),
                ('zestimate','valuationRange','high'),
                ('zestimate','valuationRange','low'),
                ('zestimate', 'amount'))

comp_tags =  (('address'),
              ('zestimate','valuationRange','high'),
              ('zestimate','valuationRange','low'),
              ('zestimate', 'amount'))

##Colums for data##
home_cols = ['street', 'zipcode', 'city', 'state',
             'latitude', 'longitude', 'currency1',
             'valuation_high',  'currency2', 'valuation_low',
             'currency3' ,'zestimate', 'zpid']

comp_cols = ['city', 'latitude', 'longitude', 'state',
             'street', 'zipcode',  'valuation_high',
             'currency1', 'valuation_low', 'currency2',
             'zestimate', 'currency3', 'zpid']


##Get starting home data##
r = utils.get_response(api = 'search', params = search_params)

home = utils.parse_response(response = r,
                            api = 'search',
                            tags = search_tags,
                            cols = home_cols)


##Get Comps for original property
comp_response = utils.get_response(api = 'comp', params = search_params)

comps = utils.parse_response(response = comp_response,
                             api = 'comp',
                             tags = comp_tags,
                             cols = comp_cols)

##Cmobine data and write to csv
home = home[comp_cols]

data_list = [home,comps]
all_data = pd.concat(data_list)
all_data['record_date'] = datetime.datetime.now()
all_data.to_csv(path)


path = 'data/comps.csv'



all_data.to_csv(path)

all_data.keys()

if os.path.isfile(path):
    ##check for exising file
    existing_data = pd.read_csv(path)
    existing_data = existing_data.drop('Unnamed: 0', axis = 1)
    data_list = [all_data, existing_data]

    all_data = pd.concat(data_list, sort = 'FALSE')

all_data.to_csv(path)
