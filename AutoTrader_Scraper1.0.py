# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 12:08:03 2022

@author: Samid
"""

from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import re
import time
import random
import os
from nltk.sentiment import SentimentIntensityAnalyzer

os.chdir("G:/Samid work/Python/Car Prices/")
os.getcwd()

headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

sia = SentimentIntensityAnalyzer()
# setting up the lists that will form our dataframe with all the results
titles = []
subtitles = []
extraDetails =[]
price = []
RegYear = []
BodyType = []
Mileage = []
EngineSize = []
HP = []
Seller =[]
KeyDetails1 =[]
KeyDetails2 =[]
KeyDetails3 =[]
KeyDetails4 =[]
KeyDetails5 =[]
KeyDetails6 =[]
KeyDetails7 =[]
KeyDetails8 =[]
KeyDetails9 =[]
KeyDetails10 =[]


start = time.time()

link= 'https://www.autotrader.co.uk/car-search?sort=price-asc&postcode=wc2r2pp&radius=20&include-delivery-option=on&year-to=2022'
links = [link]

# Work out number of results
sapo_url = str(links[0])
r = get(sapo_url, headers=headers)
page_html = BeautifulSoup(r.text, 'html.parser')
HC2 = page_html.find_all('h1', class_="search-form__count js-results-count")      #for first page
NumResults = int(re.findall(r'\d+,\d+',str(HC2))[0].replace(",",""))
Pages = round(NumResults/10)
print('There are',NumResults,'results for this query, and', Pages, 'pages.')

# 10 results per page so divide number of results by 10 to get number of pages

for i in range(2,round(Pages)):
    links.append(link + str(i))
    
if  len(links)+1 >100:   
    print('Scraping 100 out of', len(links)+1, 'pages:')            #AutoTrader doesn't seem to handle over 100 pages


# We can now loop our code over these links to scrape our variables
    
start = time.time()  
for url in range(len(links)):
    print('Page', url)
    sapo_url = str(links[url])
    r = get(sapo_url, headers=headers)
    page_html = BeautifulSoup(r.text, 'html.parser')
    car_containers = page_html.find_all('div', class_="product-card__inner")
    if car_containers  != []:
        for idx, container in enumerate(car_containers ):
            
            #Title
            t= re.search('(?<="product-card-details__title">\n).*', str(car_containers[idx])).group()
            titles.append(t)
            
            #Subtitle
            s= re.search('(?<="product-card-details__subtitle">\n).*', str(car_containers[idx])).group()
            subtitles.append(s)
            
            #Extra details
            try:
                e= re.search('(?<="product-card-details__attention-grabber">\n).*', str(car_containers[idx])).group()
                extraDetails.append(e)
            except:
                extraDetails.append('NA')
                
            #Price
            p= re.search('(?<="product-card-pricing__price">\n).*', str(car_containers[idx])).group()
            P= p.replace(',','').replace('£','').replace('<span>','').replace('</span>','')
            price.append(P)
            
            
            #Seller
            seller= re.search('(?<=<h3 class="product-card-seller-info__name atc-type-picanto">).*', str(car_containers[idx])).group().replace('</h3>','')
            Seller.append(seller)
            
            #Key Specs
            """
            have 5 specs which are in a tricky format with new lines between each.
            So make multiple fillers for each spec and subtract
            """
            AllSpecs = re.search('(?<="listing-key-specs">\n).*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*', str(car_containers[idx])).group() #abcde
            KeyDetails= AllSpecs.replace('<li class="atc-type-picanto--medium">','').replace('</li>','').replace('</ul>\n</section>\n</div>\n<div class="product-card-seller-info">','')
            DetailsList= KeyDetails.splitlines()
            
            while len(DetailsList) <10:
                DetailsList.append('N/A')
          
            KeyDetails1.append(DetailsList[0])   
            KeyDetails2.append(DetailsList[1])
            KeyDetails3.append(DetailsList[2])
            KeyDetails4.append(DetailsList[3])
            KeyDetails5.append(DetailsList[4])
            KeyDetails6.append(DetailsList[5])
            KeyDetails7.append(DetailsList[6])
            KeyDetails8.append(DetailsList[7])
            KeyDetails9.append(DetailsList[8])
            KeyDetails10.append(DetailsList[9])
            Mileage.append('N/A')
 
            
    else:
        break
    
    time.sleep(random.randint(1,3))
    
end = time.time() - start

Cars_df = pd.DataFrame(
{
 'Titles': titles, 
 'Subtitles':subtitles, 
 'Extra details': extraDetails, 
 'Price': price, 
 'Seller Name': Seller,
 'KeyDetails1': KeyDetails1, 
 'KeyDetails2': KeyDetails2, 
 'KeyDetails3': KeyDetails3,
 'KeyDetails4': KeyDetails4, 
 'KeyDetails5': KeyDetails5, 
 'KeyDetails6': KeyDetails6, 
 'KeyDetails7': KeyDetails7, 
 'KeyDetails8': KeyDetails8, 
 'KeyDetails9': KeyDetails9, 
 'KeyDetails10': KeyDetails10
})


file = "DescendingCars_df" + str(round(end)) +".tsv"

Cars_df.to_csv(file, sep="\t",index=False) 

print(end)       
