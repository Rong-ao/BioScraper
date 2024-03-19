import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3

print('If this is the first time to use this program on your computer, I recommend you to check whether package "requests", "BeautifulSoup" and "pandas" were installed.\n\
      If not, run these commands to install:\n\
      pip install requests\n\
      pip install beautifulsoup4\n\
      pip install pandas\n\
      pip install urllib3\n\n')
print('Author: Rongao Kou, Westlake University (If any problem, please contact with kourongao@westlake.edu.cn)\n\n')


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
        print('No page found')

    return soup


def info_scraper(soup):
    print(type(soup))
    if soup.find('comment', {'type': 'subcellular location'}) is None:
        loc = ['Not found']
    else:
        loc = soup.find('comment', {'type': 'subcellular location'}).text
        loc = list(filter(None, loc.split('\n')))
        print(loc)
    return loc


def main(in_dir, out_dir, secret_protein='N'):
    df = pd.read_csv(in_dir, header=None)
    print(df)
    df.columns = ['Uniprot ID']
    l = []
    n = 0
    for i in df['Uniprot ID']:
        print('****************** Searching for Uniprot ID {}... [{}/{}] ******************'.format(i, str(n + 1), str(len(df))))
        request = get_protein_info(i)
        location = info_scraper(request)
        location = '|'.join(location)
        l.append(location)
        n += 1
    s = pd.Series(l, name='Subcellular location')
    df = pd.concat([df, s], axis=1)
    # df.columns = ['Uniprot ID', 'Subcellular location']
    df.to_csv(output + '_sub_loc.tsv', sep='\t')
    print('Your file has been stored in "{}"'.format(out_dir + '_sub_loc.tsv'))
    if secret_protein == 'Y':
        df_secret = df[df['Subcellular location'].str.contains('Secreted')]
        df_secret.to_csv(out_dir + '_secreted.csv', sep=',')
        print('Your secret protein file has been stored in "{}"'.format(out_dir + '_secreted.csv'))
    input('Press anything to exit')


filepath = input('Please input your Uniprot ID list file directory (csv format recommended): ')
output = input('Please input your output file directory (with output name you want): ')
secret = input('Do you want to select secreted proteins as an independent file? (Y/N): ')
main(filepath, output, secret)
