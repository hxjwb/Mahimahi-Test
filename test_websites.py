import csv
list_path = '/home/xiangjie/Mahimahi-Test/cipherscan/top1m/top-1m.csv'
# read the list
with open(list_path, 'r') as f:
    reader = csv.reader(f)
    urls = list(reader)

urls = urls[0:20]

import os

for url in urls:
    url = url[1]
    print(url)
    cmd1 = f'python3 runsel.py --url {url}'
    
    os.system(cmd1)