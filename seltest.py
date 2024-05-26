
# This is the path to the chromedriver
path = "/home/xiangjie/Mahimahi-Test/compete_stream/chromedriver-linux64/chromedriver"
path2 = "/home/xiangjie/Mahimahi-Test/chrome-linux64"


from tqdm import tqdm


#Alexa top 1000

list_path = '/home/xiangjie/Mahimahi-Test/cipherscan/top1m/top-1m.csv'

import csv
import random

# read the list
with open(list_path, 'r') as f:
    reader = csv.reader(f)
    urls = list(reader)

urls = urls[0:1000]

# use a ramdom seed to shuffle the list
# random.seed(10)

# random.shuffle(urls)



# print(urls[0:1000])

# add path to PATH
import os
os.environ["PATH"] += os.pathsep + path
os.environ["PATH"] += os.pathsep + path2

import time
from selenium import webdriver
# headless
options = webdriver.ChromeOptions()

options.add_argument('headless')

driver = webdriver.Chrome(path, chrome_options=options)

# set timeout to 10 seconds
driver.set_page_load_timeout(10)

ips = []
titles = []


# access through ip address
ip = "172.217.24.110"
driver.get("http://"+ip)


print(driver.title)
# for i in tqdm(range(1000)):


#     url = urls[i][1]
    
#     # get the ip address of the url
#     # print(url)
    
#     try:
#         os.system("host "+url +" > ip.txt") 
#         with open("ip.txt") as f:
#             ip = f.read().split('\n')[0].split()[-1]
#         # print(ip)
        
#         ips.append(ip)
#     except:
#         # print("error")
#         ips.append("error")
#         continue
    
    
#     try:
#         driver.get("http://"+ip) 

#         # print title of the page
#         # print(driver.title)
#         titles.append(driver.title)
#     except:
#         # timeout
#         # print("timeout")
#         titles.append("timeout")
    
    
# import pandas as pd

# df = pd.DataFrame({'url': urls[0:1000], 'ip': ips, 'title': titles})

# df.to_csv('top1000.csv', index=False)