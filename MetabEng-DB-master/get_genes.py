import requests
from bs4 import BeautifulSoup
import re
import numpy as np

def get_gene_data(enzyme):
    base = "http://rest.kegg.jp/find/genes/"
    url = base + enzyme
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tsv_data = response.text
    data = re.split('\n|\t',tsv_data)
    d = np.asarray(data)
    clean_data = clean_requests(d)
    clean_data = np.vstack(clean_data)
    gene_data = split_clean_data(clean_data)
    gene_data = np.asarray(gene_data)
    org_ids = gene_data[:,0]
    genes = gene_data[:,2]
    gene_names = gene_data[:,3]
    kegg_ids = gene_data[:,4]
    return org_ids, genes, gene_names, kegg_ids

def split_clean_data(clean_data):
    [n_genes,c] = clean_data.shape
    gene_data = init_matrix(n_genes,5)
    for i in range(0,n_genes):
        i_org = clean_data[i][0]
        i_gene = clean_data[i][1]
        i_split_org = i_org.split(':')
        i_split_gene = i_gene.split(';')
        kegg_id = i_org
        org_id = i_split_org[0]
        kegg_gene_id = i_split_org[1]
        [gene_id,gene_name] = split_gene(i_split_gene)
        gene_data[i][0] = org_id
        gene_data[i][1] = kegg_gene_id
        gene_data[i][2] = gene_id
        gene_data[i][3] = gene_name
        gene_data[i][4] = kegg_id
    return gene_data

def split_gene(i_split_gene):
    if len(i_split_gene) == 1:
        gene_id = ''
        gene_name = i_split_gene[0]
    else: 
        gene_id = i_split_gene[0]
        gene_name = i_split_gene[1]
    return gene_id, gene_name

def new_index(i,ii,iii,n_cols):
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
    n_cols = 2
    n_rows = int((len(d)-1)/n_cols)
    ii = 0
    iii = 0
    clean_data = init_matrix(n_rows,n_cols)
    clean_data[ii][iii] = d[0]
    for i in range(1,len(d)-1):
        c_val = d[i]
        [ii,iii] = new_index(i,ii,iii,n_cols)
        clean_data[ii][iii] = c_val
    return clean_data


