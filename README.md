# Uniprot Scraper

This script is a scraper to scrape protein informations from Uniprot database.

Usage: directly running this script with Python3 (dependences: pandas, requests, BeautifulSoup & lxml parser, urllib3)

Before running this scraper, check whether your environment satisfied dependences.

## Version 1.0: searching for protein subcellular loaction & secreted protein selection.

Version 1.0 accepts 3 arguments: 
### 1. Input file: Input directory of your ID file, which is a column list of protein Uniprot IDs, csv format recommended.

    (e.g. D:\Users\work_dir\test.csv)
   
### 2. Output file: Output directory of output file (csv format) containing Uniprot IDs and corresponding subcelluar location.
   NO filename extension is fine and recommended, output filename will end with 'sub_loc.csv' automatically.

    (e.g. D:\Users\work_dir\out_test  --->  D:\Users\work_dir\out_test_sub_loc.tsv)
   
### 3. Secreted protein selection: Accept Uppercase 'Y' or 'N', corresponding to select secreted protein as a seperated file 'xxx_secreted.csv'
   
   'xxx' is same as output name in 2

Thanks Yusong Zhang from Shandong University for asking me for develop this tool.

For more requirements and information worth, I will keep to update this scraper.

If any issue, please contact with kourongao@westlake.edu.cn
