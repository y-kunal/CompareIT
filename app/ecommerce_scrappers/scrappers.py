import requests,time
from bs4 import BeautifulSoup

def scrapper(url):
   # Header information to act like request is send by browser
   header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36", 
   "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
   "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

   # div classes for different types of structure of html
   div_class = ["_2kHMtA","_4ddWXP","_1xHGtK _373qXS"]
   time.sleep(2)

   # making a get request to the given url
   page = requests.get(url,headers=header)
   # getting the html of the page  
   htmlContent=page.content
   # making a Bs4 obj to traverse the html
   soup = BeautifulSoup(htmlContent,'html.parser')
   divClass =""

   # selecting the div class according to searched product 
   for i in div_class:
      temp = soup.find_all("div",{"class":i})
      if temp:
         divClass = i

   return divClass,soup

def FlipkartHtmlDetailsScraping(url):

   divClass,soup = scrapper(url)

   # different html classes of different html design
   flipkart_dic_class = {"_2kHMtA":{"image":"_396cs4 _3exPp9","heading":"_4rR01T","price":"_30jeq3 _1_WHN1"},
   "_4ddWXP":{"image":"_396cs4 _3exPp9","heading":"s1Q9rs","price":"_30jeq3"},
   "_1xHGtK _373qXS":{"image":"_2r_T1I","heading":"IRpwTa","price":"_30jeq3"}}
   
   # for smartphone and laptop types of product
   if divClass=="_2kHMtA":
      imgsrc = soup.find_all("img",{"class":flipkart_dic_class[divClass]["image"]})
      heading=soup.find_all("div",{"class":flipkart_dic_class[divClass]["heading"]})
      price = soup.find_all("div",{"class":flipkart_dic_class[divClass]["price"]})
      Pagelink = soup.find_all("a",{"class":"_1fQZEK"})

   # for fashion and clothing
   elif divClass == "_1xHGtK _373qXS":
      imgsrc = soup.find_all("img",{"class":flipkart_dic_class[divClass]["image"]})
      heading = soup.find_all("a",{"class":flipkart_dic_class[divClass]["heading"]})
      price = soup.find_all("div",{"class":flipkart_dic_class[divClass]["price"]})
      Pagelink = soup.find_all("a",{"class":flipkart_dic_class[divClass]["heading"]})
   
   # for others
   else:
      imgsrc = soup.find_all("img",{"class":flipkart_dic_class[divClass]["image"]})
      heading = soup.find_all("a",{"class":flipkart_dic_class[divClass]["heading"]})
      price = soup.find_all("div",{"class":flipkart_dic_class[divClass]["price"]})
      Pagelink = soup.find_all("a",{"class":flipkart_dic_class[divClass]["heading"]})




   title =[]
   cost =[]
   imageSrc = []
   link = []

   for i in range(len(heading)):
      title.append(heading[i].text.strip())
      cost.append(price[i].text.strip())
      imageSrc.append(imgsrc[i]['src'])
      link.append("https://flipkart.com"+Pagelink[i]['href'])

   return title,cost,imageSrc,link

def PaytmHtmlDetailsScrapping(url):

   divClass,soup = scrapper(url)  

   # different div classes for different product attributes like price, title and img

   heading = soup.find_all("div",{"class":"UGUy"})
   cost = soup.find_all("div",{"class":"_1kMS"})

   imgDiv = soup.find_all("div",{"class":"_3nWP"})
   PageLink = soup.find_all("a",{"class":"_8vVO"})

   src=[]
   price=[]
   title =[]
   link =[]
   for i in imgDiv:
      src.append(i.find("img")['src'])

   for i in range(len(heading)):
      title.append(heading[i].text.strip())
      price.append(cost[i].text.strip())
      link.append("https://paytmmall.com"+PageLink[i]['href'])
   
   return title,price,src,link

def AmazonHtmlDetailsScrapping(url):
   div,soup = scrapper(url)

   heading = soup.find_all("h2",{"class":"a-size-mini a-spacing-none a-color-base s-line-clamp-2"})
   cost = soup.find_all("span",{"class":"a-price-whole"})
   imgSrc = soup.find_all("img",{"class":"s-image"})
   PageLink = soup.find_all("a",{"class":"a-link-normal a-text-normal"})

   title = []
   price = []
   src = []
   link = []

   for i in range(len(heading)):
      title.append(heading[i].text)
      price.append(cost[i].text)
      src.append(imgSrc[i]['src'])
      link.append("https://amazon.in"+PageLink[i]['href'])

   return title,price,src,link 

def ShopCluesScrapping(url):

   soup = scrapper(url)[1]

   heading = soup.find_all("h2",{"class":""})
   cost = soup.find_all("span",{"class":"p_price"})
   imgSrc = soup.find("div",{"class":"cat_listing"}).find_all("img")
   PageLink = soup.find_all("div","column col3 search_blocks")
   
   title = []
   price = []
   src = []
   link = []

   for i in range(len(heading)):
      title.append(heading[i].text.strip())
      price.append(cost[i].text.strip())
      src.append(imgSrc[i]['src'])
   
   for i in range(len(PageLink)):
      link.append(PageLink[i].find("a")['href'])

   return title,price,src,link
   









