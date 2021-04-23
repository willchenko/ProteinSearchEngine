import requests
import urllib.request
import time
from bs4 import BeautifulSoup

reaction = 'Sucrose + H2O = Glucose + Fructose'
enzyme_class = get_enzyme_class(reaction)


def get_enzyme_class(reaction):
    reaction_url = get_rxn_url(reaction)
    url_base = 'http://equilibrator.weizmann.ac.il/search?query='
    url = url_base + reaction_url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, “html.parser”)
    s = soup.find_all('div')
    p = soup.find('<td><strong>Catalyzed by</strong></td>')
    st = soup.find_all(string='Catalyzed by')
    td = st[0].findParent().findParent().findNextSibling()
    l = list(td.children)
    new_list = remove_blank_lines(l)
    enzyme_class = []
    for y in new_list:
        str_y = soup_to_string(y)
        start = str_y.find('[') + 4
        end = str_y.find(']')
        ec = str_y[start:end]
        enzyme_class.append(ec)
    return enzyme_class
    
def soup_to_string(soup):
    string = ''
    for x in soup:
        string = string + str(x)
    return string
        
def remove_blank_lines(old_list):
    new_list = []
    for s in old_list:
        if s != '\n':
            ns = s
            new_list.append(ns)
    return new_list

def get_url_char(letter):
    if letter == '+':
        nl = '+%2B+'
    elif letter == '=':
        nl = '+%3D+'
    elif letter == ' ':
        nl = ''
    else:
        nl = letter
    return nl

def get_rxn_url(reaction):
    reaction_url =''
    for letter in reaction:
        nl = get_url_char(letter)
        reaction_url = reaction_url + nl
    return reaction_url




        
