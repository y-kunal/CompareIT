from bs4 import BeautifulSoup
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import session

# mongodb dbms modules
from pymongo import MongoClient


cluster = MongoClient("Mongodb Atlas Uri")
db = cluster['CLuster Name']
collection = db['Database Name']

schedule = BackgroundScheduler()


def UrlAnalyzer(url):

    if "amazon" in url:

        indx = url.find("/dp/")
        if indx != -1:

            indx2 = indx+14
            ShortUrl = url[0:indx2]
            return ShortUrl
        
        else:
            return None 

    elif "flipkart" in url:
        
        indx = url.find("/p/")
        if indx != -1:

            indx2 = indx + 19
            ShortUrl = url[0:indx2]
            return ShortUrl

        else:
            return None 
    
    else:
         
         return None

def AddTracker(url,TargetPrice):
    
    ShortUrl = UrlAnalyzer(url)

    GroupByEmail = collection.find({"username":session['username']})
    AllUrl = []

    for i in GroupByEmail:
        AllUrl.append(i['url'])

    if ShortUrl not in AllUrl:
        collection.insert_one({'username':session['username'],'url':ShortUrl,'TargetPrice':TargetPrice,'status':"Active"})
        return True 
    else:
        return False

def GetPrice(url):
    
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36", 
    "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    page = requests.get(url,headers=header) 
    htmlcontent = page.content
    soup = BeautifulSoup(htmlcontent,'html.parser')

    if "flipkart" in url:
        
        UnFilteredPrice = soup.find("div",{"class":"_30jeq3 _16Jk6d"}).text

        StrPrice = UnFilteredPrice.strip()[1:].replace(",","")
        price = int(StrPrice)

        return price
    
    if "amazon" in url:

        UnFilteredPrice = soup.find("span",{"class":"a-offscreen"}).text

        StrPrice = UnFilteredPrice.strip()[1:].replace(",","")
        FloatPrice = float(StrPrice)
        price = round(FloatPrice)
        
        return price 
        

