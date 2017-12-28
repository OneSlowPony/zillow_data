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

    if api == 'search':
        base_url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
        url = base_url + 'zws-id='+params['zws_id']+'&address='+params['address']+'&citystatezip='+params['citystatezip']

    if api == 'comp':
        base_url = 'http://www.zillow.com/webservice/GetComps.htm?'
        url = base_url  +'zws-id='+params['zws_id']+'&zpid='+params['zpid']+'&count='+params['count']

    r = requests.get(url)

    return r
