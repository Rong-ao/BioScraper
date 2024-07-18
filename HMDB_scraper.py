import time

print('If this is the first time to use this program on your computer, I recommend you to check whether package "requests", "BeautifulSoup" and "pandas" were installed.\n\
      If not, run these commands to install:\n\
      pip install requests\n\
      pip install beautifulsoup4\n\
      pip install lxml\n\
      pip install pandas\n\
      pip install urllib3\n\n')
print('Author: Rongao Kou, Westlake University (If any problem, please check https://github.com/Rong-ao/BioScraper)\n\n')
print('If there are not requested packages above on your computer, it will close automatically in 10 seconds.')
time.sleep(10)

import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib3
import json

# For more help, see https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
              'Upgrade-Insecure-Requests': '1'}


def CAS_to_CID(cas):
    try:
        url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/cids/JSON".format(cas)
        s = requests.session()
        requests.packages.urllib3.disable_warnings()
        r = s.get(url, headers=header, verify=False, timeout=60)
        j = json.loads(r.text)
        cid = j['IdentifierList']['CID'][0]
    except:
        cid = None

    return cid


def CID_to_HMDB(cid):
    try:
        url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{}/JSON/?heading=Human+Metabolite+Information".format(cid)
        # URL here is obtained by these steps:
        # 1. Find section "Human Metabolite Information" in https://pubchem.ncbi.nlm.nih.gov/compound/133402/ by Browser
        # 2. Click Full Screen bottom, press F12 to open console 
        # 3. Fresh the page and check items in "Network"
        # 4. Open the item with "?heading..." in its name
        s = requests.session()
        requests.packages.urllib3.disable_warnings()
        r = s.get(url, headers=header, verify=False, timeout=60)
        j = json.loads(r.text)
        hmdb = j['Record']['Reference'][0]['URL']
    except:
        hmdb = None

    return hmdb


def info_scraper(HMDB):
    try:
        url = HMDB
        s = requests.session()
        requests.packages.urllib3.disable_warnings()
        r = s.get(url, headers=header, verify=False, timeout=60)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, 'html.parser')
        description = soup.find('td', {'class':"met-desc"})
        description = description.contents[0]
        description = description[:description.find('(PMID')]
    except:
        description = 'Not found related information in HMDB'

    return description
    

def integrate(in_dir, sheet_number=0):
    if in_dir.endswith('xlsx') or in_dir.endswith('xls'):
        df = pd.read_excel(io=in_dir, header=0, index_col=None, sheet_name=sheet_number)
    elif in_dir.endswith('csv'):
        df = pd.read_csv(in_dir, header=0, index_col=None)
    print(df)
    l = []
    link = []
    for cas in df['CAS']:
        print("****************** Searching for CAS ID: {} ******************".format(cas))
        if pd.isna(cas) == True:
            info = 'No CAS ID'
            link_site = None
        else:
            cid = CAS_to_CID(cas)
            if cid == None:
                link_site = None
                info = "CID Not found"
            else:
                hmdb = CID_to_HMDB(cid)
                if hmdb == None:
                    link_site = 'https://pubchem.ncbi.nlm.nih.gov/compound/{}'.format(cid)
                    info = "CID: {}, but HMDBID Not found".format(cid)
                else:
                    # print(hmdb)
                    link_site = hmdb
                    info = info_scraper(hmdb)
        print(info)
        l.append(info)
        link.append('=HYPERLINK("{}", "{}")'.format(link_site, link_site))
    s = pd.Series(l, name='Description(HMDB)')
    s2 = pd.Series(link, name='Hyperlink')
    df = pd.concat([df, s, s2], axis=1)
    print(df)

    return df

def main():
    print('This scraper is used for searching for metabolite information from PubChem (https://pubchem.ncbi.nlm.nih.gov/) and HMDB (https://hmdb.ca/) according to CAS ID.')
    filepath = input('Please input your list file directory of metabolites (csv or xlsx format recommended, e.g. D:\\Users\\work_dir\\test.csv): ')
    output = input('Please input your output file directory (with output name you want, e.g. D:\\Users\\work_dir\\out_test): ')
    if filepath.endswith('xlsx') or filepath.endswith('xls'):
        sheet = input('Which sheet do you want to search for? \n\
                      You can:\n\
                      Enter the number or sheet name, e.g. 0 OR Sheet1 for the first sheet\n\
                      Or press Enter for all sheets\n')
        excel = pd.ExcelFile(filepath)
        with pd.ExcelWriter(output + '.xlsx') as writer:
            if sheet == '':
                sheet_list = excel.sheet_names
            else:
                if sheet.isdigit():
                    sheet_list = [excel.sheet_names[sheet-1]]
                else:
                    sheet_list = [sheet]
            for i in sheet_list:
                print("****************** Proceeding Excel Sheet: {}... ******************".format(i))
                df = integrate(filepath, i)
                df.to_excel(writer, sheet_name=i, index=False)
    elif filepath.endswith('csv'):
        df = integrate(filepath, sheet)
        df.to_csv(output + '.csv', sep='\t', encoding='utf-8-sig')
    else:
        print('Wrong File Format Received! Please check your input file format or spelling.')


main()
input('Press anything to exit')