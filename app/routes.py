from flask import render_template,request,url_for,session,redirect
from flask.helpers import flash
from app import app,db,mail

# sql database manangement
import sqlalchemy,pymysql

# hashing modules
from werkzeug.security import generate_password_hash,check_password_hash

# Mail modules
from flask_mail import Message

# My models
from app.models import userlogininfo,wishlist

# My modules
from app.Password_Generator import PasswordGenerator
from price_drop import AddTracker,collection
import app.ecommerce_scrappers.scrappers as myscrappers
import app.electronics_compare.ExtractSpecs as Ecompare


# browser header to pretend being a normal browser request 
header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36", 
"Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
"DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

# home page 
@app.route('/',methods=['GET','POST'])
def home():
   session['url'] = request.url
   return render_template("index.html")

# search results for searched item in the home page 
@app.route('/search/',methods=['GET','POST'])
def search_results():
   session['url'] = request.url
   # getting the search keyword
   searchurl = request.args.get('search_bar')
   
   # Url for all the ecommerce sites to search directly in the website
   # amazon_url = "https://www.amazon.in/s?k="+searchurl
   flipkart_url = "https://www.flipkart.com/search?q="+searchurl
   # reliance_url = "https://www.reliancedigital.in/search?q="+searchurl
   paytm_mall_url = "https://paytmmall.com/shop/search?q="+searchurl
   # tataCliq_url = "https://www.tatacliq.com/search/?searchCategory=all&text="+searchurl
   ShopClues_url = "https://www.shopclues.com/search?q="+searchurl

   try:

      '''flipkart products information'''
      FlipTitle,FlipPrice,FlipSrc,FlipLink = myscrappers.FlipkartHtmlDetailsScraping(flipkart_url)
   
      '''paytm products information'''
      PaytTitle,PaytPrice,PaytSrc,PaytLink = myscrappers.PaytmHtmlDetailsScrapping(paytm_mall_url)
   
      '''amazon products information'''
      # AmazTitle,AmazPrice,AmazSrc,AmazLink = myscrappers.AmazonHtmlDetailsScrapping(amazon_url)
   
      '''Shopclues products information'''
      ShopTitle,ShopPrice,ShopSrc,ShopLink = myscrappers.ShopCluesScrapping(ShopClues_url)

      return render_template("search.html",FlipTitle=FlipTitle,FlipPrice=FlipPrice,FlipSrc=FlipSrc,FlipLink = FlipLink
      ,PaytTitle=PaytTitle,PaytPrice=PaytPrice,PaytSrc=PaytSrc,PaytLink = PaytLink
      ,ShopTitle = ShopTitle,ShopPrice = ShopPrice,ShopSrc = ShopSrc,ShopLink = ShopLink)
   
   # ,AmazTitle = AmazTitle,AmazPrice=AmazPrice,AmazSrc=AmazSrc,AmazLink=AmazLink)
   
   except:
      flash('Sorry, No Result Found\nPlease check the spelling or try searching something else')
      return render_template("search.html")


# smartphone compare results page 
@app.route('/results/',methods=['GET','POST'])
def compare_results():
   try:

      session['url'] = request.url
      # get the text input from user from both the textbox
      textbox1 = request.args.get('textbox1')
      textbox2 = request.args.get('textbox2')
      DeviceType = request.args.get('DeviceType')
      
      # op= request.args.get('radioButton')

      # getting the html from the website with respect to the text in both the textbox

      
      soup1 = Ecompare.HtmlPage(textbox1,DeviceType)
      soup2 = Ecompare.HtmlPage(textbox2,DeviceType)

      
      
      # extracting all the tables
      SpecsContent1 = soup1.find("div",{"class":"_st-wrp"}).find_all("table")
      SpecsContent2 = soup2.find("div",{"class":"_st-wrp"}).find_all("table")
      specs1=[]
      specs2=[]
      # extracting table data 
      for i in range(len(SpecsContent1)):
         specs1.append(SpecsContent1[i].find_all("td"))
      
      for i in range(len(SpecsContent2)):
         specs2.append(SpecsContent2[i].find_all("td"))
      '''making the html into list of tuples(spec,value) and converting it into dictionary'''
      specs_list1 = dict(Ecompare.ListOfSpecs(specs1))
      specs_list2 = dict(Ecompare.ListOfSpecs(specs2))
      spec = Ecompare.CombineSpecs(specs_list1,specs_list2)

      device1_img = soup1.find("div",{"class":"_pdmimg __arModalBtn _flx"}).find("img")['src']
      device2_img = soup2.find("div",{"class":"_pdmimg __arModalBtn _flx"}).find("img")['src']


      return render_template("compare_results.html",specs=spec,device1_img = device1_img,device2_img=device2_img)

      
   except TypeError:
      flash('Sorry, No Result Found\nPlease check the spelling or try searching something else')
      return render_template("compare_results.html")

