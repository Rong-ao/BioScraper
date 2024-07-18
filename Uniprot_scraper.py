import time

print('If this is the first time to use this program on your computer, I recommend you to check whether package "requests", "BeautifulSoup" and "pandas" were installed.\n\
      If not, run these commands to install:\n\
      pip install requests\n\
      pip install beautifulsoup4\n\
      pip install lxml\n\
      pip install pandas\n\
      pip install urllib3\n\n')
print('Author: Rongao Kou, Westlake University (If any problem, please check https://github.com/Rong-ao/Uniprot-scraper)\n\n')
print('If there are not requested packages above on your computer, it will close automatically in 15 seconds.')
time.sleep(15)

import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
import openpyxl
import re



# Written for writer: Uniprot provides specific API for batch search, check link below
# For more help, see https://www.uniprot.org/help/api


def get_protein_info(pro_id):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
              'Upgrade-Insecure-Requests': '1'}
    try:
        url = 'https://rest.uniprot.org/uniprotkb/{}?format=xml'.format(pro_id)  # (www is not available)
        s = requests.session()
        requests.packages.urllib3.disable_warnings()  # Ignore warning from urllib3 (without certificate)
        r = s.get(url, headers=header, verify=False, timeout=30)
        # print(r.status_code)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
    except:
        soup = BeautifulSoup("", 'xml')
        print('No page found')
    return soup
        
    
def uniprot_annotation_scraper(soup):
    if soup.find('comment', {'type': 'subcellular location'}) is None:
        loc = ['Not found Uniprot Annotation']
    else:
        loc = soup.find('comment', {'type': 'subcellular location'}).text
        loc = list(filter(None, loc.split('\n')))
        print('Uniprot annotation:')
        print(loc)
    return loc

def go_cc_scraper(soup):
    loc = soup.find_all('property', {'type': 'term', 'value':re.compile('C:')})
    loc = [x.attrs['value'][2:] for x in loc]
    print('GO Cellular Component term:')
    print(loc)
    return loc

def main(in_dir, out_dir, secret_protein='N'):
    if in_dir.endswith('xlsx') or in_dir.endswith('xls'):
        df = pd.read_excel(io=in_dir, header=None, index_col=None)
    elif in_dir.endswith('csv'):
        df = pd.read_csv(in_dir, header=None, index_col=None)
    print(df)
    df.columns = ['Uniprot ID']
    uni_l = []
    go_l = []
    n = 0
    for i in df['Uniprot ID']:
        print('****************** Searching for Uniprot ID {}... [{}/{}] ******************'.format(i, str(n + 1), str(len(df))))
        request = get_protein_info(i)
        uni_location = uniprot_annotation_scraper(request)
        go_location = go_cc_scraper(request)
        uni_location = '|'.join(uni_location)
        go_location = '|'.join(go_location)
        uni_l.append(uni_location)
        go_l.append(go_location)
        n += 1
    uni_s = pd.Series(uni_l, name='Uniprot Subcellular Location')
    go_s = pd.Series(go_l, name='Gene Ontology (Cellular Component)')
    df = pd.concat([df, uni_s, go_s], axis=1)
    # df.columns = ['Uniprot ID', 'Subcellular location', 'Gene Ontology']
    df.to_csv(out_dir + '_sub_loc.tsv', sep='\t')
    print('Your file has been stored in "{}"'.format(out_dir + '_sub_loc.csv'))
    if secret_protein == 'Y':
        df_secret = df[(df['Uniprot Subcellular Location'].str.contains('Secreted')) | (df['Gene Ontology (Cellular Component)'].str.contains('extracellular'))]
        df_secret.to_csv(out_dir + '_secreted.csv', sep='\t')
        print('Your secret protein file has been stored in "{}"'.format(out_dir + '_secreted.csv'))
    input('Press anything to exit')


filepath = input('Please input your Uniprot ID list file directory (csv format recommended, e.g. D:\\Users\\work_dir\\test.csv): ')
output = input('Please input your output file directory (with output name you want, e.g. D:\\Users\\work_dir\\out_test):')
secret = input('Do you want to select secreted proteins as an independent file? (Y/N): ')
main(filepath, output, secret)
