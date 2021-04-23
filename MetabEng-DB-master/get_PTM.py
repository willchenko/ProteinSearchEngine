#get Post Translational Modifications and sequences from unitprot_id
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

def get_modifications(uniprot_id):
    base_url = "https://www.uniprot.org/uniprot/"
    url = base_url + uniprot_id + ".txt"
    response = requests.get(url)
    tsv_data = response.text
    data = re.split('\n|\t',tsv_data)
    ptm_data = [i for i in data if 'FT' in i[0:2]]
    if len(ptm_data) < 2:
        ptm = ['No PTM']
    else:
        clean_ptm = clean_the_data(ptm_data)
        clean_ptm = np.asarray(clean_ptm)
        n_cols = 4
        len_data = len(clean_ptm)
        clean_ptm = clean_ptm.reshape(int(len_data/n_cols),-1)
        ptm = np.vstack(clean_ptm)
    return ptm
    
def clean_the_data(ptm_data):
    clean_ptm = []
    for i in range(0,int(len(ptm_data))-1):
        current_ptm = ptm_data[i]
        i_split = re.split('  ', current_ptm)
        i_clean = [ii for ii in i_split if ii]
        if len(i_clean) > 3:
            ptm_type = i_clean[1]
            ptm_start = i_clean[2]
            ptm_stop = i_clean[3]
            ptm_description = i_clean[4]
            clean_ptm.append(ptm_type)
            clean_ptm.append(ptm_start)
            clean_ptm.append(ptm_stop)
            clean_ptm.append(ptm_description)
    return clean_ptm
        
def init_matrix(m, n):
    """Creates a m by n matrix filled with zeros."""
    return [[0]*n for i in range(m)]

def ptm_loop(uniprot_ids):
    len_data = len(uniprot_ids)
    ptm_dict = {}
    ptm_summary_dict = {}
    for i in range(0,len_data):
        current_uniprot_id = uniprot_ids[i]
        current_ptm = get_modifications(current_uniprot_id)
        n_mods = get_number_of_mod(current_ptm)
        types = [i[0] for i in current_ptm]
        disulf_bonds = [i for i in types if 'DISULFID' in i]
        gly_bonds = [i for i in types if 'CARBOHYD' in i]
        n_dsb = len(disulf_bonds)
        n_gly = len(gly_bonds)
        current_summary = str(n_mods) + ' total modifications', str(n_dsb) + ' disulfide bonds', str(n_gly) + ' glycosylation modification'
        ptm_summary_dict[current_uniprot_id] = current_summary
        ptm_dict[current_uniprot_id] = current_ptm
    return ptm_dict, ptm_summary_dict


def get_number_of_mod(current_ptm):
    if 'No PTM' in current_ptm[0]:
        n_mods = 0
    else:
        n_mods = len(current_ptm)
    return n_mods
        





