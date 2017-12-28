import requests
import pandas as pd
from xml.etree import ElementTree
import xmltodict
from bs4 import BeautifulSoup
import numpy as np


zws_id = ''
address = ''
citystatezip =''
zpid = ''
count = '25'



##GET HOME DATA##
search_params = {'zws_id': zws_id, 'address': address,
                'citystatezip': citystatezip,
                'zpid': zpid, 'count': count}

r = get_response(api = 'search', params = search_params)


cont = xmltodict.parse(r.content.decode('utf-8'))
cont =  dict(cont.get('SearchResults:searchresults', None)['response']['results']['result'])

search_tags = (('address'),
            ('zestimate','valuationRange','high'),
            ('zestimate','valuationRange','low'),
            ('zestimate', 'amount'))

search_dfs = [get_attribute(api = 'search', data = cont, tag = vals) for vals in search_tags]
home =  pd.concat(search_dfs, axis = 1)
home_cols = ['street', 'zipcode', 'city', 'state', 'latitude', 'longitude', 'currency1', 'valuation_high',  'currency2', 'valuation_low', 'currency3' ,'zestimate']
home.columns = home_cols
home['zpid'] = cont['zpid']

 ##GET COMPS##
comp_base = 'http://www.zillow.com/webservice/GetComps.htm?'

comp_url = comp_base +'&zws-id='+zws_id+'&zpid='+zpid+'&count='+count
comp_url
r = requests.get(comp_url)

cont = xmltodict.parse(r.content.decode('utf-8'))
keys = cont.get('Comps:comps', None)['response']['properties']['comparables']['comp']

tag_vals =  (('address'),
            ('zestimate','valuationRange','high'),
            ('zestimate','valuationRange','low'),
            ('zestimate', 'amount'))


sep_df = [get_attribute(api = 'comp', data = keys, tag = vals) for vals in tag_vals]

comp= pd.concat(sep_df, axis = 1)
comp['zpid'] = [keys[b][tag] for b in range(len(keys))]

comp_cols = ['city', 'latitude', 'longitude', 'state', 'street', 'zipcode', 'valuation_high', 'currency1', 'valuation_low', 'currency2', 'zestimate', 'currency3', 'zpid']

comp.columns = comp_cols

home = home[comp_cols]

data_list = [home,comp]
all_data = pd.concat(data_list)
