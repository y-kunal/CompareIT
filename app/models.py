from app import db


# intializing database table schema
# Login details table 
class userlogininfo(db.Model):

   # column definition
   username = db.Column(db.String(100),unique = True,primary_key = True)
   password = db.Column(db.VARCHAR(300),nullable = False)
   name = db.Column(db.String(100),nullable = False)

   def __init__(self,username,password,name):
      self.username = username 
      self.password = password
      self.name = name

# user wishlist table 
class wishlist(db.Model):

   # column definition
    username = db.Column(db.String(100),db.ForeignKey('userlogininfo.username'),nullable = False)
    ProductName = db.Column(db.String(500))
    ProductPrice = db.Column(db.String(50))
    SiteLink = db.Column(db.String(1000))
    ImageSrc = db.Column(db.String(1000))
    Id = db.Column(db.String(500),primary_key = True)

    def __init__(self,username,ProductName,ProductPrice,SiteLink,ImageSrc,Id):
        
        self.username = username
        self.ProductName = ProductName
        self.ProductPrice = ProductPrice
        self.SiteLink = SiteLink
        self.ImageSrc = ImageSrc
        self.Id = Id

