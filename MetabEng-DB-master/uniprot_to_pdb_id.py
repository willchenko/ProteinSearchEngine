#uniprot ids to pdb ids
import urllib
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

def get_pdb_ids(uniprot_id):
    url = "https://www.uniprot.org/uploadlists/"
    params = {
    "from": "ACC",
    "to": "PDB_ID",
    "format": "tab",
    "query": uniprot_id
        }
    data = urllib.parse.urlencode(params)
    data = data.encode("utf-8")
    req = urllib.request.Request(url, data)
    response = get_data(req)
    mapping = response.decode("utf-8")
    mapping_list = re.split('\n|\t',mapping)
    mapping_list.remove('')
    ml = np.asarray(mapping_list)
    ml = ml.reshape(-1,2)
    ml = np.delete(ml,0,1)
    pdb_ids = np.delete(ml,0,0)
    if pdb_ids.size == 0:
        ids = ['N/A']
        pdb_ids = np.asarray(ids)
    return pdb_ids
    
def get_data(req):
    with urllib.request.urlopen(req) as f:
       response = f.read()
    return response

def pdb_id_loop(uniprot_ids):
    len_data = len(uniprot_ids)
    pdb_dict = {}
    for i in range(0,len_data):
        current_uniprot_id = uniprot_ids[i]
        current_pdb_ids = get_pdb_ids(current_uniprot_id)
        pdb_dict[current_uniprot_id] = current_pdb_ids
    return pdb_dict




        
    
