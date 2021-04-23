#get MW from unitprot_id 
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

def get_size(uniprot_id):
    base_url = "https://www.uniprot.org/uniprot/"
    url = base_url + uniprot_id + ".txt"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tsv_data = response.text
    data = re.split('\n|\t',tsv_data)
    seq_data = [i for i in data if 'SQ' in i[0:2]]
    if seq_data == []:
        protein_length = 'N/A'
        protein_mw = 'N/A'
    else:
        seq_data = seq_data[0]
        seq_data = re.split('  |;| ',seq_data)
        seq_clean = [ii for ii in seq_data if ii]
        protein_length = int(seq_clean[2])
        protein_mw = int(seq_clean[4])
    return protein_length, protein_mw 

def protein_size_loop(uniprot_ids):
    len_data = len(uniprot_ids)
    length_dict = {}
    mw_dict = {}
    for i in range(0,len_data):
        current_uniprot_id = uniprot_ids[i]
        current_size = get_size(current_uniprot_id)
        current_length = current_size[0]
        current_mw = current_size[1]
        length_dict[current_uniprot_id] = current_length
        mw_dict[current_uniprot_id] = current_mw
    return length_dict, mw_dict
        
