'https://www.chinabidding.com/en'

# https://www.chinabidding.com/en/foreignLoansDetail/254509338-BidNoticeEn.html
# 0701-23181168616r
# Project Name:Yichang Three Gorges Modern Logistics Center Infrastructure -Procurement of Port comprehensive equipmentPlace of Implementation
# Place of Implementation:Hubei YichangList of Products
# Beginning of Selling Bidding Documents:2023-01-20
# Ending of Selling Bidding Documents:2023-03-10
# Price of Bidding Documents:￥2000/$2855
# Purchasers:Yichang Transportation Investment Co
# Contact:Huang jianTel
# Tel:0086-0717-6288518
# Bidding Agency:China International Tendering Co
# Bank(USD):Business Department of Bank of China Head OfficeAccount NO
# Account NO.(USD):778350040281


import pandas as pd
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
from rake_nltk import Rake
import re
import requests
import spacy
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

class Scrape():
    
    ## Get url to perform scraping
    def __init__(self,url):
        self.url=url

    ## Create a method to get Soup object of HTML text and add all the important tags
    def bsoup(self):
        html_text=requests.get(self.url,verify=False).text
        self.soup=BeautifulSoup(html_text,'lxml')
        div_tags_IBRD=self.soup.find_all('div', class_="ui-list-div ui-list-IBRD"'')

        self.a_tags=[]
        for i in range(0,len(div_tags_IBRD)):
            self.a_tags.extend(div_tags_IBRD[i].find_all('a'))

    ## Create method to get all the important hyperlinks of tenders/projects
    project_links=[]
    def links(self):
        self.bsoup()
        for i in self.a_tags:
            if i.get('href') != '#':
                if len(i.get('href'))==77:
                    self.project_links.append(i.get('href'))

    ## Create method to extract important attributes of project from each project link
    def attributes(self):
        self.links()
        self.text=[]
        for i in self.project_links[0:10]:
            html_text_i=requests.get(i,verify=False).text
            soup=BeautifulSoup(html_text_i,'lxml')
            print(i)

    #         self.title = soup.find('p').text.strip()
    #         self.main_info = soup.find('div',class_='main-info').text.strip()
    #         self.text.append(self.main_info)

    #         self.bid_no=re.search('[\d-]+[a-z]{1}',self.title)
    #         self.project_name=re.search('Project Name:[ \w-]+',self.main_info)
    #         self.place_imple=re.search('Place of Implementation:[ \w-]+',self.main_info)
    #         self.start_bid_doc_sell=re.search('Beginning of Selling Bidding Documents:[\d-]+',self.main_info)
    #         self.end_bid_doc_sell=re.search('Ending of Selling Bidding Documents:[\d-]+',self.main_info)
    #         self.price_bid_doc=re.search('Price of Bidding Documents:￥[\d/$]+',self.main_info)
    #         self.perchaser=re.search('Purchasers:[\w -]+',self.main_info)
    #         self.contact_person=re.search('Contact:[\w -]+',self.main_info)
    #         self.tele_phone=re.search('Tel:[\d -]+',self.main_info)
    #         self.bidding_agency=re.search('Bidding Agency:[\w -]+',self.main_info)
    #         self.remittance_bank_USD=re.search('Bank\(USD\):[\w ]+',self.main_info)
    #         self.account_no_USD=re.search('Account NO.\(USD\):[\w ]+',self.main_info)
    #         break
            
            

    # def tokenize(self):
    #     self.attributes()
    #     self.tokens_list=[]
    #     for i in self.text:
    #         self.tokens_list.append(word_tokenize(i))
    #         break
        
    #     return self.tokens_list
    
    # def cleaning(self):
    #     self.tokenize()
    #     self.clean_list=[]
    #     for i in self.tokens_list:
    #         list1=[j for j in i if j not in punctuation]
    #         self.clean_list.append(list1)

    #     return self.clean_list

    # def normalize(self):
    #     self.cleaning()
    #     self.normal_words=[]
    #     for i in self.clean_list:
    #         list2=[j.lower() for j in i if j.isalnum()]
    #         self.normal_words.append(list2)

    #     return self.normal_words

    # def remove_stops(self):
    #     self.normalize()
    #     self.domain_words=[]
    #     words=stopwords.words('english')
    #     for i in self.normal_words:
    #         list3=[j for j in i if j not in words]
    #         self.domain_words.append(list3)

    #     return self.domain_words

    # def keyphrase_extract(self):
    #     self.remove_stops()
    #     rake=Rake()
    #     for i in self.domain_words:
    #         string1=' '.join(i)
    #         rake.extract_keywords_from_text(string1)
    #         print(rake.get_ranked_phrases_with_scores())

#     def standardize(self):
#         self.attributes()
#         self.Bidding_No=[]
#         self.Project_Name=[]
#         self.Place_of_Implementation=[]
#         self.Start_Bid_Doc_Sell=[]
#         self.End_Bid_Doc_Sell=[]
#         self.Price_of_Bid_Doc=[]
#         self.Perchaser=[]
#         self.Contact_Person=[]
#         self.Telephone_No=[]
#         self.Bidding_Agency=[]
#         self.Remittance_Bank_USD=[]
#         self.Account_No_USD=[]

#         for i in self.project_links:
#             self.Bidding_No.append(self.bid_no.group())

#             name=self.project_name.group().replace('Place of Implementation','')
#             name1=name.replace('Project Name:','')
#             self.Project_Name.append(name1)
            
#             print(self.project_name.group())
#             print(self.place_imple.group())
#             print(self.start_bid_doc_sell.group())
#             print(self.end_bid_doc_sell.group())
#             print(self.price_bid_doc.group())
#             print(self.perchaser.group())
#             print(self.contact_person.group())
#             print(self.tele_phone.group())
#             print(self.bidding_agency.group())
#             print(self.remittance_bank_USD.group())
#             print(self.account_no_USD.group())
#             # print(pd.read_html(i)[0],'\n\n')
#             break

obj=Scrape('https://www.chinabidding.com/en')
obj.attributes()