@app.route('/login/',methods=['GET','POST'])
def login():
   session['LoggedIn'] = False
   if request.method =='POST':
      # getting the user login userid and password
      session['username'] = request.form['login_username']
      password = request.form['login_password']

      user =  userlogininfo.query.filter_by(username = session['username']).first()
      
      if user:
      
         session['name'] = user.name
         password_hash = user.password
         if check_password_hash(password_hash,password):
            session['LoggedIn']  = True
            if 'url' in session:    
               return redirect(session['url'])
            else:
               return redirect(url_for('home'))

         else:
            flash('Incorrect email id or password')
            session['LoggedIn'] = False
            return redirect(url_for('login'))
         
      else:
         flash('Email-id Not registered!')
         return redirect(url_for('login'))
      
   return render_template('login.html')

def PasswordValidator(password):
   if len(password)<6:
      return False,"Password Must Have Atleast 6 Characters!"

   if len(password)>20:
      return False,"Password Must Be less than 20 Characters!"

   if not any(ch.isdigit() for  ch in password):
      return False,"Password Must Have Atleast One Digit!"
   
   if not any(ch.isupper() for ch in password):
      return False,"Password Must Include One upper case letter!"

   return True,"Valid Password"  
   
@app.route('/register/',methods=['GET','POST'])
def register():

   if request.method =='POST':
      # getting the user credentials 
      user_name = request.form['register_name']
      user_username = request.form['register_email']
      user_password = request.form['register_password']

      # checking if the password is a valid password
      IsPasswordValid = PasswordValidator(user_password)
      
      if IsPasswordValid[0] == True:
         # hashing the password
         password = generate_password_hash(request.form['register_password'])
      else:
         flash(IsPasswordValid[1])
         return render_template('register.html')

      try:
         # adding user 
         user =  userlogininfo(user_username,password,user_name)
         db.session.add(user)
         db.session.commit()
         session['username'] = user_username
         session['name'] = user_name
         session['LoggedIn'] = True

         # redirecting to the previous url
         if 'url' in session:
            return redirect(session['url'])
         else:
            return redirect(url_for('home'))

      except sqlalchemy.exc.IntegrityError:
         flash('Email-id already registered')
         return render_template('register.html')
           
   return render_template('register.html')   

@app.route('/add_item/',methods= ['GET','POST'])
def add_item():

   if 'LoggedIn' in session and  session['LoggedIn'] == True:

      product_name = request.args.get('product_name')
      product_price = request.args.get('price')
      product_link = request.args.get('site_link')
      product_image = request.args.get('image')
      id = session['username']+product_name 
      # filtering product in wishlist based on the username
      all_products =   wishlist.query.filter_by(username = session['username'])

      # filtering product names of a particular user
      all_products_name = []
      for i in all_products:
         all_products_name.append(i.ProductName)
      
      if product_name not in all_products_name:
         try:
            product =   wishlist(session['username'],product_name,product_price,product_link,product_image,id)
            db.session.add(product)
            db.session.commit()
      
         except sqlalchemy.exc.DatabaseError:
            new_product_price = product_price[1:]
            db.session.rollback()
            product =    wishlist(session['username'],product_name,new_product_price,product_link,product_image,id)
            db.session.add(product)
            db.session.commit()
         
            return redirect(url_for('my_wishlist'))

      else:
         flash('Item already in wishlist')
      
   else:
      return redirect(url_for('login'))

   return  render_template('add_item.html')

@app.route('/my_wishlist/',methods = ['POST','GET'])
def my_wishlist():
   
   if 'LoggedIn' in session and  session['LoggedIn'] == True:
      
      MyWishListProduct = wishlist.query.filter_by(username = session['username'])
      Product_Name = []
      Product_Price = [] 
      Image_Src = []
      Site_Link = []

      for i in MyWishListProduct:

         Product_Name.append(i.ProductName)
         Product_Price.append(i.ProductPrice)
         Site_Link.append(i.SiteLink)
         Image_Src.append(i.ImageSrc)

      # removing the question mark in the price 
      New_Product_Price = []

      for i in Product_Price:
         if "?" in i:
            New_Product_Price.append(i[1:])
         else:
            New_Product_Price.append(i)



      if request.method == "POST":
         product_name = request.form['product_name']
         db.session.query(wishlist).filter_by(username = session['username'],ProductName = product_name).delete()
         db.session.commit()

         

         return redirect(url_for('my_wishlist'))

   else:
      return redirect(url_for('login'))
   
   return render_template('wishlist.html',Product_Name = Product_Name,Product_Price = New_Product_Price,
   Site_Link = Site_Link,Image_Src = Image_Src,Length = len(Product_Name))

