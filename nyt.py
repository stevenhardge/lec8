from datetime import datetime
from secrets import *
import requests

import requests
import json


CACHE_FNAME = 'cache_file_name.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}




# A helper function that accepts 2 parameters
# and returns a string that uniquely represents the request
# that could be made with this info (url + params)
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

MAX_STALENESS = 10
def is_fresh(cache_entry):
    now = datetime.now().timestamp()
    
    staleness = now - cache_entry['cache_timestamp']

    return staleness > MAX_STALENESS

def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        if is_fresh(CACHE_DICTION[unique_ident]) is False:
            print("Getting cached data...")
            return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        pass
    print("Making a request for new data...")
    # Make the request and cache the new data
    resp = requests.get(baseurl, params)
    CACHE_DICTION[unique_ident] = json.loads(resp.text)
    CACHE_DICTION[unique_ident]['cache_timestamp'] = datetime.now().timestamp()
    dumped_json_cache = json.dumps(CACHE_DICTION)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json_cache)
    fw.close() # Close the open file
    return CACHE_DICTION[unique_ident]

nyt_key = '88e78485f5d6461194318e31871f68df'

# gets stories from a particular section of NY times
def get_stories(section):
    baseurl = 'https://api.nytimes.com/svc/topstories/v2/'
    extendedurl = baseurl + section + '.json'
    params={'api-key': nyt_key}
    return make_request_using_cache(extendedurl, params)


def get_headlines(nyt_results_dict):
    results = nyt_results_dict['results']
    headlines = []
    for r in results:
        headlines.append(r['title'])
    return headlines




section = 'arts'
stories = get_stories(section)
# print(stories) # should print a big pile of json

headlines = get_headlines(stories)
# for h in headlines:
#     print(h)
