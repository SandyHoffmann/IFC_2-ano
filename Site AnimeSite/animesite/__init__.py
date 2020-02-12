from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from animesite.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(Config)
bcrypt = Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USERNAME']='animekawaaiwebsite@gmail.com'
app.config['MAIL_PASSWORD']='narutouzumaki69'
app.config['MAIL_DEFAULT_SENDER']='animekawaaiwebsite@gmail.com'

mail=Mail(app)


from animesite import routes
