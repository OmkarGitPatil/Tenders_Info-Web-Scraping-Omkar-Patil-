import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

## Joining all the DataFrames created from 30 URLs (Separate three .py files used to scrape data as well as to create .csv files from them
## because all the 30 links could not be accessed by computer system in one try.)

df=pd.read_csv(r'C:\Users\Omkar\Desktop\World Bank Projects\Web Scraper\CSV file\China Bidding Info.csv')
df_1=pd.read_csv(r'C:\Users\Omkar\Desktop\World Bank Projects\Web Scraper\CSV file\China Bidding Info 1.csv')
df_2=pd.read_csv(r'C:\Users\Omkar\Desktop\World Bank Projects\Web Scraper\CSV file\China Bidding Info 2.csv')

df_total=pd.concat([df,df_1,df_2],ignore_index=True)
# df_total.to_csv(r'C:\Users\Omkar\Desktop\World Bank Projects\Web Scraper\CSV file\China Bidding Info Total.csv')
# print(df_total['Project ID'].to_list())

url='https://www.chinabidding.com/en'
html_text=requests.get(url,verify=False).text
soup=BeautifulSoup(html_text,'lxml')
div_tags_IBRD=soup.find_all('div', class_="ui-list-div ui-list-IBRD"'')

a_tags=[]
for i in range(0,len(div_tags_IBRD)):
    a_tags.extend(div_tags_IBRD[i].find_all('a'))

project_links=[]
for i in a_tags:
    if i.get('href') != '#':
        if len(i.get('href'))==77:
            project_links.append(i.get('href'))

## Storing list of products in the form of .csv file by the name of its Bidding No (Project ID)
count=0
list1=df_total['Project ID'].to_list()
for i in project_links[0:10]:
    df=pd.read_html(i)[0]
    df.to_csv(f'C:\\Users\\Omkar\\Desktop\\World Bank Projects\\Web Scraper\\List of Products\\{list1[count]}.csv',encoding='utf-8')
    count+=1

count=10
list1=df_total['Project ID'].to_list()
for i in project_links[10:20]:
    df=pd.read_html(i)[0]
    df.to_csv(f'C:\\Users\\Omkar\\Desktop\\World Bank Projects\\Web Scraper\\List of Products\\{list1[count]}.csv',encoding='utf-8')
    count+=1

count=20
list1=df_total['Project ID'].to_list()
for i in project_links[20:30]:
    df=pd.read_html(i)[0]
    df.to_csv(f'C:\\Users\\Omkar\\Desktop\\World Bank Projects\\Web Scraper\\List of Products\\{list1[count]}.csv',encoding='utf-8')
    count+=1