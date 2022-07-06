import requests,time
from bs4 import BeautifulSoup

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36", 
   "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
   "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

#for selecting the even values for list of tuples of specs 
def even(length):
   if(length % 2==0 or length == 0):
      return True
   else:
      return False
      
def HtmlPage(textbox,DeviceType):
   # preparing query url using the text searched in the input text box
   
   if DeviceType=="1":
      url ="https://gadgets.ndtv.com/laptops/laptop-finder?query="+textbox 
   elif DeviceType=="2":
      url ="https://gadgets.ndtv.com/mobiles/phone-finder?query="+textbox

   time.sleep(1)
   page = requests.get(url,headers=header)
   htmlcontent = page.content

   # getting the url of full specs page
   soup = BeautifulSoup(htmlcontent,'html.parser')

   # "_flspc" is the class name of full specs link
   searched_url = soup.find("a",{"class":"_flspc"})['href']
   time.sleep(1)
   '''extracting the html of the full specs page and return the soup for traversing elements'''
   newpage = requests.get(searched_url,headers=header)
   new_htmlcontent = newpage.content
   new_soup = BeautifulSoup(new_htmlcontent,'html.parser')
   
   return new_soup
      
def ListOfSpecs(content):

   # removing the html tags from the content
   SpecsContentText=[]
   for i in range(len(content)):
      for j in range(len(content[i])):
         SpecsContentText.append(content[i][j].text)

   # making the content in specs value by making list of tuple
   temp=[]
   i=0
   while(i<(len(SpecsContentText)-1)): 
         temp.append((SpecsContentText[i],SpecsContentText[i+1]))
         i=i+1
   # Fetching only even of value to not get repeated specs
   Specs = []
   for i in range(len(temp)):
      if(even(i)):
            Specs.append((temp[i][0],temp[i][1]))
   
   return Specs

'''Combining the two dictionary of the specification in one dictionary'''
def CombineSpecs(SpecsDict1,SpecsDict2):
   CombinedSpecs = {}
   for i in SpecsDict1:
      if i in SpecsDict2 or i in SpecsDict1:
         CombinedSpecs[i] = SpecsDict1.get(i),SpecsDict2.get(i)

   return CombinedSpecs