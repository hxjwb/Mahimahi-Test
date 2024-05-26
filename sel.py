
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    
    # url
    parser.add_argument('--url', type=str, default="http://www.google.com")
    
    url = parser.parse_args().url
    # This is the path to the chromedriver
    path = "/home/xiangjie/Mahimahi-Test/compete_stream/chromedriver-linux64/chromedriver"
    path2 = "/home/xiangjie/Mahimahi-Test/chrome-linux64"


    # from tqdm import tqdm


    #Alexa top 1000




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

    # set timeout to 30 seconds
    driver.set_page_load_timeout(30)


    # url = "http://www.google.com"

    driver.get(url)

    print(driver.title)
    time.sleep(30)



# ips = []
# titles = []

# for i in tqdm(range(200)):


#     url = urls[i][1]
    
#     # get the ip address of the url
#     # print(url)
    
#     # try:
#     #     os.system("host "+url +" > ip.txt") 
#     #     with open("ip.txt") as f:
#     #         ip = f.read().split('\n')[0].split()[-1]
#     #     # print(ip)
        
#     #     ips.append(ip)
#     # except:
#     #     # print("error")
#     #     ips.append("error")
#     #     continue
    
    
#     try:
#         driver.get("http://"+url) 
#         time.sleep(5)

#         print(driver.title)
        
#         titles.append(driver.title)
#     except:

#         print("timeout")
#         titles.append("timeout")
    
    
# import pandas as pd

# df = pd.DataFrame({'url': urls[0:1000], 'ip': ips, 'title': titles})

# df.to_csv('top1000.csv', index=False)



# 