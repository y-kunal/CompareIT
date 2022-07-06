from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://Username:password@Servername/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "Enter your flask secret key"

# mail config
# Name/IP address of the email server.
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# Port number of server used
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] =  os.environ.get('flask_email_id')
app.config['MAIL_PASSWORD'] = os.environ.get('flask_email_password')
mail = Mail(app)

db = SQLAlchemy(app)

from app import routes
