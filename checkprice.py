from time import sleep
from app import app,mail
from apscheduler.schedulers.background import BackgroundScheduler

# Flask Mail modules 
from flask_mail import Message
from price_drop import GetPrice,collection


schedule = BackgroundScheduler()

def CheckPrice():
    print("Function CHal pada!!!")
    ActiveTrackers = collection.find({"status":"Active"})
    
    for tracker in ActiveTrackers:
        
        url = tracker['url']
        price = GetPrice(url)
        TargetPrice = tracker['TargetPrice']
        username = tracker['username']

        if price < TargetPrice:

            # sending mail to the respected user
            msg = Message("Price Dropped", sender='kunalyadav8600@gmail.com',
            recipients = [tracker['username']])
            msg.body = "Price has been drop for a product you added for alert. Click On the Below Link to Visit the Page.\n{}".format(url)
            with app.app_context():
                mail.send(msg)

            # setting status as deactivated to not repeat the mail
            collection.update_one({"username":username,"url":url},{"$set":{"status":"Deactivated"}})

schedule.add_job(id= "Tracker",func = CheckPrice,trigger='interval',hours = 1)
schedule.start()

while True:
    sleep(10)

