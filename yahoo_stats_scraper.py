''' 
NAME: Janit Sriganeshaelankovan 
CREATED: July 3, 2018 - 21:36 (EDT)
GOAL: Yahoo Company Stats Scraper
ENVIRONMENT: Base
LAST UPDATE: January 13, 2019 - 22:40 (EDT)
'''




import re
import requests 
from bs4 import BeautifulSoup as soup
import time
from collections import OrderedDict
import csv
import pandas as pd 


''' YAHOO COMPANY STATISTICS '''
#GET THE METERICS
meterics = {}
with open('Yahoo_StatMeterics.txt', 'r') as f:
    for x in f:
        met = x.split(':')
        meterics[met[0]] = met[1].strip('\n').strip(' ')

meterics = OrderedDict(sorted(meterics.items(), key=lambda t: t[0]))
meterics_keys = sorted(meterics.keys())



#GET THE INFO
def get_stats(tickers_list):
    filename = 'company_stats'
    for idx, ticker in enumerate(tickers_list):
        time.sleep(1)
        print('WORKING ON {}: {}'.format(idx, ticker))
        
        resp = requests.get(r'https://ca.finance.yahoo.com/quote/{}/key-statistics'.format(ticker))
        html = resp.text
        page_soup = soup(html, 'lxml')
        body = page_soup.body
        data = str(body.find_all('script'))
        values = data.split(r'"QuoteSummaryStore"')
        
        with open('{}.txt'.format(filename), 'a',  encoding='utf-8') as f:
            f.write(ticker + ',')
            try:
                for key, val in meterics.items():
            #        print('{}, {}'.format(key, val))
                    pattern = '"%s":{(.*?)}' % (val,)
                    d = re.findall(pattern, values[1])
                    
                    if d:
                        pattern2 = r'"fmt":(.*)'
                        value = re.findall(pattern2, d[0])
                    else:
                        value = d 
                    
                    if value:
                        v =  value[0].split(',', 1)[0]
                        v = v.strip('""')
        #                print('{}: {}'.format(key, v))
                        f.write(v + ',')
                    else:
                        value_none = 'NAN'
        #                print('{}: {}'.format(key, value_none))
                        f.write(value_none + ',')
                f.write('\n')
            except Exception as e:
                print('{} could not be found'.format(ticker))
                f.write('NAN')
                f.write('\n')
                
#CONVERT TXT FILE TO CSV 
def converter(filename):
    with open('{}.txt'.format(filename), 'r') as csvfile:
            csvfile1 = csv.reader(csvfile, delimiter=',')
            with open('{}.txt'.format(filename).replace('.txt','.csv'), 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                for row in csvfile1:
                    writer.writerow(row)


def more_stats(filename):
    df = pd.read_csv('{}.txt'.format(filename))
    #print(df.columns.values)
    df.set_index('Ticker', inplace=True)
    
    #print(df.index.name)
    
    #print(df.dtypes)
    
    df = df.assign(Sector="", Industry="")
    
    
    
    groups = {'Sector':"sector", 'Industry':"industry"}
    
    ind = df.index.get_values()
    len(ind)
    for idx, i in enumerate(ind):
        print('{}:{}'.format(idx, i))
        resp = requests.get(r'https://ca.finance.yahoo.com/quote/{}'.format(i))
        html = resp.text
        page_soup = soup(html, 'lxml')
        body = page_soup.body
        data = str(body.find_all('script'))
        values = data.split(r'"summaryProfile"')
        
        try:
            if values:
                for key, val in groups.items():
                    sentence = values[1].split(r'"%s":' % (val, ))
                    matches = re.findall(r'\"(.+?)\"',sentence[1])
                    if matches[0]:
                        if key == 'Website':
                            try:
                                m = matches[0].split('www.')
                                df.loc[i, key] = m[1]
                            except:
                                m = matches[0].split('www.')
                                df.loc[i, key] = m[0]
                        else:
                            df.loc[i, key] = matches[0]
                    else:
                        print("NO {} INFO FOUND ON {}".format(key, i))
                        df.loc[i, key] = 'NAN'
            else:
                print("NO DATA FOUND ON {}".format(i))
                df.loc[i, 'Sector'] = 'NAN'
                df.loc[i, 'Industry'] = 'NAN'
#                continue
            
        except Exception as e:
            print('{}:{}'.format(i, str(e)))
            df.loc[i, 'Sector'] = 'NAN'
            df.loc[i, 'Industry'] = 'NAN'
        
    df.to_csv('{}_moreinfo.csv'.format(filename))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
