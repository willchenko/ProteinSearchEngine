import requests
import re
import numpy as np

def get_kinetics(uniprot_id):
    QUERY_URL = 'http://sabiork.h-its.org/sabioRestWebServices/kineticlawsExportTsv'
    # specify search fields and search terms
    query_dict = {"UniprotID":uniprot_id}
    query_string = ' AND '.join(['%s:%s' % (k,v) for k,v in query_dict.items()])
    # specify output fields and send request
    query = {'fields[]':['EntryID', 'Organism', 'UniprotID','ECNumber', 'Parameter','Temperature','pH'], 'q':query_string}
    request = requests.get(QUERY_URL, params = query)
    tsv_data = request.text
    data = re.split('\n|\t',tsv_data)
    d = np.asarray(data)
    if len(d) < 2:
        clean_data = ['No experimental kinetic information available']
    else: 
        clean_data = clean_requests(d)
        clean_data = np.vstack(clean_data)
    return clean_data

def new_index(i,ii,iii):
    n_cols = 12 # this is set for number of results from query (not 1:1 ratio)
    if i % n_cols == 0:
        ii = ii + 1
        iii = 0
    else:
        ii = ii
        iii = iii+1
    return ii,iii

def init_matrix(m, n):
    """Creates a m by n matrix filled with zeros."""
    return [[0]*n for i in range(m)]

def clean_requests(d):
    ii = 0
    iii = 0
    n_cols = 12 # this is set for number of results from query (not 1:1 ratio)
    n_rows = int((len(d)-1)/n_cols)
    clean_data = init_matrix(n_rows,n_cols)
    clean_data[ii][iii] = d[0]
    for i in range(1,len(d)-1):
        c_val = d[i]
        [ii,iii] = new_index(i,ii,iii)
        clean_data[ii][iii] = c_val
    return clean_data
    
def kinetics_loop(uniprot_ids):
    len_data = len(uniprot_ids)
    kinetics_dict = {}
    kinetics_summary_dict = {}
    for i in range(0,len_data):
        current_uniprot_id = uniprot_ids[i]
        current_kinetics = get_kinetics(current_uniprot_id)
        current_summary = get_summary_kinetics(current_kinetics)
        kinetics_dict[current_uniprot_id] = current_kinetics
        kinetics_summary_dict[current_uniprot_id] = current_summary
    return kinetics_dict, kinetics_summary_dict

def get_ph_and_temp(current_kinetics,n_entries):
    ph_list = []
    temp_list = []
    for j in range(1,n_entries):
        c_temp = current_kinetics[j][10]
        c_ph = current_kinetics[j][11]
        ph_list.append(c_ph)
        temp_list.append(c_temp)
    return temp_list, ph_list
    
def get_kcat(current_kinetics,n_entries): 
    types = [j[4] for j in current_kinetics]
    kcat_array = []
    for j in range(1,5):
        if 'kcat' in types[j] and 'Km' not in types[j]:
            current_start = current_kinetics[j][6]
            current_end = current_kinetics[j][7]
            kcat_array.append(current_start)
            kcat_array.append(current_end)
    return kcat_array

def get_summary_kinetics(current_kinetics):
    if 'No experimental kinetic information available' in current_kinetics[0]:
        current_summary = current_kinetics
    else:
        n_entries = len(current_kinetics)
        [temp_list,ph_list] = get_ph_and_temp(current_kinetics,n_entries)
        temp_list = [x for x in temp_list if x]
        ph_list = [x for x in ph_list if x]
        temp_list = [float(x) for x in temp_list]
        ph_list = [float(x) for x in ph_list]
        max_temp = max(temp_list)
        min_temp = min(temp_list)
        max_ph = max(ph_list)
        min_ph = min(ph_list)
        kcat_array = get_kcat(current_kinetics,n_entries)
        kcat_array = [x for x in kcat_array if x] #remove empty strings
        kcat_summary = get_kcat_summary(kcat_array)
        current_summary = [str(n_entries)+' total entries','Temperature Range: '+str(min_temp)+'-'+str(max_temp),kcat_summary]
    return current_summary
    
def get_kcat_summary(kcat_array):
    if kcat_array == []:
        kcat_summary = 'No kcat measurements'
    else:
        kcat_array = [float(x) for x in kcat_array] #turn strings to numbers
        min_kcat = min(kcat_array)
        max_kcat = max(kcat_array)
        kcat_summary = 'kcat range: '+str(min_kcat)+'-'+str(max_kcat)
    return kcat_summary
