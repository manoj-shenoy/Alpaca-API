from bs4 import BeautifulSoup
import requests

url = 'https://finance.yahoo.com/gainers'
def WebScraper(url):
    r=requests.get(url)

    soup=BeautifulSoup(r.content)

    stock_list=[]
    for i in range(21,31,1):
        ind_stock=str(soup.find_all('a')[i]['href'])
        idx=ind_stock.find('=')
        stk=ind_stock[idx+1:]
        stock_list.append(stk)

    return stock_list
WebScraper(url=url)
