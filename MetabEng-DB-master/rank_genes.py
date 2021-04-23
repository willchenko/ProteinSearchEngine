#rank each gene

# basic outline
#PTM
#   No PTM's:+100
#   No Disulfide bonds: +50
#   No gly bonds: +50

#Kintetics:
#   Any info available: +50
#   kcat available: + (another) 50

#known expression host
#   same as input: +150
#   any: +75

#protein mw
#   smallest: +100
#   2nd: +75
#   3rd: +50
#   top 10: +25

def order_scores(uniprot_ids, ptm_summary_dict, kinetics_summary_dict, known_hosts_dict):
    scores_dict = scores_loop(uniprot_ids, ptm_summary_dict, kinetics_summary_dict, known_hosts_dict)
    ordered_scores_dict = sorted(scores_dict.items(), key=lambda x: x[1],reverse=True)
    return ordered_scores_dict

def scores_loop(uniprot_ids, ptm_summary_dict, kinetics_summary_dict, known_hosts_dict):
    scores_dict = {}
    for j in range(0,len(uniprot_ids)):
        current_uniprot_id = uniprot_ids[j]
        current_ptm_score = get_current_ptm_score(ptm_summary_dict,current_uniprot_id)
        current_kinetics_score = get_current_kinetics_score(kinetics_summary_dict,current_uniprot_id)
        current_hosts_score = get_current_hosts_score(known_hosts_dict,current_uniprot_id)
        current_score = current_ptm_score + current_kinetics_score + current_hosts_score
        scores_dict[current_uniprot_id] = current_score
    return scores_dict

def get_current_ptm_score(ptm_summary_dict,current_uniprot_id):
    current_sum = ptm_summary_dict[current_uniprot_id]
    total = current_sum[0]
    total_n = [int(i) for i in total.split() if i.isdigit()]
    total_n = total_n[0]
    dsb = current_sum[1]
    dsb_n = [int(i) for i in dsb.split() if i.isdigit()]
    dsb_n = dsb_n[0]
    gb = current_sum[2]
    gb_n = [int(i) for i in gb.split() if i.isdigit()]
    gb_n = gb_n[0]
    current_ptm_score = 0
    if total_n == 0:
        current_ptm_score = current_ptm_score + 100
    elif total_n > 0 and dsb_n == 0:
        current_ptm_score = current_ptm_score + 50
    elif total_n > 0 and gb_n ==0:
        current_ptm_score = current_ptm_score + 50
    else:
        current_ptm_score = current_ptm_score
    return current_ptm_score

def get_current_kinetics_score(kinetics_summary_dict,current_uniprot_id):
    current_sum = kinetics_summary_dict[current_uniprot_id]
    current_kinetics_score = 0
    if 'No experimental kinetic information available' in current_sum:
        current_kinetics_score = 0
    else:
        current_kinetics_score = 100
    return current_kinetics_score

def get_current_hosts_score(known_hosts_dict,current_uniprot_id):
    current_hosts = known_hosts_dict[current_uniprot_id]
    current_hosts_score = 0
    if 'None' in current_hosts[0]:
        current_hosts_score = 0
    else:
        current_hosts_score = 150
    return current_hosts_score