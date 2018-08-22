import requests
import pandas as pd
from xml.etree import ElementTree
import xmltodict
from bs4 import BeautifulSoup
import numpy as np
import urllib

def get_attribute(api,data,tag):

    print(tag)

    if api == 'comp':

        if type(tag) == str:
            value = pd.DataFrame([dict(data[b][tag]) for b in range(len(data))])
            return value

        if len(tag) == 2:
            value = pd.DataFrame([dict(data[b][tag[0]][tag[1]]) for b in range(len(data))])
            return value

        if len(tag) == 3:
            value = pd.DataFrame([dict(data[b][tag[0]][tag[1]][tag[2]]) for b in range(len(data))])
            return value

    if api == 'search':

        if type(tag) == str:
            value = data[tag]
            return pd.DataFrame(value, index = [0])

        if len(tag) == 2:
            value =  pd.DataFrame(data[tag[0]][tag[1]], index = [0])
            return value

        if len(tag) == 3:
            value = pd.DataFrame(data[tag[0]][tag[1]][tag[2]], index = [0])
            return value


def get_response(api, params):

    print('Starting....')

    if api == 'search':
        print('Search API')

        base_url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
        url = base_url + 'zws-id='+params['zws_id']+'&address='+params['address']+'&citystatezip='+params['citystatezip']

    if api == 'comp':
        base_url = 'http://www.zillow.com/webservice/GetComps.htm?'
        url = base_url  +'zws-id='+params['zws_id']+'&zpid='+params['zpid']+'&count='+params['count']


    print(url)
    r = requests.get(url)

    return r

def parse_response(response, tags, cols, api):

    print('Parsing desired data from response.....')

    if api == 'search':

        cont = xmltodict.parse(response.content.decode('utf-8'))
        cont =  dict(cont.get('SearchResults:searchresults', None)['response']['results']['result'])
        search_dfs = [get_attribute(api = 'search', data = cont, tag = vals) for vals in tags]

        zpid = cont['zpid']

    if api == 'comp':

        cont = xmltodict.parse(response.content.decode('utf-8'))
        keys = cont.get('Comps:comps', None)['response']['properties']['comparables']['comp']
        search_dfs = [get_attribute(api = 'comp', data = keys, tag = vals) for vals in tags]

        ##THIS IS BROKEN--FIX
        zpid = [keys[b][tag] for b in range(len(keys))]


    print('Combining data frames')

    home_data =  pd.concat(search_dfs, axis = 1)

    home_cols = ['street', 'zipcode', 'city', 'state', 'latitude',
            'longitude', 'currency1', 'valuation_high',  'currency2',
            'valuation_low', 'currency3' ,'zestimate']

    print('Setting column names')

    home_data.columns = cols
    home_data['zpid'] = zpid

    return home_data
