import urllib
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

def kegg_to_uniprot_id(kegg_id):
    url = "https://www.uniprot.org/uploadlists/"
    params = {
    "from": "KEGG_ID",
    "to": "ACC",
    "format": "tab",
    "query": kegg_id
    }
    data = urllib.parse.urlencode(params)
    data = data.encode("utf-8")
    req = urllib.request.Request(url, data)
    response = get_data(req)
    mapping = response.decode("utf-8")
    mapping_list = re.split('\n|\t',mapping)
    if len(mapping_list) < 4:
        uniprot_id = 'N/A'
    else:
        uniprot_id = mapping_list[3]
    return uniprot_id 

def get_data(req):
    with urllib.request.urlopen(req) as f:
       response = f.read()
    return response

def uniprot_id_loop(kegg_ids):
    len_data = len(kegg_ids)
    uniprot_ids = []
    for i in range(0,10):
#        print(i)
        current_kegg_id = kegg_ids[i]
        uniprot_id = kegg_to_uniprot_id(current_kegg_id)
        uniprot_ids.append(uniprot_id)
    return uniprot_ids
