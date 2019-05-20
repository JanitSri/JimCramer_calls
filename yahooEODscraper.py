''' 
NAME: Janit Sriganeshaelankovan 
CREATED: July 3, 2018 - 21:36 (EDT)
GOAL: Yahoo Finance End-of-day Scraper 
LAST UPDATE: January 10, 2019 - 20:13 (EDT)
'''


import time 
import datetime 
from bs4 import BeautifulSoup as soup
import re
import requests 
import os 



def individual_security_eod(start_date, end_date, equities):
    path4 = r'C:\Users\janit\Documents\Practice - Python\Finance - python\Jim Cramer\final\stocks_data'
    
    equity_list = equities
    no_data = []
    total_time = []
    
    start = int(time.mktime(datetime.datetime.strptime(start_date, "%d/%m/%Y").timetuple()))
    
    end = int(time.mktime(datetime.datetime.strptime(end_date, "%d/%m/%Y").timetuple()))
    
    print('The start date is {} and the end date is {}'.format(start,end))
    
    for idx, t in enumerate(equity_list):
        time.sleep(1)
        start_time = time.time()
        print('{} -- {}'.format(idx, t))
        test_list = []
                
        # parsing the data 
        resp = requests.get('https://ca.finance.yahoo.com/quote/{}/history?period1={}&period2={}&interval=1d&filter=history&frequency=1d'.format(t, start, end))
        html = resp.text
        page_soup = soup(html, 'lxml')
        body = page_soup.body
        data = str(body.find_all('script'))
        
        # REGEX formating 
        d = re.findall(r'"HistoricalPriceStore":(.*)\]?', data)
        for x in d:
            y = re.findall(r'^[^\]]+', x)
            for i in y:
                final_data = re.findall(r'"prices":(.*)\]?', i)
                final_final_data = [x.split(r'},') for x in final_data]
            for x in final_final_data[0]:
                m = re.findall(r'\{"date":(\d+.?\d+),"open":(\d+.?\d+),"high":(\d+.?\d+),"low":(\d+.?\d+),"close":(\d+.?\d+),"volume":(\d+.?\d+),"adjclose":(\d+.?\d+)', x)
                if m:
                    test_list.append(m)
        
        # writing to txt file 
        if test_list:
            with open(path4 + '\{}.txt'.format(t), 'w') as f:
                for l in test_list:
                    ll = ','.join(a for a in l[0][:])
#                    print(ll)
                    f.write(ll + '\n')
        else:
            no_data.append(t)
        total_time.append(time.time()-start_time)    
    
    print('done')














