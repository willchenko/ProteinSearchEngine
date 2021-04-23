#input
import os
import pandas as pd
import numpy as np
#from GUI import my_form_post

#os.chdir(r"C:\Users\Owner\Documents\PhD_stuff\phd_classes\Fall_2019\bioinformatics\Project")
os.chdir(r"C:\Users\bradw\Documents\MetabEng-DB-master\MetabEng-DB-master")

enzyme_class = "3.4.13"

#enzyme_class = my_form_post()

#get genes
from get_genes import get_gene_data, split_clean_data, split_gene, new_index, init_matrix, clean_requests
import get_genes
[org_ids,genes,gene_names,kegg_ids] = get_genes.get_gene_data(enzyme_class)

#kegg to uniprot
from kegg_to_unitprot_id import kegg_to_uniprot_id, get_data, uniprot_id_loop
import kegg_to_unitprot_id
uniprot_ids = kegg_to_unitprot_id.uniprot_id_loop(kegg_ids)

#uniprot to pdb
from uniprot_to_pdb_id import get_pdb_ids, get_data, pdb_id_loop
import uniprot_to_pdb_id
pdb_dict = pdb_id_loop(uniprot_ids)

#uniprot ids to pdb ids to expression hosts
from get_expression_host import get_unique_hosts, get_exp_hosts, get_org_from_data_loop, exp_hosts_loop, get_unique_items, unique_loop, hosts_uniprot_loop
import get_expression_host
known_hosts_dict = hosts_uniprot_loop(uniprot_ids,pdb_dict)

#get kinetics
from get_kinetics import get_kinetics, new_index, init_matrix, clean_requests, kinetics_loop, get_kcat, get_ph_and_temp, get_summary_kinetics, get_kcat_summary  
import get_kinetics
[kinetics_dict,kinetics_summary_dict] = kinetics_loop(uniprot_ids)

#get PTM
from get_PTM import get_modifications, clean_the_data, init_matrix, ptm_loop
import get_PTM
[ptm_dict,ptm_summary_dict] = ptm_loop(uniprot_ids)

#get protein size
from get_protein_size import get_size, protein_size_loop
import get_protein_size
[length_dict, mw_dict] = protein_size_loop(uniprot_ids)

#get ranking
from rank_genes import order_scores, scores_loop, get_current_ptm_score, get_current_kinetics_score, get_current_hosts_score
import rank_genes
ordered_scores_dict = order_scores(uniprot_ids, ptm_summary_dict, kinetics_summary_dict, known_hosts_dict)

#make other dictionaries
from make_other_dicts import make_dicts
import make_other_dicts
[kegg_id_dict,org_id_dict,genes_dict] = make_dicts(uniprot_ids, kegg_ids, org_ids, genes)

raw_ec_dict = {
    "ec_number": enzyme_class,
    "genes": genes,
    "organism": org_ids,
    "kegg_ids": kegg_ids,
    "uniprot_ids": uniprot_ids,
    "pdb_ids": pdb_dict,
    "raw_kinetics": kinetics_dict,
    "kinetics_summary": kinetics_summary_dict,
    "known_expression_host": known_hosts_dict,
    "protein_length": length_dict,
    "protein_mw": mw_dict,
    "raw_ptm": ptm_dict,
    "ptm_summarry": ptm_summary_dict
    }

#Initialize and populate the table
mat = init_matrix(10,8)
cols = ['Genes', 'Organisms', 'Kegg Ids', 'Uniprot Ids', 'PTM Summaries', 'Kinetic Summaries', 'Protein Weights', 'Known Hosts']
for i in range(10):    
    mat[i][0] = genes_dict[ordered_scores_dict[i][0]]
    mat[i][1] = org_id_dict[ordered_scores_dict[i][0]]
    mat[i][2] = kegg_id_dict[ordered_scores_dict[i][0]]
    mat[i][3] = ordered_scores_dict[i][0]
    mat[i][4] = ptm_summary_dict[ordered_scores_dict[i][0]]
    mat[i][5] = kinetics_summary_dict[ordered_scores_dict[i][0]]
    mat[i][6] = mw_dict[ordered_scores_dict[i][0]]
    mat[i][7] = known_hosts_dict[ordered_scores_dict[i][0]]

mat = np.asarray(mat)
df = pd.DataFrame(mat, columns=cols)
pd.set_option('display.max_colwidth', -1)
html_table = df.to_html(classes=["table table-striped"])


