#create dictionary of kegg_ids,org_ids,genes to uniprot_ids

def make_dicts(uniprot_ids,kegg_ids,org_ids,genes):
    kegg_id_dict = {}
    org_id_dict = {}
    genes_dict = {}
    for i in range(0,len(uniprot_ids)):
        current_uniprot_id = uniprot_ids[i]
        current_kegg_id = kegg_ids[i]
        current_org_id = org_ids[i]
        current_genes = genes[i]
        kegg_id_dict[current_uniprot_id] = current_kegg_id
        org_id_dict[current_uniprot_id] = current_org_id
        genes_dict[current_uniprot_id] = current_genes
    return kegg_id_dict, org_id_dict, genes_dict
