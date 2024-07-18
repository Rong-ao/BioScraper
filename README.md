# **BioScraper**
- [Uniprot Scraper](#uniprot-scraper)
- [HMDB Scraper](#hmdb-scraper)

These scripts are scrapers to scrape substance informations from biomedical databases.

Running: directly running this script with Python3 (dependences: pandas, requests, BeautifulSoup & lxml parser, urllib3)

Before running scraper, check whether your environment satisfied dependences.

# Uniprot Scraper
Version 1.0: searching for protein subcellular loaction & secreted protein selection.

### Uniprot Scraper accepts 3 arguments: 
### 1. Input file: Input directory of your ID file, which is a column list of protein Uniprot IDs, csv or xlsx format recommended.

`e.g. D:\Users\work_dir\test.csv`
   
### 2. Output file: Output directory of output file (csv format) containing Uniprot IDs and corresponding subcelluar location.
   NO filename extension is fine and recommended, output filename will end with `sub_loc.csv` automatically.

`e.g. D:\Users\work_dir\out_test  --->  D:\Users\work_dir\out_test_sub_loc.tsv`
   
### 3. Secreted protein selection: 
Accept Uppercase `Y` or `N`, corresponding to select secreted protein as a seperated file `xxx_secreted.csv`, `xxx` is same as output name in 2
   
# HMDB Scraper
Version 1.0: searching for description of metabolite in HMDB according to CAS ID.
### HMDB Scraper accepts 3 arguments: 
### 1. Input file: same as Uniprot Scraper

`e.g. D:\Users\work_dir\test.csv`
   
### 2. Output file: Output directory of output file (csv format) containing CAS IDs and corresponding description in HMDB.
   NO filename extension recommended, output filename will end with `.csv` or `xlsx` automatically (same as your input).

`e.g. D:\Users\work_dir\out_test  --->  D:\Users\work_dir\out_test.csv`
   
### 3. Sheet in your input file
   You will need this paramter only when you are using xlsx file as input. It determines which sheet the program will deal with. 
   
`e.g. 1 = Sheet1, 2 = Sheet2. You can also enter the name of sheet.`
If you want all sheets searched, just press `Enter`.

### Example
You can check xlsx file in `Example_data/HMDB_scraper_example`. Here is an example to running it:

1. When showing: 

`Please input your list file directory of metabolites (csv or xlsx format recommended, e.g. D:\Users\work_dir\test.csv): `

Enter directory of input file Metabolite_searching.xlsx on your computer.
For example, if I put it under the file folder `C:\User\Desktop\`, I should enter:

`C:\User\Desktop\Metabolite_searching.xlsx`

2. When showing:

`Please input your output file directory (with output name you want, e.g. D:\Users\work_dir\out_test): `

For example, if I want to put result under the file folder `C:\User\Desktop\Result\` and name it as `Result_HMDB`, I should enter:

`C:\User\Desktop\Result\Result_HMDB`

3. When showing:

`Which sheet do you want to search for?`

For example, if I want to search all sheets in input file, just press `Enter` on your keyboard.
Finally, you will get the same output file as `Result_HMDB.xlsx` in `Example_data/HMDB_scraper_example`. Have a try!

**Thanks Yusong Zhang from Shandong University for asking me for develop these tools.**

For more requirements and information worth, I will keep to update this scraper.

If any issue, please contact with kourongao@westlake.edu.cn
