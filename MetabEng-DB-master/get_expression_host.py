#from pdb id get known expression host
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

def get_unique_hosts(pdb_list):
    hosts_list = exp_hosts_loop(pdb_list)
    hosts_list = np.asarray(hosts_list)
    unique_hosts_list = get_unique_items(hosts_list)
    return unique_hosts_list

def get_exp_hosts(pdb_id):
    url = "https://www.rcsb.org/pdb/rest/customReport.xml?pdbids=" + pdb_id
    url = url + "&customReportColumns=expressionHost"
    response = requests.get(url)
    tsv_data = response.text
    data = re.split('\n|\t',tsv_data)
    d = np.asarray(data)
    query = '<dimEntity.expressionHost>'
    data_oi = [i for i in d if query in i]
    expression_hosts = get_org_from_data_loop(data_oi)
    exp_hosts = np.asarray(expression_hosts)
    expression_hosts = get_unique_items(exp_hosts)
    return expression_hosts

def get_org_from_data_loop(data_oi):
    expression_hosts = []
    for i in data_oi:
        split_data = re.split('<|>',i)
        exp_org = split_data[2]
        expression_hosts.append(exp_org)
    return expression_hosts
    
def exp_hosts_loop(pdb_list):
    hosts_list = []
    for i in pdb_list:
        current_pdb_id = i[0]
        current_hosts = get_exp_hosts(current_pdb_id)
        hosts_list.append(current_hosts)
    return hosts_list

def get_unique_items(array):
    #get unique items from np.array
    #two cases - length of 1, length of greater than 1
    unique_array = np.unique(array)
    len_unique_array = len(unique_array)
    unique_items = []
    if len_unique_array == 0:
        unique_items.append('None')
    elif len_unique_array ==1:
        unique_items.append(unique_array[0])
    else:
        unique_items = unique_loop(unique_array,len_unique_array,unique_items)
    return unique_items

def unique_loop(unique_array,len_unique_array,unique_items):
    for i in range(0,len_unique_array):
        print(i)
        current_item = unique_array[i]
        unique_items.append(current_item)
    return unique_items
                    
def hosts_uniprot_loop(uniprot_ids,pdb_dict):
    len_data = len(uniprot_ids)
    hosts_dict = {}
    for i in range(0,len_data):
        current_uniprot_id = uniprot_ids[i]
        print(i,current_uniprot_id)
        pdb_list = pdb_dict[current_uniprot_id]
        current_hosts = get_unique_hosts(pdb_list)
        hosts_dict[current_uniprot_id] = current_hosts
    return hosts_dict
        