@app.route('/account_password_change/',methods=['POST','GET'])
def account_password_change():

   if 'LoggedIn' in session and  session['LoggedIn'] == True:
    
      if request.method == "POST":

         current_password = request.form['current_password']
         new_password = request.form['new_password']
         IsPasswordValid = PasswordValidator(new_password)

         if not IsPasswordValid[0] == True:
            flash(IsPasswordValid[1])
            return render_template('password_change.html')


         #  extract the user with the logged in email id 
         user = userlogininfo.query.filter_by(username = session['username']).first()

         #  check if entered password matches with the original password 
         if check_password_hash(user.password,current_password):

            #  filtering user by username and changing password 
            db.session.query(userlogininfo).filter_by(username=session['username']).update({userlogininfo.password: generate_password_hash(new_password)})
            db.session.commit()
            flash('Password Successfully Changed!')
            session['LoggedIn']  = False
            return render_template('login.html')
         
         else:
            flash("Incorrect Password")

      return render_template('password_change.html')
   
   else:
      return redirect(url_for('login'))

@app.route('/reset_password/',methods=['POST','GET'])
def reset_password():
   if request.method == 'POST': 
      # Getting user email_id
      email_id = request.form["email_id"]
      
      # searching for the email_id in the database 
      user = userlogininfo.query.filter_by(username = email_id).first()

      # checking if the user with the email exist. If exist generate and send a new password 
      if user:

         resetted_password = PasswordGenerator()
         msg = Message("CompareIT Account Password Reset", sender='kunalyadav8600@gmail.com',
         recipients = [email_id])
         msg.body = "Password : {} \nYour Password Has Been Resetted. Please Change Your Password as soon as possible.".format(resetted_password)
         
         try:
            mail.send(msg)
            db.session.query(userlogininfo).filter_by(username=email_id).update({userlogininfo.password: generate_password_hash(resetted_password)})
            db.session.commit()
            flash('Password Successfully sent to your registered Email-Id')
            return redirect(url_for('login'))

         except:
            flash('Some Error Has Occured')
            db.session.rollback()
            return render_template('reset_pass.html')

      # else throw message incorrect email
      else:
         flash('Incorrect Email-id')
   return render_template('reset_pass.html')

@app.route('/price_drop_alert/',methods= ['POST','GET'])
def price_drop_alert():
   session['url'] = request.url
   
   if 'LoggedIn' in session and  session['LoggedIn'] == True:
      if request.method == "POST":
         url = request.form['user_url']
         target_price = int(request.form['target_price'])
         
         FlashMsg = AddTracker(url,target_price)

         if FlashMsg:
            flash("Tracker Successfully Added")

         else:
            flash("Tracker Already Exist for the given Url")

   else:
      return redirect(url_for('login'))   

   return render_template('price_drop.html')

@app.route('/view_added_alerts/',methods = ['POST','GET'])
def view_added_alerts():
   
   if 'LoggedIn' in session and  session['LoggedIn'] == True:

      trackers = collection.find({'username':session['username']})
      url =[]
      target_price =[]
      Status=[]

      for tracker in trackers:

         url.append(tracker['url'])
         target_price.append(tracker['TargetPrice'])
         Status.append(tracker['status'])


      if request.method == "POST":

         # To differentiate Between Requests for delete and Activate Tracker
         if 'delete_btn' in request.form:
            HiddenUrl = request.form['HiddenUrl']

            collection.delete_one({"username":session['username'],"url":HiddenUrl})

            return redirect(url_for('view_added_alerts'))

         if 'activate_btn' in request.form:
            Url = request.form['HiddenUrlActivate']

            collection.update_one({"username":session['username'],'url':Url},{"$set":{"status":"Active"}})

            return redirect(url_for('view_added_alerts'))
      
   else:

      return redirect(url_for('login'))

   return render_template('view_alerts.html',url = url, TargetPrice = target_price,Status =Status ,length = len(url))

      
