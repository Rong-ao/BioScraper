import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib3
import json

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
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            description = soup.find('td', {'class':"met-desc"})
            description = description.contents[0]
            description = description[:description.find('(PMID')]
    except:
        description = 'Not found related information in HMDB'

    return description
    

def integrate(in_dir, out_dir, sheet_number=0):
    if in_dir.endswith('xlsx') or in_dir.endswith('xls'):
        df = pd.read_excel(io=in_dir, header=0, index_col=None, sheet_name=sheet_number)
        file_type = 'excel'
    elif in_dir.endswith('csv'):
        df = pd.read_csv(in_dir, header=0, index_col=None)
        file_type = 'csv'
    print(df)
    l = []
    link = []
    for cas in df['CAS']:
        print("Searching for CAS ID: {}".format(cas))
        if pd.isna(cas) == True:
            info = None
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
                    print(hmdb)
                    link_site = hmdb
                    info = info_scraper(hmdb)
        print(info)
        l.append(info)
        link.append('=HYPERLINK("{}", "{}")'.format(link_site, link_site))
    s = pd.Series(l, name='Description(HMDB)')
    print(s)
    s2 = pd.Series(link, name='Hyperlink')
    print(s2)
    df = pd.concat([df, s, s2], axis=1)
    print(df)
    df.to_csv(out_dir + '.csv', sep='\t', encoding='utf-8-sig')
    

    return

def main():
    filepath = input('Please input your list file directory of metabolites (csv or xlsx format recommended, e.g. D:\\Users\\work_dir\\test.csv): ')
    output = input('Please input your output file directory (with output name you want, e.g. D:\\Users\\work_dir\\out_test):')
    if filepath.endswith('xlsx') or filepath.endswith('xls'):
        sheet = input('Which sheet do you want to search for? (enter the number or sheet name, e.g. 0 OR Sheet1, or press Enter for all sheets)')
        if sheet == '\n':
            sheet = None
            
            df = pd.read_csv(output + '.csv', header=0, index_col=None, sep='\t')
            with pd.ExcelWriter(output + '.xlsx') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
            os.remove(output + '.csv')
        else:
            integrate(filepath, output, sheet)

main()
# main(in_dir="C:\\Users\\DELL\\Desktop\\化合物询价.xlsx", out_dir="C:\\Users\\DELL\\Desktop\\化合物询价_sheet1", sheet_number=0)

# main(in_dir="C:\\Users\\DELL\\Desktop\\化合物询价.xlsx", out_dir="C:\\Users\\DELL\\Desktop\\化合物询价_sheet2", sheet_number=1)

# df1 = pd.read_csv("C:\\Users\\DELL\\Desktop\\化合物询价_sheet1.csv", header=0, index_col=None, sep='\t')
# df2 = pd.read_csv("C:\\Users\\DELL\\Desktop\\化合物询价_sheet2.csv", header=0, index_col=None, sep='\t')
# print(df1)
# print(df2)
# with pd.ExcelWriter('C:\\Users\\DELL\\Desktop\\化合物询价_HMDB.xlsx') as writer:
#     df1.to_excel(writer, sheet_name='Sheet1', index=False)
#     df2.to_excel(writer, sheet_name='Sheet2', index=False)