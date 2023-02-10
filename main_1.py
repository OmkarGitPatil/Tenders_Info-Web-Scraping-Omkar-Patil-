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
    count=1
    def attributes(self):
        self.links()
        self.text=[]
        self.a=[]
        self.b=[]
        self.c=[]
        self.d=[]
        self.e=[]
        self.f=[]
        self.g=[]
        self.h=[]
        self.ii=[]
        self.j=[]
        self.k=[]
        self.l=[]
        for i in self.project_links[10:20]:
            html_text_i=requests.get(i,verify=False).text
            soup=BeautifulSoup(html_text_i,'lxml')
            print(f'link {self.count} is ',i)
            self.count+=1

            self.title = soup.find('p').text.strip()
            self.main_info = soup.find('div',class_='main-info').text.strip()
            self.text.append(self.main_info)
            self.a.append(re.search('[\d][\w-]+',self.title))
            self.b.append(re.search('Project Name:[ \w-]+',self.main_info))
            self.c.append(re.search('Place of Implementation:[ \w-]+',self.main_info))
            self.d.append(re.search('Beginning of Selling Bidding Documents:[\d-]+',self.main_info))
            self.e.append(re.search('Ending of Selling Bidding Documents:[\d-]+',self.main_info))
            self.f.append(re.search('Price of Bidding Documents:￥[\d/$]+',self.main_info))
            self.g.append(re.search('Purchasers:[\w -]+',self.main_info))
            self.h.append(re.search('Contact:[\w .-]+',self.main_info))
            self.ii.append(re.search('Tel:[\d -]+',self.main_info))
            self.j.append(re.search('Bidding Agency:[\w -]+',self.main_info))
            self.k.append(re.search('Bank\(USD\):[\w ]+',self.main_info))
            self.l.append(re.search('Account NO.\(USD\):[\w ]+',self.main_info))
            
    ## Create method to make tokens of text data
    def tokenize(self):
        self.attributes()
        self.tokens_list=[]
        for i in self.text:
            self.tokens_list.append(word_tokenize(i))
            break
        
        return self.tokens_list
    
    ## Create method to clean tokens of text data
    def cleaning(self):
        self.tokenize()
        self.clean_list=[]
        for i in self.tokens_list:
            list1=[j for j in i if j not in punctuation]
            self.clean_list.append(list1)

        return self.clean_list
    
    ## Create method to normalize tokens of text data
    def normalize(self):
        self.cleaning()
        self.normal_words=[]
        for i in self.clean_list:
            list2=[j.lower() for j in i if j.isalnum()]
            self.normal_words.append(list2)

        return self.normal_words

    ## Create method to remove stopwords from text data
    def remove_stops(self):
        self.normalize()
        self.domain_words=[]
        words=stopwords.words('english')
        for i in self.normal_words:
            list3=[j for j in i if j not in words]
            self.domain_words.append(list3)

        return self.domain_words

    ## Create method to extract keyphrase
    def keyphrase_extract(self):
        self.remove_stops()
        rake=Rake()
        for i in self.domain_words:
            string1=' '.join(i)
            rake.extract_keywords_from_text(string1)
            print(rake.get_ranked_phrases_with_scores())

    ## Create method to standardize the text data
    def standardize(self):
        self.attributes()
        self.Bidding_No=[]
        self.Project_Name=[]
        self.Place_of_Implementation=[]
        self.Start_Bid_Doc_Sell=[]
        self.End_Bid_Doc_Sell=[]
        self.Price_of_Bid_Doc=[]
        self.Perchaser=[]
        self.Contact_Person=[]
        self.Telephone_No=[]
        self.Bidding_Agency=[]
        self.Remittance_Bank_USD=[]
        self.Account_No_USD=[]

        for i in range(0,10):
            if self.a[i] == None:
                self.Bidding_No.append('Nil')
            else:
                self.Bidding_No.append(self.a[i].group())

            if self.b[i] == None:
                self.Project_Name.append('Nil')
            else:
                self.Project_Name.append(self.b[i].group().replace('Place of Implementation','').split(':')[1])

            if self.c[i] == None:
                self.Place_of_Implementation.append('Nil')
            else:
                self.Place_of_Implementation.append(self.c[i].group().replace('List of Products','').split(':')[1])

            if self.d[i] == None:
                self.Start_Bid_Doc_Sell.append('Nil')
            else:
                self.Start_Bid_Doc_Sell.append(self.d[i].group().split(':')[1])

            if self.e[i] == None:
                self.End_Bid_Doc_Sell.append('Nil')
            else:
                self.End_Bid_Doc_Sell.append(self.e[i].group().split(':')[1])

            if self.f[i] == None:
                self.Price_of_Bid_Doc.append('Nil')
            else:
                self.Price_of_Bid_Doc.append(self.f[i].group().split(':')[1])
            
            if self.g[i] == None:
                self.Perchaser.append('Nil')
            else:
                self.Perchaser.append(self.g[i].group().split(':')[1])

            if self.h[i] == None:
                self.Contact_Person.append('Nil')
            else:
                self.Contact_Person.append(self.h[i].group().split(':')[1])

            if self.ii[i] == None:
                self.Telephone_No.append('Nil')
            else:
                self.Telephone_No.append(self.ii[i].group().split(':')[1])

            if self.j[i] == None:
                self.Bidding_Agency.append('Nil')
            else:
                self.Bidding_Agency.append(self.j[i].group().split(':')[1])

            if self.k[i] == None:
                self.Remittance_Bank_USD.append('Nil')
            else:
                self.Remittance_Bank_USD.append(self.k[i].group().split(':')[1])

            
            if self.l[i] == None:
                self.Account_No_USD.append('Nill')
            else:
                self.Account_No_USD.append(self.l[i].group().split(':')[1])
            # print(pd.read_html(i)[0],'\n\n')
            

        # print('self.Bidding_No',self.Bidding_No,len(self.Bidding_No),'\n\n')
        # print('self.Project_Name',self.Project_Name,len(self.Project_Name),'\n\n')
        # print('self.Place_of_Implementation',self.Place_of_Implementation,len(self.Place_of_Implementation),'\n\n')
        # print('self.Start_Bid_Doc_Sell',self.Start_Bid_Doc_Sell,len(self.Start_Bid_Doc_Sell),'\n\n')
        # print('self.End_Bid_Doc_Sell',self.End_Bid_Doc_Sell,len(self.End_Bid_Doc_Sell),'\n\n')
        # print('self.Price_of_Bid_Doc',self.Price_of_Bid_Doc,len(self.Price_of_Bid_Doc),'\n\n')
        # print('self.Perchaser',self.Perchaser,len(self.Perchaser),'\n\n')
        # print('self.Contact_Person',self.Contact_Person,len(self.Contact_Person),'\n\n')
        # print('self.Telephone_No',self.Telephone_No,len(self.Telephone_No),'\n\n')
        # print('self.Bidding_Agency',self.Bidding_Agency,len(self.Bidding_Agency),'\n\n')
        # print('self.Remittance_Bank_USD',self.Remittance_Bank_USD,len(self.Remittance_Bank_USD),'\n\n')
        # print('self.Account_No_USD',self.Account_No_USD,len(self.Account_No_USD))
        
    ## Create method to get .csv file containing all the important attributes and its content   
    def get_csv(self):
        self.standardize()

        df_dict={'URL of Tender':self.project_links[10:20],'Project ID':self.Bidding_No,'Project Name':self.Project_Name,
                'Page Content':self.text,
                'Place of Implementation':self.Place_of_Implementation,'Start Date of Doc Sell':self.End_Bid_Doc_Sell,
                'End Date of Doc Sell':self.End_Bid_Doc_Sell,'Price of Bid Doc':self.Price_of_Bid_Doc,
                'Purchaser':self.Perchaser,'Contact Person':self.Contact_Person,'Telephone No':self.Telephone_No,
                'Bidding Agency':self.Bidding_Agency,'Bank of Remittance':self.Remittance_Bank_USD,'Account No':self.Account_No_USD}

        df=pd.DataFrame(df_dict)

        df.to_csv(r'C:\Users\Omkar\Desktop\World Bank Projects\Web Scraper\CSV file\China Bidding Info 1.csv')

        return df


obj=Scrape('https://www.chinabidding.com/en')
print(obj.get_csv())